# DMARC Reports Parser

Автоматический парсер DMARC отчетов с отправкой результатов на email.

## Как это работает

Процесс полностью автоматизирован и выполняется в Docker-контейнере:

    - parsedmarc подключается к указанному вами почтовому ящику (например, dmarc-reports@yourdomain.com) по IMAP.
    - Он находит все непрочитанные письма с DMARC-отчётами и обрабатывает их.
    - из папки результата выполнения содержимое всех .json формирует сообщение письма
    - отправляется на указанный вами email через SMTP, только если не была пройдена проверка и одно из полей:
        spf, dkim, dmarc содержит false.
    - parsedmarc обработанные письма в почтовом ящике переносит в Archives/Aggregate, чтобы не анализировать их повторно.

## Запуск

```bash
# Измените .env
cp .env.example .env

# Сборка образа
docker build -t dmarc-reports-parser:latest .

./run_dmarc.sh
```

## Конфигурация

Все настройки производятся в файле .env:

    IMAP_HOST: Сервер для чтения почты.
    IMAP_USER: Логин почтового ящика для сбора отчётов.
    IMAP_PASSWORD: Пароль от этого ящика.
    SMTP_HOST: Сервер для отправки итогового отчёта.
    SMTP_USER: Логин для отправки.
    SMTP_PASSWORD: Пароль для отправки.
    RECIPIENT_EMAIL: Email, на который придёт обработанный отчёт.

## Структура проекта

```
dmarc-reports-parser/
├── Dockerfile                 # Docker образ
├── run_dmarc.sh              # Скрипт запуска
├── config/
│   └── parsedmarc.ini.template  # Шаблон конфигурации
├── scripts/
│   ├── run_parser.sh         # Основной скрипт в контейнере
│   └── send_email.py         # Отправка результатов
|-- .env.example              # Пример переменных окружения
└── README.md
```

## Автоматизация

### Cron
```bash
crontab -e
0 7 * * * /path/to/dmarc-reports-parser/run_dmarc.sh
```

## Пример работы в терминале

```bash
➜  dmarc-reports-parser ./run_dmarc.sh
🔄 Запуск parsedmarc...
✅ Отчет отправлен
```

