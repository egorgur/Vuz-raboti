# Инструкция по сборке APK-файла через интерфейс командной строки (CLI)

Для сборки приложения Markio без использования графического интерфейса Android Studio, выполните следующие шаги.

## 1. Предварительные требования
*   Установленный **JDK 17** или выше.
*   Установленный **Android SDK**.
*   Настроенная переменная окружения `ANDROID_HOME` или файл `local.properties` в корне проекта с указанием пути к SDK:
    ```properties
    sdk.dir=/path/to/android/sdk
    ```

## 2. Подготовка скрипта
Убедитесь, что файл `gradlew` имеет права на выполнение (для Linux/macOS):
```bash
chmod +x gradlew
```

## 3. Команды сборки

### Сборка отладочной версии (Debug APK)
Эта версия используется для тестирования и не требует настройки ключей подписи.
```bash
./gradlew assembleDebug
```
**Результат:** `app/build/outputs/apk/debug/app-debug.apk`

### Сборка релизной версии (Release APK)
```bash
./gradlew assembleRelease
```
**Результат:** `app/build/outputs/apk/release/app-release-unsigned.apk`
*Примечание: данный файл необходимо подписать с помощью `apksigner` перед установкой на устройство.*

### Сборка Android App Bundle (AAB)
Рекомендуемый формат для публикации в Google Play.
```bash
./gradlew bundleRelease
```
**Результат:** `app/build/outputs/bundle/release/app-release.aab`

## 4. Очистка проекта
Если возникли ошибки сборки, рекомендуется выполнить полную очистку:
```bash
./gradlew clean
```
