// security/csrf.js
const crypto = require('crypto');
const { db } = require('../database');

// Время жизни CSRF токена (1 час)
const CSRF_TOKEN_DURATION = 60 * 60 * 1000;

/**
 * Генерация CSRF токена
 */
function generateToken() {
  return crypto.randomBytes(32).toString('hex');
}

/**
 * Создание и сохранение CSRF токена для сессии
 */
function createToken(sessionId) {
  const token = generateToken();
  const expiresAt = new Date(Date.now() + CSRF_TOKEN_DURATION).toISOString();
  
  db.prepare(`
    INSERT INTO csrf_tokens (token, session_id, expires_at)
    VALUES (?, ?, ?)
  `).run(token, sessionId, expiresAt);
  
  return token;
}

/**
 * Проверка CSRF токена
 */
function verifyToken(token, sessionId) {
  if (!token || !sessionId) return false;
  
  const stored = db.prepare(`
    SELECT * FROM csrf_tokens
    WHERE token = ? AND session_id = ? AND expires_at > datetime('now')
  `).get(token, sessionId);
  
  return !!stored;
}

/**
 * Удаление использованного токена (опционально, для одноразовых токенов)
 */
function deleteToken(token) {
  db.prepare('DELETE FROM csrf_tokens WHERE token = ?').run(token);
}

/**
 * Middleware для проверки CSRF токена
 * Для GET запросов токен не требуется, для POST/PUT/DELETE - обязателен
 */
function csrfProtection(req, res, next) {
  // GET запросы не требуют CSRF защиты
  if (req.method === 'GET' || req.method === 'HEAD' || req.method === 'OPTIONS') {
    return next();
  }
  
  // Для аутентифицированных пользователей проверяем токен
  if (req.user) {
    const token = req.headers['x-csrf-token'] || req.body?.csrf_token;
    
    if (!token) {
      return res.status(403).json({ error: 'CSRF токен отсутствует' });
    }
    
    if (!verifyToken(token, req.user.sessionId)) {
      return res.status(403).json({ error: 'Недействительный CSRF токен' });
    }
    
    // Удаляем использованный токен (одноразовый)
    deleteToken(token);
  }
  
  next();
}

module.exports = {
  createToken,
  verifyToken,
  deleteToken,
  csrfProtection
};

