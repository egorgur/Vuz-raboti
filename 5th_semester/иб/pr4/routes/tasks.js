// routes/tasks.js
const express = require('express');
const { db } = require('../database');
const { requireAuth, requireRole } = require('../security/session');
const { csrfProtection } = require('../security/csrf');
const { validateTask, validateId } = require('../security/validation');

const router = express.Router();

// Все маршруты требуют аутентификации
router.use(requireAuth);
router.use(csrfProtection);

/**
 * Получение всех задач пользователя
 */
router.get('/', (req, res) => {
  try {
    const tasks = db.prepare(`
      SELECT id, title, description, completed, created_at, updated_at
      FROM tasks
      WHERE user_id = ?
      ORDER BY created_at DESC
    `).all(req.user.id);
    
    res.json({ tasks });
  } catch (error) {
    console.error('Ошибка получения задач:', error);
    res.status(500).json({ error: 'Внутренняя ошибка сервера' });
  }
});

/**
 * Получение всех задач (только для администраторов)
 * Должен быть определён ПЕРЕД /:id, чтобы Express правильно обрабатывал маршрут
 */
router.get('/admin/all', requireRole('admin'), (req, res) => {
  try {
    const usernameFilter = req.query.username || '';
    const taskTitleFilter = req.query.task || '';
    
    let query = `
      SELECT t.id, t.title, t.description, t.completed, t.created_at, t.updated_at,
             u.username, u.id as user_id
      FROM tasks t
      JOIN users u ON t.user_id = u.id
      WHERE 1=1
    `;
    const params = [];
    
    // Фильтр по имени пользователя
    if (usernameFilter.trim()) {
      query += ' AND u.username LIKE ?';
      params.push(`%${usernameFilter.trim()}%`);
    }
    
    // Фильтр по названию задачи
    if (taskTitleFilter.trim()) {
      query += ' AND t.title LIKE ?';
      params.push(`%${taskTitleFilter.trim()}%`);
    }
    
    query += ' ORDER BY t.created_at DESC';
    
    const tasks = db.prepare(query).all(...params);
    
    res.json({ tasks });
  } catch (error) {
    console.error('Ошибка получения всех задач:', error);
    res.status(500).json({ error: 'Внутренняя ошибка сервера' });
  }
});

/**
 * Получение задачи по ID
 */
router.get('/:id', (req, res) => {
  try {
    const idValidation = validateId(req.params.id);
    if (!idValidation.valid) {
      return res.status(400).json({ error: idValidation.error });
    }
    
    // Получаем задачу с информацией о владельце
    const task = db.prepare(`
      SELECT id, title, description, completed, created_at, updated_at, user_id
      FROM tasks
      WHERE id = ?
    `).get(idValidation.value);
    
    if (!task) {
      return res.status(404).json({ error: 'Задача не найдена' });
    }
    
    // Проверка прав: администратор может просматривать любые задачи, обычный пользователь - только свои
    if (req.user.role !== 'admin' && task.user_id !== req.user.id) {
      return res.status(403).json({ error: 'Недостаточно прав для просмотра этой задачи' });
    }
    
    // Удаляем user_id из ответа (не нужен клиенту)
    delete task.user_id;
    
    res.json({ task });
  } catch (error) {
    console.error('Ошибка получения задачи:', error);
    res.status(500).json({ error: 'Внутренняя ошибка сервера' });
  }
});

/**
 * Создание новой задачи
 */
router.post('/', (req, res) => {
  try {
    const taskValidation = validateTask(req.body.title, req.body.description);
    if (!taskValidation.valid) {
      return res.status(400).json({ error: taskValidation.error });
    }
    
    const { title, description } = taskValidation.value;
    
    // Получаем статус выполнения (если передан)
    const completed = req.body.completed ? 1 : 0;
    
    const result = db.prepare(`
      INSERT INTO tasks (user_id, title, description, completed)
      VALUES (?, ?, ?, ?)
    `).run(req.user.id, title, description, completed);
    
    const task = db.prepare(`
      SELECT id, title, description, completed, created_at, updated_at
      FROM tasks
      WHERE id = ?
    `).get(result.lastInsertRowid);
    
    res.status(201).json({ task });
  } catch (error) {
    console.error('Ошибка создания задачи:', error);
    res.status(500).json({ error: 'Внутренняя ошибка сервера' });
  }
});

/**
 * Обновление задачи
 */
router.put('/:id', (req, res) => {
  try {
    const idValidation = validateId(req.params.id);
    if (!idValidation.valid) {
      return res.status(400).json({ error: idValidation.error });
    }
    
    // Проверка существования задачи
    const existing = db.prepare('SELECT id, user_id FROM tasks WHERE id = ?').get(idValidation.value);
    
    if (!existing) {
      return res.status(404).json({ error: 'Задача не найдена' });
    }
    
    // Проверка прав: администратор может редактировать любые задачи, обычный пользователь - только свои
    if (req.user.role !== 'admin' && existing.user_id !== req.user.id) {
      return res.status(403).json({ error: 'Недостаточно прав для редактирования этой задачи' });
    }
    
    // Валидация обновляемых данных
    const updates = {};
    if (req.body.title !== undefined) {
      const taskValidation = validateTask(req.body.title, req.body.description);
      if (!taskValidation.valid) {
        return res.status(400).json({ error: taskValidation.error });
      }
      updates.title = taskValidation.value.title;
      updates.description = taskValidation.value.description;
    }
    
    if (req.body.completed !== undefined) {
      updates.completed = req.body.completed ? 1 : 0;
    }
    
    // Проверка, что есть хотя бы одно поле для обновления
    if (Object.keys(updates).length === 0) {
      return res.status(400).json({ error: 'Не указаны поля для обновления' });
    }
    
    // Обновление задачи (для администратора не проверяем user_id в WHERE)
    const setClause = Object.keys(updates).map(key => `${key} = ?`).join(', ');
    const values = [...Object.values(updates), idValidation.value];
    
    db.prepare(`
      UPDATE tasks
      SET ${setClause}, updated_at = CURRENT_TIMESTAMP
      WHERE id = ?
    `).run(...values);
    
    const task = db.prepare(`
      SELECT id, title, description, completed, created_at, updated_at
      FROM tasks
      WHERE id = ?
    `).get(idValidation.value);
    
    res.json({ task });
  } catch (error) {
    console.error('Ошибка обновления задачи:', error);
    res.status(500).json({ error: 'Внутренняя ошибка сервера' });
  }
});

/**
 * Удаление задачи
 */
router.delete('/:id', (req, res) => {
  try {
    const idValidation = validateId(req.params.id);
    if (!idValidation.valid) {
      return res.status(400).json({ error: idValidation.error });
    }
    
    // Проверка существования задачи
    const task = db.prepare('SELECT id, user_id FROM tasks WHERE id = ?').get(idValidation.value);
    
    if (!task) {
      return res.status(404).json({ error: 'Задача не найдена' });
    }
    
    // Проверка прав: администратор может удалять любые задачи, обычный пользователь - только свои
    if (req.user.role !== 'admin' && task.user_id !== req.user.id) {
      return res.status(403).json({ error: 'Недостаточно прав для удаления этой задачи' });
    }
    
    // Удаление задачи
    const result = db.prepare('DELETE FROM tasks WHERE id = ?').run(idValidation.value);
    
    if (result.changes === 0) {
      return res.status(404).json({ error: 'Задача не найдена' });
    }
    
    res.json({ message: 'Задача удалена' });
  } catch (error) {
    console.error('Ошибка удаления задачи:', error);
    res.status(500).json({ error: 'Внутренняя ошибка сервера' });
  }
});

module.exports = router;

