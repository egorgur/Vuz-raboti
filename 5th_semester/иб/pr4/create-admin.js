const bcrypt = require('bcrypt');
const { initDatabase, db } = require('./database');
const readline = require('readline');

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

async function createAdmin() {
  // Инициализируем БД
  await initDatabase();
  
  rl.question('Введите имя пользователя для администратора: ', async (username) => {
    if (!username || username.trim().length < 3) {
      console.error('Имя пользователя должно содержать минимум 3 символа');
      rl.close();
      process.exit(1);
    }
    
    rl.question('Введите пароль: ', async (password) => {
      if (!password || password.length < 6) {
        console.error('Пароль должен содержать минимум 6 символов');
        rl.close();
        process.exit(1);
      }
      
      try {
        // Проверка существования пользователя
        const existing = db.prepare('SELECT id FROM users WHERE username = ?').get(username.trim());
        if (existing) {
          console.error('Пользователь с таким именем уже существует');
          rl.close();
          process.exit(1);
        }
        
        // Хеширование пароля
        const saltRounds = 10;
        const passwordHash = await bcrypt.hash(password, saltRounds);
        
        // Создание администратора
        const result = db.prepare(`
          INSERT INTO users (username, password_hash, role)
          VALUES (?, ?, 'admin')
        `).run(username.trim(), passwordHash);
        
        console.log(`Администратор успешно создан! ID: ${result.lastInsertRowid}`);
        console.log(`Имя пользователя: ${username.trim()}`);
        console.log('Роль: admin');
        
      } catch (error) {
        console.error('Ошибка создания администратора:', error);
      } finally {
        rl.close();
        process.exit(0);
      }
    });
  });
}

// Запуск
createAdmin().catch((error) => {
  console.error('Ошибка инициализации:', error);
  console.error('Убедитесь, что база данных инициализирована. Запустите сервер (npm start) хотя бы один раз.');
  rl.close();
  process.exit(1);
});
