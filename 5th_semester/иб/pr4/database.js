// database.js
const initSqlJs = require('sql.js');
const fs = require('fs-extra');
const path = require('path');

let db = null;
let dbFile = path.join(__dirname, 'app.db');

// Инициализация базы данных
async function initDatabase() {
  // Загружаем SQL.js
  const SQL = await initSqlJs();
  
  // Загружаем существующую БД или создаём новую
  let buffer;
  try {
    buffer = await fs.readFile(dbFile);
    db = new SQL.Database(buffer);
  } catch (error) {
    // Файл не существует, создаём новую БД
    db = new SQL.Database();
  }
  
  // Включаем foreign keys
  db.run('PRAGMA foreign_keys = ON');
  
  // Инициализация таблиц
  initTables();
  
  // Сохраняем БД
  saveDatabase();
  
  // Очистка устаревших сессий и токенов
  cleanupExpiredSessions();
  
  // Периодическое сохранение (каждые 5 минут)
  setInterval(() => {
    saveDatabase();
    cleanupExpiredSessions();
  }, 5 * 60 * 1000);
}

// Инициализация таблиц
function initTables() {
  // Таблица пользователей
  db.run(`
    CREATE TABLE IF NOT EXISTS users (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      username TEXT UNIQUE NOT NULL,
      password_hash TEXT NOT NULL,
      role TEXT NOT NULL DEFAULT 'user',
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
  `);
  
  // Таблица сессий
  db.run(`
    CREATE TABLE IF NOT EXISTS sessions (
      id TEXT PRIMARY KEY,
      user_id INTEGER NOT NULL,
      expires_at DATETIME NOT NULL,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
  `);
  
  // Таблица CSRF токенов
  db.run(`
    CREATE TABLE IF NOT EXISTS csrf_tokens (
      token TEXT PRIMARY KEY,
      session_id TEXT NOT NULL,
      expires_at DATETIME NOT NULL,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE CASCADE
    )
  `);
  
  // Таблица задач
  db.run(`
    CREATE TABLE IF NOT EXISTS tasks (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      user_id INTEGER NOT NULL,
      title TEXT NOT NULL,
      description TEXT,
      completed INTEGER DEFAULT 0,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
  `);
  
  // Создаём индексы
  try {
    db.run('CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON sessions(user_id)');
    db.run('CREATE INDEX IF NOT EXISTS idx_sessions_expires_at ON sessions(expires_at)');
    db.run('CREATE INDEX IF NOT EXISTS idx_csrf_session_id ON csrf_tokens(session_id)');
    db.run('CREATE INDEX IF NOT EXISTS idx_tasks_user_id ON tasks(user_id)');
  } catch (e) {
    // Индексы могут уже существовать
  }
}

// Сохранение базы данных в файл
function saveDatabase() {
  if (!db) return;
  try {
    const data = db.export();
    const buffer = Buffer.from(data);
    fs.writeFileSync(dbFile, buffer);
  } catch (error) {
    console.error('Ошибка сохранения БД:', error);
  }
}

// Очистка устаревших сессий и токенов
function cleanupExpiredSessions() {
  if (!db) return;
  const now = new Date().toISOString();
  try {
    const stmt1 = db.prepare('DELETE FROM csrf_tokens WHERE expires_at < ?');
    stmt1.bind([now]);
    stmt1.step();
    stmt1.free();
    
    const stmt2 = db.prepare('DELETE FROM sessions WHERE expires_at < ?');
    stmt2.bind([now]);
    stmt2.step();
    stmt2.free();
    
    saveDatabase();
  } catch (e) {
    // Игнорируем ошибки при очистке
    console.error('Ошибка очистки сессий:', e);
  }
}

// Обёртка для совместимости с better-sqlite3 API
const dbWrapper = {
  prepare: (sql) => {
    if (!db) {
      throw new Error('База данных не инициализирована');
    }
    
    const stmt = db.prepare(sql);
    
    return {
      run: (...params) => {
        try {
          if (params.length > 0) {
            // Фильтруем undefined значения
            const filteredParams = params.filter(p => p !== undefined);
            if (filteredParams.length > 0) {
              stmt.bind(filteredParams);
            }
          }
          stmt.step();
          
          // Получаем lastInsertRowid сразу после выполнения
          let lastInsertRowid = 0;
          try {
            const lastIdStmt = db.prepare('SELECT last_insert_rowid() as id');
            if (lastIdStmt.step()) {
              const row = lastIdStmt.getAsObject({});
              lastInsertRowid = parseInt(row.id) || 0;
            }
            lastIdStmt.free();
          } catch (e) {
            // Игнорируем ошибки получения lastInsertRowid
            console.error('Ошибка получения lastInsertRowid:', e);
          }
          
          stmt.reset();
          saveDatabase();
          
          return { 
            lastInsertRowid: lastInsertRowid,
            changes: 1 // sql.js не возвращает точное количество изменений
          };
        } catch (error) {
          stmt.reset();
          console.error('Ошибка выполнения запроса:', error, 'SQL:', sql, 'Params:', params);
          throw error;
        }
      },
      get: (...params) => {
        try {
          if (params.length > 0) {
            // Фильтруем undefined значения
            const filteredParams = params.filter(p => p !== undefined);
            if (filteredParams.length > 0) {
              stmt.bind(filteredParams);
            }
          }
          const hasRow = stmt.step();
          if (!hasRow) {
            stmt.reset();
            return null;
          }
          
          // Получаем имена колонок
          const columnNames = stmt.getColumnNames();
          // Получаем значения
          const values = stmt.get();
          
          // Создаём объект из колонок и значений
          const result = {};
          for (let i = 0; i < columnNames.length; i++) {
            result[columnNames[i]] = values[i];
          }
          
          stmt.reset();
          return result;
        } catch (error) {
          stmt.reset();
          console.error('Ошибка получения данных:', error, 'SQL:', sql, 'Params:', params);
          throw error;
        }
      },
      all: (...params) => {
        try {
          if (params.length > 0) {
            // Фильтруем undefined значения
            const filteredParams = params.filter(p => p !== undefined);
            if (filteredParams.length > 0) {
              stmt.bind(filteredParams);
            }
          }
          
          // Получаем имена колонок один раз
          const columnNames = stmt.getColumnNames();
          const results = [];
          
          while (stmt.step()) {
            // Получаем значения
            const values = stmt.get();
            // Создаём объект из колонок и значений
            const row = {};
            for (let i = 0; i < columnNames.length; i++) {
              row[columnNames[i]] = values[i];
            }
            results.push(row);
          }
          
          stmt.reset();
          return results;
        } catch (error) {
          stmt.reset();
          console.error('Ошибка получения всех данных:', error, 'SQL:', sql, 'Params:', params);
          throw error;
        }
      }
    };
  },
  exec: (sql) => {
    if (!db) {
      throw new Error('База данных не инициализирована');
    }
    db.run(sql);
    saveDatabase();
  }
};

// Экспортируем обёртку и функцию инициализации
module.exports = {
  get db() {
    return dbWrapper;
  },
  initDatabase,
  saveDatabase
};
