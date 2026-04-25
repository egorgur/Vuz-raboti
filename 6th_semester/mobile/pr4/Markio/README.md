# Markio — Мобильное приложение для заметок и погоды

## Описание

**Markio** — мобильное Android-приложение, реализующее пользовательский интерфейс по макету из Figma. Приложение содержит 4 экрана:

1. **Вход** — экран авторизации с полями email и пароль
2. **Регистрация** — экран создания аккаунта
3. **Главная (Погода)** — отображение погоды и карты (статические данные)
4. **Заметки** — список заметок с возможностью создания, редактирования и удаления

Данные заполнены статическими объектами.

## Технологии

- **Язык:** Kotlin
- **Минимальная версия Android:** API 26 (Android 8.0)
- **Целевая версия:** API 34 (Android 14)
- **Система сборки:** Gradle 9.4 (Kotlin DSL)
- **Android Gradle Plugin:** 9.1.0
- **Kotlin:** built-in support from AGP 9.1
- **UI:** XML Layouts + Material Components

## Структура проекта

```
Markio/
├── app/
│   ├── build.gradle.kts          # Конфигурация модуля приложения
│   ├── proguard-rules.pro
│   └── src/main/
│       ├── AndroidManifest.xml
│       ├── java/com/markio/app/
│       │   ├── LoginActivity.kt      # Экран входа
│       │   ├── RegisterActivity.kt   # Экран регистрации
│       │   ├── MainActivity.kt       # Главный экран с табами
│       │   ├── WeatherFragment.kt    # Фрагмент погоды
│       │   ├── NotesFragment.kt      # Фрагмент заметок
│       │   ├── NotesAdapter.kt       # Адаптер для RecyclerView
│       │   └── Note.kt              # Модель данных заметки
│       └── res/
│           ├── layout/               # XML-разметки экранов
│           ├── drawable/             # Фоны, иконки
│           └── values/               # Цвета, строки, темы
├── build.gradle.kts              # Корневой файл сборки
├── settings.gradle.kts           # Настройки проекта
└── gradle/wrapper/
    └── gradle-wrapper.properties
```

## Инструкция по сборке APK

### Предварительные требования

1. **Java Development Kit (JDK) 17** или выше
   ```bash
   # Проверка версии Java
   java -version
   ```

2. **Android SDK** — должен быть установлен с компонентами:
   - Android SDK Platform 34
   - Android SDK Build-Tools 36.0.0
   - Android SDK Command-line Tools

3. **Переменные окружения:**
   ```bash
   export ANDROID_HOME=$HOME/Android/Sdk
   export ANDROID_SDK_ROOT=$HOME/Android/Sdk
   export PATH=$PATH:$ANDROID_HOME/cmdline-tools/latest/bin
   export PATH=$PATH:$ANDROID_HOME/platform-tools
   export PATH=$PATH:$ANDROID_HOME/build-tools/36.0.0
   ```

4. **Локальная настройка SDK для Gradle:**
   создайте файл `local.properties` в корне проекта со строкой:
   ```properties
   sdk.dir=/home/master/Android/Sdk
   ```

### Сборка Debug APK

```bash
# 1. Перейти в директорию проекта
cd Markio

# 2. Сделать gradlew исполняемым (Linux/macOS)
chmod +x gradlew

# 3. Собрать debug APK
./gradlew assembleDebug
```

> Проект настроен на современные плагины для `Gradle 9.4`, поэтому требуется `JDK 17+`.

Готовый APK будет находиться по пути:
```
app/build/outputs/apk/debug/app-debug.apk
```

### Сборка Release APK

```bash
# 1. Собрать release APK (без подписи)
./gradlew assembleRelease
```

Готовый APK будет находиться по пути:
```
app/build/outputs/apk/release/app-release-unsigned.apk
```

### Подписание Release APK (опционально)

```bash
# 1. Создать keystore (если ещё нет)
keytool -genkey -v -keystore markio-release-key.jks \
  -keyalg RSA -keysize 2048 -validity 10000 \
  -alias markio

# 2. Подписать APK
apksigner sign --ks markio-release-key.jks \
  --out app-release-signed.apk \
  app/build/outputs/apk/release/app-release-unsigned.apk

# 3. Проверить подпись
apksigner verify app-release-signed.apk
```

### Установка на устройство

```bash
# Установить APK на подключённое устройство через ADB
adb install app/build/outputs/apk/debug/app-debug.apk
```

### Сборка через Android Studio

1. Открыть папку `Markio` в Android Studio
2. Дождаться синхронизации Gradle
3. **Build → Build Bundle(s) / APK(s) → Build APK(s)**
4. APK появится в `app/build/outputs/apk/debug/`

## Навигация в приложении

1. При запуске открывается **экран входа**
2. Нажатие «Зарегистрироваться» → переход на **экран регистрации**
3. Нажатие «Войти» / «Создать аккаунт» → переход на **главный экран**
4. На главном экране переключение между вкладками **Погода** и **Заметки**
5. Нажатие «Выйти» → возврат на экран входа

## Автор

Практическая работа №2 — Реализация пользовательского интерфейса мобильного приложения.
