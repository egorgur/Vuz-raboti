// security/validation.js
/**
 * Валидация и санитизация входных данных
 */

/**
 * Проверка username
 */
function validateUsername(username) {
  if (!username || typeof username !== 'string') {
    return { valid: false, error: 'Имя пользователя обязательно' };
  }
  
  const trimmed = username.trim();
  
  if (trimmed.length < 3 || trimmed.length > 20) {
    return { valid: false, error: 'Имя пользователя должно быть от 3 до 20 символов' };
  }
  
  if (!/^[a-zA-Z0-9_]+$/.test(trimmed)) {
    return { valid: false, error: 'Имя пользователя может содержать только буквы, цифры и подчёркивание' };
  }
  
  return { valid: true, value: trimmed };
}

/**
 * Проверка password
 */
function validatePassword(password) {
  if (!password || typeof password !== 'string') {
    return { valid: false, error: 'Пароль обязателен' };
  }
  
  if (password.length < 6) {
    return { valid: false, error: 'Пароль должен содержать минимум 6 символов' };
  }
  
  if (password.length > 100) {
    return { valid: false, error: 'Пароль слишком длинный' };
  }
  
  return { valid: true, value: password };
}

/**
 * Санитизация строки (защита от XSS)
 */
function sanitizeString(str) {
  if (typeof str !== 'string') return '';
  
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#x27;')
    .replace(/\//g, '&#x2F;')
    .trim();
}

/**
 * Санитизация для HTML (менее агрессивная, для отображения)
 */
function sanitizeHTML(str) {
  if (typeof str !== 'string') return '';
  
  // Разрешаем только безопасные символы
  return str
    .replace(/[<>]/g, '') // Удаляем угловые скобки
    .trim();
}

/**
 * Валидация задачи
 */
function validateTask(title, description) {
  if (!title || typeof title !== 'string') {
    return { valid: false, error: 'Название задачи обязательно' };
  }
  
  const sanitizedTitle = sanitizeHTML(title.trim());
  
  if (sanitizedTitle.length === 0) {
    return { valid: false, error: 'Название задачи не может быть пустым' };
  }
  
  if (sanitizedTitle.length > 200) {
    return { valid: false, error: 'Название задачи слишком длинное' };
  }
  
  const sanitizedDesc = description ? sanitizeHTML(description.trim()) : '';
  
  if (sanitizedDesc.length > 1000) {
    return { valid: false, error: 'Описание задачи слишком длинное' };
  }
  
  return {
    valid: true,
    value: {
      title: sanitizedTitle,
      description: sanitizedDesc
    }
  };
}

/**
 * Защита от SQL injection через параметризованные запросы
 * (better-sqlite3 уже использует параметризованные запросы, но для явности)
 */
function validateId(id) {
  const numId = parseInt(id, 10);
  if (isNaN(numId) || numId <= 0) {
    return { valid: false, error: 'Недействительный ID' };
  }
  return { valid: true, value: numId };
}

module.exports = {
  validateUsername,
  validatePassword,
  sanitizeString,
  sanitizeHTML,
  validateTask,
  validateId
};

