// security/session.js
const crypto = require('crypto');
const { db } = require('../database');

// Секретный ключ для HMAC (в продакшене должен быть в переменных окружения)
const HMAC_SECRET = process.env.HMAC_SECRET || crypto.randomBytes(32).toString('hex');

// Время жизни сессии (30 минут)
const SESSION_DURATION = 30 * 60 * 1000;

/**
 * Создание новой сессии для пользователя
 */
function createSession(userId) {
  const sessionId = crypto.randomBytes(32).toString('hex');
  const expiresAt = new Date(Date.now() + SESSION_DURATION).toISOString();
  
  db.prepare(`
    INSERT INTO sessions (id, user_id, expires_at)
    VALUES (?, ?, ?)
  `).run(sessionId, userId, expiresAt);
  
  return sessionId;
}

/**
 * Проверка и получение данных сессии
 */
function getSession(sessionId) {
  if (!sessionId) return null;
  
  try {
    const session = db.prepare(`
      SELECT s.*, u.username, u.role
      FROM sessions s
      JOIN users u ON s.user_id = u.id
      WHERE s.id = ? AND s.expires_at > datetime('now')
    `).get(sessionId);
    
    return session || null;
  } catch (error) {
    console.error('Ошибка получения сессии:', error);
    return null;
  }
}

/**
 * Удаление сессии
 */
function deleteSession(sessionId) {
  if (!sessionId) return;
  
  db.prepare('DELETE FROM sessions WHERE id = ?').run(sessionId);
  // Также удаляем все CSRF токены этой сессии
  db.prepare('DELETE FROM csrf_tokens WHERE session_id = ?').run(sessionId);
}

/**
 * Обновление времени жизни сессии
 */
function refreshSession(sessionId) {
  if (!sessionId) return;
  
  const expiresAt = new Date(Date.now() + SESSION_DURATION).toISOString();
  db.prepare('UPDATE sessions SET expires_at = ? WHERE id = ?').run(expiresAt, sessionId);
}

/**
 * Создание подписанной cookie с HMAC
 */
function createSignedCookie(value) {
  const hmac = crypto.createHmac('sha256', HMAC_SECRET);
  hmac.update(value);
  const signature = hmac.digest('hex');
  return `${value}.${signature}`;
}

/**
 * Проверка подписи cookie
 */
function verifySignedCookie(signedValue) {
  if (!signedValue || typeof signedValue !== 'string') return null;
  
  const parts = signedValue.split('.');
  if (parts.length !== 2) return null;
  
  const [value, signature] = parts;
  const hmac = crypto.createHmac('sha256', HMAC_SECRET);
  hmac.update(value);
  const expectedSignature = hmac.digest('hex');
  
  // Защита от timing attacks через crypto.timingSafeEqual
  if (signature.length !== expectedSignature.length) return null;
  
  try {
    if (crypto.timingSafeEqual(Buffer.from(signature), Buffer.from(expectedSignature))) {
      return value;
    }
  } catch (e) {
    return null;
  }
  
  return null;
}

/**
 * Middleware для проверки аутентификации
 */
function requireAuth(req, res, next) {
  const sessionCookie = req.cookies?.session;
  
  if (!sessionCookie) {
    return res.status(401).json({ error: 'Требуется аутентификация' });
  }
  
  const sessionId = verifySignedCookie(sessionCookie);
  if (!sessionId) {
    res.clearCookie('session');
    return res.status(401).json({ error: 'Недействительная сессия' });
  }
  
  const session = getSession(sessionId);
  if (!session) {
    res.clearCookie('session');
    return res.status(401).json({ error: 'Сессия истекла' });
  }
  
  // Обновляем время жизни сессии при каждом запросе
  refreshSession(sessionId);
  
  // Получаем поля из сессии (sql.js возвращает данные в правильном формате после исправления)
  const userId = session.user_id;
  const username = session.username;
  const role = session.role;
  
  if (!userId) {
    console.error('Ошибка: user_id не найден в сессии:', session);
    res.clearCookie('session');
    return res.status(401).json({ error: 'Недействительная сессия' });
  }
  
  // Добавляем данные пользователя в запрос
  req.user = {
    id: userId,
    username: username,
    role: role,
    sessionId: sessionId
  };
  
  next();
}

/**
 * Middleware для проверки роли
 */
function requireRole(...allowedRoles) {
  return (req, res, next) => {
    if (!req.user) {
      return res.status(401).json({ error: 'Требуется аутентификация' });
    }
    
    if (!allowedRoles.includes(req.user.role)) {
      return res.status(403).json({ error: 'Недостаточно прав доступа' });
    }
    
    next();
  };
}

module.exports = {
  createSession,
  getSession,
  deleteSession,
  refreshSession,
  createSignedCookie,
  verifySignedCookie,
  requireAuth,
  requireRole,
  SESSION_DURATION
};

