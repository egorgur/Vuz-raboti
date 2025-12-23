// routes/auth.js
const express = require('express');
const bcrypt = require('bcrypt');
const { db } = require('../database');
const { createSession, createSignedCookie, deleteSession, verifySignedCookie, getSession } = require('../security/session');
const { createToken } = require('../security/csrf');
const { validateUsername, validatePassword } = require('../security/validation');
const { initKeyExchange, completeKeyExchange, decryptData } = require('../security/diffie-hellman');

const router = express.Router();

/**
 * Инициализация обмена ключами Диффи-Хеллмана
 */
router.get('/key-exchange', (req, res) => {
  try {
    const keyData = initKeyExchange();
    res.json(keyData);
  } catch (error) {
    console.error('Ошибка инициализации обмена ключами:', error);
    res.status(500).json({ error: 'Ошибка инициализации обмена ключами' });
  }
});

/**
 * Регистрация нового пользователя (с защитой Диффи-Хеллмана)
 */
router.post('/register', async (req, res) => {
  try {
    let username, password;
    
    // Проверяем, используется ли защищённый канал (Диффи-Хеллман)
    if (req.body.exchangeId && req.body.clientPublicKey && req.body.encryptedData) {
      // Расшифровываем данные
      try {
        const encryptionKey = completeKeyExchange(req.body.exchangeId, req.body.clientPublicKey);
        const decryptedJson = decryptData(
          req.body.encryptedData.encrypted,
          req.body.encryptedData.iv,
          req.body.encryptedData.authTag,
          encryptionKey
        );
        const decryptedData = JSON.parse(decryptedJson);
        username = decryptedData.username;
        password = decryptedData.password;
      } catch (dhError) {
        console.error('Ошибка расшифровки:', dhError);
        return res.status(400).json({ error: 'Ошибка расшифровки данных' });
      }
    } else {
      // Обычный режим (для обратной совместимости - НЕ РЕКОМЕНДУЕТСЯ)
      username = req.body.username;
      password = req.body.password;
    }
    
    // Валидация входных данных
    const usernameValidation = validateUsername(username);
    if (!usernameValidation.valid) {
      return res.status(400).json({ error: usernameValidation.error });
    }
    
    const passwordValidation = validatePassword(password);
    if (!passwordValidation.valid) {
      return res.status(400).json({ error: passwordValidation.error });
    }
    
    username = usernameValidation.value;
    password = passwordValidation.value;
    
    // Проверка существования пользователя
    const existing = db.prepare('SELECT id FROM users WHERE username = ?').get(username);
    if (existing) {
      return res.status(409).json({ error: 'Пользователь с таким именем уже существует' });
    }
    
    // Хеширование пароля
    const saltRounds = 10;
    const passwordHash = await bcrypt.hash(password, saltRounds);
    
    // Создание пользователя (по умолчанию роль 'user')
    let result;
    try {
      result = db.prepare(`
        INSERT INTO users (username, password_hash, role)
        VALUES (?, ?, 'user')
      `).run(username, passwordHash);
    } catch (dbError) {
      console.error('Ошибка БД при создании пользователя:', dbError);
      throw dbError;
    }
    
    // Получаем ID созданного пользователя
    let userId = result.lastInsertRowid;
    if (!userId || userId === 0) {
      // Если lastInsertRowid не сработал, получаем ID через запрос
      const newUser = db.prepare('SELECT id FROM users WHERE username = ?').get(username);
      if (!newUser) {
        return res.status(500).json({ error: 'Ошибка создания пользователя' });
      }
      userId = newUser.id || newUser['id'] || parseInt(newUser.id);
      if (!userId) {
        return res.status(500).json({ error: 'Ошибка получения ID пользователя' });
      }
    }
    
    console.log('Создан пользователь с ID:', userId);
    
    // Автоматический вход после регистрации
    const sessionId = createSession(userId);
    const signedCookie = createSignedCookie(sessionId);
    const csrfToken = createToken(sessionId);
    
    res.cookie('session', signedCookie, {
      httpOnly: true,
      secure: false, // В продакшене должно быть true для HTTPS
      sameSite: 'strict',
      maxAge: 30 * 60 * 1000 // 30 минут
    });
    
    res.status(201).json({
      message: 'Регистрация успешна',
      user: {
        id: userId,
        username: username,
        role: 'user'
      },
      csrf_token: csrfToken
    });
  } catch (error) {
    console.error('Ошибка регистрации:', error);
    res.status(500).json({ error: 'Внутренняя ошибка сервера' });
  }
});

/**
 * Вход в систему (с защитой Диффи-Хеллмана)
 */
router.post('/login', async (req, res) => {
  try {
    let username, password;
    
    // Проверяем, используется ли защищённый канал (Диффи-Хеллман)
    if (req.body.exchangeId && req.body.clientPublicKey && req.body.encryptedData) {
      // Расшифровываем данные
      try {
        const encryptionKey = completeKeyExchange(req.body.exchangeId, req.body.clientPublicKey);
        const decryptedJson = decryptData(
          req.body.encryptedData.encrypted,
          req.body.encryptedData.iv,
          req.body.encryptedData.authTag,
          encryptionKey
        );
        const decryptedData = JSON.parse(decryptedJson);
        username = decryptedData.username;
        password = decryptedData.password;
      } catch (dhError) {
        console.error('Ошибка расшифровки:', dhError);
        return res.status(400).json({ error: 'Ошибка расшифровки данных' });
      }
    } else {
      // Обычный режим (для обратной совместимости - НЕ РЕКОМЕНДУЕТСЯ)
      username = req.body.username;
      password = req.body.password;
    }
    
    const usernameValidation = validateUsername(username);
    if (!usernameValidation.valid) {
      return res.status(400).json({ error: usernameValidation.error });
    }
    
    const passwordValidation = validatePassword(password);
    if (!passwordValidation.valid) {
      return res.status(400).json({ error: passwordValidation.error });
    }
    
    username = usernameValidation.value;
    password = passwordValidation.value;
    
    // Поиск пользователя
    const user = db.prepare('SELECT * FROM users WHERE username = ?').get(username);
    
    if (!user) {
      // Задержка для защиты от timing attacks
      await bcrypt.hash(password, 10);
      return res.status(401).json({ error: 'Неверное имя пользователя или пароль' });
    }
    
    // Получаем password_hash (может быть в разных форматах)
    const passwordHash = user.password_hash || user['password_hash'];
    const userId = user.id || user['id'];
    
    if (!passwordHash) {
      console.error('Ошибка: password_hash не найден для пользователя:', user);
      return res.status(500).json({ error: 'Ошибка базы данных' });
    }
    
    // Проверка пароля
    const passwordMatch = await bcrypt.compare(password, passwordHash);
    
    if (!passwordMatch) {
      return res.status(401).json({ error: 'Неверное имя пользователя или пароль' });
    }
    
    // Получаем остальные поля
    const userRole = user.role || user['role'];
    const userUsername = user.username || user['username'];
    
    // Создание сессии
    const sessionId = createSession(userId);
    const signedCookie = createSignedCookie(sessionId);
    const csrfToken = createToken(sessionId);
    
    res.cookie('session', signedCookie, {
      httpOnly: true,
      secure: false, // В продакшене должно быть true для HTTPS
      sameSite: 'strict',
      maxAge: 30 * 60 * 1000
    });
    
    res.json({
      message: 'Вход выполнен успешно',
      user: {
        id: userId,
        username: userUsername,
        role: userRole
      },
      csrf_token: csrfToken
    });
  } catch (error) {
    console.error('Ошибка входа:', error);
    res.status(500).json({ error: 'Внутренняя ошибка сервера' });
  }
});

/**
 * Выход из системы
 */
router.post('/logout', (req, res) => {
  const sessionCookie = req.cookies?.session;
  
  if (sessionCookie) {
    const sessionId = verifySignedCookie(sessionCookie);
    if (sessionId) {
      deleteSession(sessionId);
    }
  }
  
  res.clearCookie('session');
  res.json({ message: 'Выход выполнен успешно' });
});

/**
 * Получение текущего пользователя
 */
router.get('/me', (req, res) => {
  const sessionCookie = req.cookies?.session;
  
  if (!sessionCookie) {
    return res.status(401).json({ error: 'Не аутентифицирован' });
  }
  
  const sessionId = verifySignedCookie(sessionCookie);
  
  if (!sessionId) {
    return res.status(401).json({ error: 'Недействительная сессия' });
  }
  
  const session = getSession(sessionId);
  
  if (!session) {
    return res.status(401).json({ error: 'Сессия истекла' });
  }
  
  res.json({
    user: {
      id: session.user_id,
      username: session.username,
      role: session.role
    }
  });
});

/**
 * Получение нового CSRF токена
 */
router.get('/csrf-token', (req, res) => {
  const sessionCookie = req.cookies?.session;
  
  if (!sessionCookie) {
    return res.status(401).json({ error: 'Требуется аутентификация' });
  }
  
  const sessionId = verifySignedCookie(sessionCookie);
  
  if (!sessionId) {
    return res.status(401).json({ error: 'Недействительная сессия' });
  }
  
  const session = getSession(sessionId);
  
  if (!session) {
    return res.status(401).json({ error: 'Сессия истекла' });
  }
  
  const csrfToken = createToken(sessionId);
  res.json({ csrf_token: csrfToken });
});

module.exports = router;

