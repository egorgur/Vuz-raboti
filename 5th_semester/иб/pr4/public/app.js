// app.js
// Глобальное состояние приложения
let currentUser = null;
let csrfToken = null;
let isAdminView = false;

// ============================================
// Модуль Диффи-Хеллмана для безопасной передачи данных
// ============================================

/**
 * Модульное возведение в степень (a^b mod m) для BigInt
 */
function modPow(base, exponent, modulus) {
  if (modulus === BigInt(1)) return BigInt(0);
  
  let result = BigInt(1);
  base = base % modulus;
  
  while (exponent > BigInt(0)) {
    if (exponent % BigInt(2) === BigInt(1)) {
      result = (result * base) % modulus;
    }
    exponent = exponent / BigInt(2);
    base = (base * base) % modulus;
  }
  
  return result;
}

/**
 * Генерация случайного приватного ключа (256 бит)
 */
function generatePrivateKey() {
  const array = new Uint8Array(32);
  crypto.getRandomValues(array);
  return BigInt('0x' + Array.from(array).map(b => b.toString(16).padStart(2, '0')).join(''));
}

/**
 * Вычисление публичного ключа: A = g^a mod p
 */
function computePublicKey(privateKey, g, p) {
  return modPow(g, privateKey, p);
}

/**
 * Вычисление общего секрета: K = B^a mod p
 */
function computeSharedSecret(otherPublicKey, privateKey, p) {
  return modPow(otherPublicKey, privateKey, p);
}

/**
 * Преобразование общего секрета в ключ шифрования через SHA-256
 */
async function deriveEncryptionKey(sharedSecret) {
  const secretHex = sharedSecret.toString(16).padStart(512, '0');
  const secretBytes = new Uint8Array(secretHex.match(/.{2}/g).map(byte => parseInt(byte, 16)));
  const hashBuffer = await crypto.subtle.digest('SHA-256', secretBytes);
  return new Uint8Array(hashBuffer);
}

/**
 * Шифрование данных AES-256-GCM
 */
async function encryptData(data, keyBytes) {
  const key = await crypto.subtle.importKey(
    'raw',
    keyBytes,
    { name: 'AES-GCM' },
    false,
    ['encrypt']
  );
  
  const iv = crypto.getRandomValues(new Uint8Array(12));
  const encodedData = new TextEncoder().encode(data);
  
  const encryptedBuffer = await crypto.subtle.encrypt(
    { name: 'AES-GCM', iv: iv },
    key,
    encodedData
  );
  
  // Последние 16 байт - это authTag
  const encryptedArray = new Uint8Array(encryptedBuffer);
  const encrypted = encryptedArray.slice(0, -16);
  const authTag = encryptedArray.slice(-16);
  
  return {
    encrypted: Array.from(encrypted).map(b => b.toString(16).padStart(2, '0')).join(''),
    iv: Array.from(iv).map(b => b.toString(16).padStart(2, '0')).join(''),
    authTag: Array.from(authTag).map(b => b.toString(16).padStart(2, '0')).join('')
  };
}

/**
 * Безопасная отправка данных аутентификации через Диффи-Хеллман
 */
async function secureAuthRequest(endpoint, credentials) {
  // 1. Получаем параметры DH от сервера
  const keyExchangeResponse = await fetch('/api/auth/key-exchange');
  const keyData = await keyExchangeResponse.json();
  
  const p = BigInt('0x' + keyData.p);
  const g = BigInt(keyData.g);
  const serverPublicKey = BigInt('0x' + keyData.serverPublicKey);
  
  // 2. Генерируем свой приватный ключ
  const clientPrivateKey = generatePrivateKey();
  
  // 3. Вычисляем публичный ключ клиента
  const clientPublicKey = computePublicKey(clientPrivateKey, g, p);
  
  // 4. Вычисляем общий секрет
  const sharedSecret = computeSharedSecret(serverPublicKey, clientPrivateKey, p);
  
  // 5. Получаем ключ шифрования
  const encryptionKey = await deriveEncryptionKey(sharedSecret);
  
  // 6. Шифруем данные
  const encryptedData = await encryptData(JSON.stringify(credentials), encryptionKey);
  
  // 7. Отправляем зашифрованные данные
  const response = await fetch(endpoint, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      exchangeId: keyData.exchangeId,
      clientPublicKey: clientPublicKey.toString(16),
      encryptedData: encryptedData
    })
  });
  
  return response;
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
    initAuthTabs();
    initAuthForms();
    initTaskModal();
    initAdminSearch();
    checkAuth();
    
    // Добавляем глобальные функции для кнопок в задачах
    window.editTask = editTask;
    window.deleteTask = deleteTask;
});

// Переключение между вкладками входа и регистрации
function initAuthTabs() {
    const tabs = document.querySelectorAll('.tab-btn');
    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');
    
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            
            if (tab.dataset.tab === 'login') {
                loginForm.style.display = 'block';
                registerForm.style.display = 'none';
            } else {
                loginForm.style.display = 'none';
                registerForm.style.display = 'block';
            }
        });
    });
}

// Инициализация форм аутентификации
function initAuthForms() {
    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');
    
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const errorDiv = document.getElementById('login-error');
        errorDiv.textContent = '';
        
        const credentials = {
            username: document.getElementById('login-username').value.trim(),
            password: document.getElementById('login-password').value
        };
        
        try {
            console.log('Отправка защищённого запроса входа (Диффи-Хеллман):', { username: credentials.username, password: '***' });
            
            // Используем защищённый канал Диффи-Хеллмана
            const response = await secureAuthRequest('/api/auth/login', credentials);
            
            console.log('Ответ входа получен:', response.status, response.statusText);
            
            const data = await response.json();
            
            if (response.ok) {
                csrfToken = data.csrf_token;
                currentUser = data.user;
                showApp();
                showMessage('Вход выполнен успешно (защищённый канал)', 'success');
                loginForm.reset();
            } else {
                errorDiv.textContent = data.error || 'Ошибка входа';
            }
        } catch (error) {
            errorDiv.textContent = 'Ошибка соединения с сервером';
            console.error('Ошибка входа:', error);
        }
    });
    
    registerForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const errorDiv = document.getElementById('register-error');
        errorDiv.textContent = '';
        
        const password = document.getElementById('register-password').value;
        const passwordConfirm = document.getElementById('register-password-confirm').value;
        
        // Проверка совпадения паролей
        if (password !== passwordConfirm) {
            errorDiv.textContent = 'Пароли не совпадают';
            return;
        }
        
        const credentials = {
            username: document.getElementById('register-username').value.trim(),
            password: password
        };
        
        try {
            // Логируем без пароля для безопасности
            console.log('Отправка защищённого запроса регистрации (Диффи-Хеллман):', {
                username: credentials.username,
                password: '***'
            });
            
            // Используем защищённый канал Диффи-Хеллмана
            const response = await secureAuthRequest('/api/auth/register', credentials);
            
            console.log('Ответ регистрации получен:', response.status, response.statusText);
            
            const data = await response.json();
            
            if (response.ok) {
                csrfToken = data.csrf_token;
                currentUser = data.user;
                showApp();
                showMessage('Регистрация успешна (защищённый канал)', 'success');
                registerForm.reset();
            } else {
                errorDiv.textContent = data.error || 'Ошибка регистрации';
            }
        } catch (error) {
            errorDiv.textContent = 'Ошибка соединения с сервером';
            console.error('Ошибка регистрации:', error);
        }
    });
    
    // Кнопка выхода
    document.getElementById('logout-btn').addEventListener('click', async () => {
        try {
            await fetch('/api/auth/logout', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRF-Token': csrfToken
                }
            });
            
            currentUser = null;
            csrfToken = null;
            showAuth();
            showMessage('Выход выполнен', 'success');
        } catch (error) {
            console.error('Ошибка выхода:', error);
        }
    });
}

// Проверка текущей аутентификации
async function checkAuth() {
    try {
        const response = await fetch('/api/auth/me');
        const data = await response.json();
        
        if (response.ok) {
            currentUser = data.user;
            await getCsrfToken();
            showApp();
        } else {
            showAuth();
        }
    } catch (error) {
        showAuth();
    }
}

// Получение CSRF токена
async function getCsrfToken() {
    try {
        const response = await fetch('/api/auth/csrf-token');
        const data = await response.json();
        if (response.ok) {
            csrfToken = data.csrf_token;
        }
    } catch (error) {
        console.error('Ошибка получения CSRF токена:', error);
    }
}

// Показать форму аутентификации
function showAuth() {
    document.getElementById('auth-section').style.display = 'block';
    document.getElementById('app-section').style.display = 'none';
    document.getElementById('user-info').style.display = 'none';
}

// Показать основное приложение
function showApp() {
    document.getElementById('auth-section').style.display = 'none';
    document.getElementById('app-section').style.display = 'block';
    document.getElementById('user-info').style.display = 'flex';
    
    document.getElementById('username-display').textContent = currentUser.username;
    const roleBadge = document.getElementById('role-badge');
    roleBadge.textContent = currentUser.role === 'admin' ? 'Администратор' : 'Пользователь';
    roleBadge.classList.toggle('admin', currentUser.role === 'admin');
    
    const adminBtn = document.getElementById('admin-view-btn');
    const adminSearch = document.getElementById('admin-search');
    adminBtn.style.display = currentUser.role === 'admin' ? 'flex' : 'none';
    adminSearch.style.display = currentUser.role === 'admin' && isAdminView ? 'block' : 'none';
    
    // Обновляем заголовок
    const tasksTitle = document.getElementById('tasks-title');
    if (isAdminView) {
        tasksTitle.innerHTML = '<i class="fas fa-crown"></i> Все задачи (админ)';
    } else {
        tasksTitle.innerHTML = '<i class="fas fa-tasks"></i> Мои задачи';
    }
    
    loadTasks();
}

// Загрузка задач
async function loadTasks() {
    try {
        let endpoint = isAdminView && currentUser.role === 'admin' 
            ? '/api/tasks/admin/all' 
            : '/api/tasks';
        
        // Добавляем параметры поиска для админки
        if (isAdminView && currentUser.role === 'admin') {
            const username = document.getElementById('search-username')?.value.trim() || '';
            const taskTitle = document.getElementById('search-task')?.value.trim() || '';
            
            const params = new URLSearchParams();
            if (username) params.append('username', username);
            if (taskTitle) params.append('task', taskTitle);
            
            if (params.toString()) {
                endpoint += '?' + params.toString();
            }
        }
        
        const response = await fetch(endpoint, {
            headers: {
                'X-CSRF-Token': csrfToken
            }
        });
        
        const data = await response.json();
        
        if (response.ok) {
            displayTasks(data.tasks || []);
        } else {
            if (response.status === 401) {
                showAuth();
            } else {
                showMessage(data.error || 'Ошибка загрузки задач', 'error');
            }
        }
    } catch (error) {
        showMessage('Ошибка соединения с сервером', 'error');
        console.error('Ошибка загрузки задач:', error);
    }
}

// Отображение задач
function displayTasks(tasks) {
    const container = document.getElementById('tasks-container');
    
    if (tasks.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-tasks empty-icon"></i>
                <h3>Нет задач</h3>
                <p>Создайте свою первую задачу!</p>
            </div>
        `;
        
        // Обновляем счетчик задач
        const taskCount = document.getElementById('task-count');
        if (taskCount) {
            taskCount.textContent = '0 задач';
        }
        
        return;
    }
    
    // Обновляем счетчик задач
    const taskCount = document.getElementById('task-count');
    if (taskCount) {
        taskCount.textContent = `${tasks.length} ${getTaskWord(tasks.length)}`;
    }
    
    container.innerHTML = tasks.map(task => `
        <div class="task-card ${task.completed ? 'completed' : ''}">
            <div class="task-header">
                <div class="task-title">${escapeHtml(task.title)}</div>
                <span class="task-status ${task.completed ? 'completed' : ''}">
                    ${task.completed ? 'Выполнено' : 'В работе'}
                </span>
            </div>
            ${task.description ? `<div class="task-description">${escapeHtml(task.description)}</div>` : ''}
            <div class="task-meta">
                <i class="fas fa-calendar"></i>
                Создано: ${new Date(task.created_at).toLocaleString('ru-RU')}
                ${task.username ? `<br><i class="fas fa-user"></i> Пользователь: ${escapeHtml(task.username)}` : ''}
            </div>
            <div class="task-actions">
                <button class="btn btn-outline" onclick="editTask(${task.id})">
                    <i class="fas fa-edit"></i>
                    Редактировать
                </button>
                <button class="btn btn-secondary" onclick="deleteTask(${task.id})">
                    <i class="fas fa-trash"></i>
                    Удалить
                </button>
            </div>
        </div>
    `).join('');
}

// Функция для правильного склонения слова "задача"
function getTaskWord(count) {
    if (count % 10 === 1 && count % 100 !== 11) {
        return 'задача';
    } else if ([2, 3, 4].includes(count % 10) && ![12, 13, 14].includes(count % 100)) {
        return 'задачи';
    } else {
        return 'задач';
    }
}

// Защита от XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Инициализация модального окна
function initTaskModal() {
    const modal = document.getElementById('task-modal');
    const closeBtn = document.querySelector('.modal-close');
    const cancelBtn = document.getElementById('cancel-btn');
    const form = document.getElementById('task-form');
    
    // Исправленный обработчик закрытия модального окна
    closeBtn.addEventListener('click', () => {
        modal.style.display = 'none';
    });
    
    cancelBtn.addEventListener('click', () => {
        modal.style.display = 'none';
    });
    
    // Закрытие при клике на оверлей
    document.querySelector('.modal-overlay')?.addEventListener('click', (e) => {
        if (e.target.classList.contains('modal-overlay')) {
            modal.style.display = 'none';
        }
    });
    
    // Закрытие при клике на фон модального окна
    window.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.style.display = 'none';
        }
    });
    
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        await saveTask();
    });
    
    // Исправленный обработчик для кнопки добавления задачи
    document.getElementById('add-task-btn').addEventListener('click', () => {
        console.log('Кнопка "Добавить задачу" нажата');
        openTaskModal();
    });
    
    // Обработчик для кнопки переключения админского режима
    document.getElementById('admin-view-btn').addEventListener('click', () => {
        isAdminView = !isAdminView;
        const adminBtn = document.getElementById('admin-view-btn');
        const adminSearch = document.getElementById('admin-search');
        const tasksTitle = document.getElementById('tasks-title');
        
        adminBtn.innerHTML = isAdminView 
            ? '<i class="fas fa-user"></i> Мои задачи' 
            : '<i class="fas fa-crown"></i> Все задачи (админ)';
        
        adminSearch.style.display = isAdminView && currentUser?.role === 'admin' ? 'block' : 'none';
        
        tasksTitle.innerHTML = isAdminView 
            ? '<i class="fas fa-crown"></i> Все задачи (админ)' 
            : '<i class="fas fa-tasks"></i> Мои задачи';
        
        // Очищаем поиск при переключении
        if (!isAdminView) {
            document.getElementById('search-username').value = '';
            document.getElementById('search-task').value = '';
        }
        
        loadTasks();
    });
}

// Инициализация поиска в админке
function initAdminSearch() {
    const searchBtn = document.getElementById('search-btn');
    const clearSearchBtn = document.getElementById('clear-search-btn');
    const searchUsername = document.getElementById('search-username');
    const searchTask = document.getElementById('search-task');
    
    if (searchBtn) {
        searchBtn.addEventListener('click', () => {
            loadTasks();
        });
    }
    
    if (clearSearchBtn) {
        clearSearchBtn.addEventListener('click', () => {
            if (searchUsername) searchUsername.value = '';
            if (searchTask) searchTask.value = '';
            loadTasks();
        });
    }
    
    // Поиск при нажатии Enter
    if (searchUsername) {
        searchUsername.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                loadTasks();
            }
        });
    }
    
    if (searchTask) {
        searchTask.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                loadTasks();
            }
        });
    }
}

// Открыть модальное окно для создания/редактирования задачи
function openTaskModal(task = null) {
    const modal = document.getElementById('task-modal');
    const title = document.getElementById('modal-title');
    const form = document.getElementById('task-form');
    const errorDiv = document.getElementById('task-error');
    
    console.log('Открытие модального окна для задачи:', task);
    
    errorDiv.textContent = '';
    
    if (task) {
        title.innerHTML = '<i class="fas fa-edit"></i> Редактировать задачу';
        document.getElementById('task-id').value = task.id;
        document.getElementById('task-title').value = task.title;
        document.getElementById('task-description').value = task.description || '';
        document.getElementById('task-completed').checked = task.completed === 1 || task.completed === true;
    } else {
        title.innerHTML = '<i class="fas fa-plus"></i> Добавить задачу';
        form.reset();
        document.getElementById('task-id').value = '';
        document.getElementById('task-completed').checked = false;
    }
    
    modal.style.display = 'flex';
    setTimeout(() => {
        document.getElementById('task-title').focus();
    }, 100);
}

// Сохранение задачи
async function saveTask() {
    const errorDiv = document.getElementById('task-error');
    errorDiv.textContent = '';
    
    const taskId = document.getElementById('task-id').value;
    const taskData = {
        title: document.getElementById('task-title').value.trim(),
        description: document.getElementById('task-description').value.trim(),
        completed: document.getElementById('task-completed').checked,
        csrf_token: csrfToken
    };
    
    // Проверка обязательных полей
    if (!taskData.title) {
        errorDiv.textContent = 'Название задачи обязательно';
        return;
    }
    
    try {
        const url = taskId ? `/api/tasks/${taskId}` : '/api/tasks';
        const method = taskId ? 'PUT' : 'POST';
        
        // Логируем без CSRF токена для безопасности
        const logData = { ...taskData };
        delete logData.csrf_token;
        console.log('Отправка запроса:', method, url, { ...logData, csrf_token: '***' });
        
        const response = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-Token': csrfToken
            },
            body: JSON.stringify(taskData)
        });
        
        console.log('Ответ получен:', response.status, response.statusText);
        
        const data = await response.json();
        
        if (response.ok) {
            document.getElementById('task-modal').style.display = 'none';
            await getCsrfToken(); // Получаем новый токен после использования
            loadTasks();
            showMessage(taskId ? 'Задача обновлена' : 'Задача создана', 'success');
        } else {
            if (response.status === 401) {
                showAuth();
            } else {
                errorDiv.textContent = data.error || 'Ошибка сохранения задачи';
            }
        }
    } catch (error) {
        errorDiv.textContent = 'Ошибка соединения с сервером';
        console.error('Ошибка сохранения задачи:', error);
    }
}

// Редактирование задачи
async function editTask(id) {
    try {
        const response = await fetch(`/api/tasks/${id}`, {
            headers: {
                'X-CSRF-Token': csrfToken
            }
        });
        
        const data = await response.json();
        
        if (response.ok) {
            openTaskModal(data.task);
        } else {
            if (response.status === 401) {
                showAuth();
            } else {
                showMessage(data.error || 'Ошибка загрузки задачи', 'error');
            }
        }
    } catch (error) {
        showMessage('Ошибка соединения с сервером', 'error');
        console.error('Ошибка загрузки задачи:', error);
    }
}

// Удаление задачи
async function deleteTask(id) {
    if (!confirm('Вы уверены, что хотите удалить эту задачу?')) {
        return;
    }
    
    try {
        const response = await fetch(`/api/tasks/${id}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-Token': csrfToken
            }
        });
        
        const data = await response.json();
        
        if (response.ok) {
            await getCsrfToken(); // Получаем новый токен после использования
            loadTasks();
            showMessage('Задача удалена', 'success');
        } else {
            if (response.status === 401) {
                showAuth();
            } else {
                showMessage(data.error || 'Ошибка удаления задачи', 'error');
            }
        }
    } catch (error) {
        showMessage('Ошибка соединения с сервером', 'error');
        console.error('Ошибка удаления задачи:', error);
    }
}

// Показать сообщение
function showMessage(text, type = 'success') {
    const messageDiv = document.getElementById('message');
    messageDiv.textContent = text;
    messageDiv.className = `message ${type}`;
    messageDiv.style.display = 'flex';
    
    setTimeout(() => {
        messageDiv.style.display = 'none';
    }, 3000);
}