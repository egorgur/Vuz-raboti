# Markio Application Instruction

## Описание
Markio — это Android-приложение для управления заметками, использующее Room Database для локального хранения данных.

## Как собрать APK
Для сборки APK выполните следующую команду в корневом каталоге проекта:
```bash
./gradlew assembleDebug
```
После завершения сборки, APK файл будет находиться по пути:
`app/build/outputs/apk/debug/app-debug.apk`

## Как запустить
1. Подключите Android-устройство или запустите эмулятор.
2. Выполните команду:
```bash
./gradlew installDebug
```

## Используемые технологии
- Kotlin
- Jetpack Navigation
- Room Database
- View Binding
- Material Design
