// server.js
const express = require('express');
const cookieParser = require('cookie-parser');
const path = require('path');
const { initDatabase } = require('./database');
const authRoutes = require('./routes/auth');
const taskRoutes = require('./routes/tasks');

const app = express();
const PORT = process.env.PORT || 3000;

// Флаг готовности БД
let dbReady = false;

// Middleware
app.use(express.json({ limit: '10mb' })); // Ограничение размера тела запроса
app.use(express.urlencoded({ extended: true, limit: '10mb' }));
app.use(cookieParser());

// Защита от некоторых атак через заголовки
app.use((req, res, next) => {
  // Защита от XSS
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('X-Frame-Options', 'DENY');
  res.setHeader('X-XSS-Protection', '1; mode=block');
  
  // Удаление информации о сервере
  res.removeHeader('X-Powered-By');
  
  next();
});

// Простой rate limiting (базовая защита от брутфорса)
const rateLimitMap = new Map();
const RATE_LIMIT_WINDOW = 15 * 60 * 1000; // 15 минут
const RATE_LIMIT_MAX_REQUESTS = 100; // максимум запросов

app.use((req, res, next) => {
  const ip = req.ip || req.connection.remoteAddress;
  const now = Date.now();
  
  if (!rateLimitMap.has(ip)) {
    rateLimitMap.set(ip, { count: 1, resetTime: now + RATE_LIMIT_WINDOW });
    return next();
  }
  
  const limit = rateLimitMap.get(ip);
  
  if (now > limit.resetTime) {
    limit.count = 1;
    limit.resetTime = now + RATE_LIMIT_WINDOW;
    return next();
  }
  
  if (limit.count >= RATE_LIMIT_MAX_REQUESTS) {
    return res.status(429).json({ error: 'Слишком много запросов. Попробуйте позже.' });
  }
  
  limit.count++;
  next();
});

// Очистка старых записей rate limiting
setInterval(() => {
  const now = Date.now();
  for (const [ip, limit] of rateLimitMap.entries()) {
    if (now > limit.resetTime) {
      rateLimitMap.delete(ip);
    }
  }
}, RATE_LIMIT_WINDOW);

// Статические файлы (клиентская часть)
app.use(express.static(path.join(__dirname, 'public')));

// Middleware для проверки готовности БД
// Должен быть ПЕРЕД регистрацией API маршрутов, чтобы защитить их во время запуска
app.use((req, res, next) => {
  if (!dbReady && req.path.startsWith('/api')) {
    return res.status(503).json({ error: 'База данных не готова. Подождите...' });
  }
  next();
});

// API маршруты
app.use('/api/auth', authRoutes);
app.use('/api/tasks', taskRoutes);

// Главная страница
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Обработка 404
app.use((req, res) => {
  res.status(404).json({ error: 'Страница не найдена' });
});

// Обработка ошибок
app.use((err, req, res, next) => {
  console.error('Ошибка сервера:', err);
  res.status(500).json({ error: 'Внутренняя ошибка сервера' });
});

// Инициализация базы данных и запуск сервера
initDatabase().then(() => {
  dbReady = true;
  console.log('База данных инициализирована');
  
  // Запуск сервера только после инициализации БД
  app.listen(PORT, () => {
    console.log(`Сервер запущен на http://localhost:${PORT}`);
  });
}).catch((error) => {
  console.error('Ошибка инициализации БД:', error);
  process.exit(1);
});

