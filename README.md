# 🏨 HotelReserve_bot  

Telegram-бот для управления гостиничными номерами, бронирования и обработки пользовательских запросов.

Проект реализует полный цикл работы с данными: от просмотра номеров до бронирования, оплаты и обработки отзывов.


## 🚀 Основная функциональность

### 👤 Пользователь
- просмотр каталога гостиничных номеров с пагинацией  
- круглосуточное бронирование с проверкой конфликтов дат  
- оплата через Telegram  
- отправка отзывов о проживании  
- интеллектуальный помощник по FAQ: поиск релевантной информации по смыслу запроса с использованием векторного поиска и генерация ответов с помощью локальной LLM через Ollama.

### 👨‍💻 Администратор (Django Admin)
- добавление и редактирование гостиничных номеров
- просмотр бронирований
- просмотр пользовательских отзывов  
---

## Локальная vs облачная LLM для диалогового ассистента

| Критерий          | **☁ Облачная LLM** | **🖥 Локальная LLM** | **Как это влияет на проект** |
|-------------------------------|------------------------|-------------------|----------------|
| **Приватность данных 🛡**            |Диалоги и запросы пользователей отправляются внешнему сервису| Всё остаётся на сервере бота | Бронирования и вопросы пользователей не покидают инфраструктуру проекта |
| **Стоимость эксплуатации 💸** |Оплата за каждый токен/запрос | Разовая настройка и использование своих ресурсов | Масштабирование количества пользователей не увеличивает расходы на AI |
| **Доступность 🌐** |Зависимость от интернета и API | Автономная работа на сервере | Круглосуточная работа чат-помощника без риска недоступности внешнего сервиса|
| **Настройка производительности ⚡** |Зависит от провайдера | Можно оптимизировать локально под конкретные ресурсы | Подстраивание под доступную RAM, CPU/GPU, ускорение откликов |

### Аналитика отзывов с RuBERT

Бот использует модель RuBERT для анализа пользовательских отзывов  
и автоматической классификации их по тональности.

| Категория | Пример отзыва | Классификация |
|------------|---------------|----------------|
| **Позитивный** | «Отличный номер, чисто и уютно!» | 😊 Positive |
| **Нейтральный** | «Номер соответствует описанию.» | 😐 Neutral |
| **Негативный** | Шумно ночью, сложно спать.» | 😠 Negative |

### Тестирование платежей
Используйте тестовые карты:
- **Redsys**: `4918 0100 0000 0085` <br />
Срок действия: 03/26<br />
CVC/CVV: 111<br />

## 📸 Скриншоты

### Django Admin
<img width="855" height="484" alt="admin" src="https://github.com/user-attachments/assets/eb38fc13-cd08-4d98-8c2b-675af61a27ed" /><br />
<img width="1669" height="911" alt="admin_2" src="https://github.com/user-attachments/assets/c520c609-df25-41a3-a780-8d8b29109db2" /><br />
<img width="1912" height="905" alt="Снимок экрана 2026-07-27 171045" src="https://github.com/user-attachments/assets/91c42446-7c36-437b-8e93-4a85f469c6d6" /><br />
<img width="1914" height="906" alt="Снимок экрана 2026-07-27 171143" src="https://github.com/user-attachments/assets/6b69d983-39fa-4d40-8f17-44e753f0811b" /><br />

### Пользовательский интерфейс
<img width="1217" height="1032" alt="Снимок экрана 2026-08-06 215813" src="https://github.com/user-attachments/assets/c04baa9a-fe70-47cb-bf08-675708299c91" /><br />
<img width="1212" height="1032" alt="Снимок экрана 2026-08-06 220055" src="https://github.com/user-attachments/assets/a2f78302-f4ef-4862-a850-327e8e895ff7" /><br />
<img width="1217" height="1032" alt="Снимок экрана 2026-08-06 220630" src="https://github.com/user-attachments/assets/0b1a95ab-ad0f-47bd-9c86-99ae99a07196" /><br />
<img width="1219" height="1032" alt="Снимок экрана 2026-08-06 221151" src="https://github.com/user-attachments/assets/457992dd-62d1-4349-94eb-ad3bd970e7ea" /><br />
<img width="1224" height="1032" alt="Снимок экрана 2026-08-06 221513" src="https://github.com/user-attachments/assets/7d9e3ba8-dd65-44b4-bd7d-54cb8f387c90" /><br />

## 💳 Платежные системы
### Redsys
![Процесс оплаты](https://github.com/user-attachments/assets/a1bb13ea-8507-4279-bb67-a746d8241c31)<br />
<img width="384" height="595" alt="Снимок экрана 2026-08-06 221915" src="https://github.com/user-attachments/assets/df6e319a-7545-4ced-9edf-f2b28a3da20e" /><br />
*Преимущество: мгновенное подтверждение брони*

---
## 📂 Структура проекта

```text
HotelReserve_bot/
├── apps/                         # Django приложения
│   ├── core/                     # Базовое приложение проекта
│   │   ├── migrations/
│   │   │   └── __init__.py
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── tests.py
│   │   └── views.py
│   │
│   ├── bookings/                   # Модуль работы с бронированиями
│   │   ├── migrations/
│   │   │   └── __init__.py
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── tests.py
│   │   └── views.py
│   ├── reviews/                    # Модуль работы с отзывами
│   │   ├── migrations/
│   │   │   └── __init__.py
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── crud.py
│   │   ├── models.py
│   │   ├── tests.py
│   │   └── views.py
│   ├── support/                    # Модуль работы с базой знаний
│   │   ├── migrations/
│   │   │   └── __init__.py
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── crud.py
│   │   ├── models.py
│   │   ├── tests.py
│   │   └── views.py
│   ├── rooms/                    # Модуль работы с комнатами
│   │   ├── migrations/
│   │   │   └── __init__.py
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── crud.py
│   │   ├── models.py
│   │   ├── tests.py
│   │   └── views.py
│   │
│   └── users/                    # Модуль работы с пользователями
│       ├── migrations/
│       │   └── __init__.py
│       ├── __init__.py
│       ├── admin.py
│       ├── apps.py
│       ├── crud.py
│       ├── models.py
│       ├── tests.py
│       └── views.py
│
├── config/                       # Конфигурация проекта Django
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── bot/                          # Основной backend / бизнес-логика приложения
│   ├── common/                   # Общие константы и компоненты
│   │   ├── __init__.py
│   │   ├── callbacks.py
│   │   └── texts.py
│   ├── handlers/                 # Обработчики пользовательских запросов
│   │   ├── __init__.py
│   │   ├── ai_handlers.py
│   │   ├── booking_handlers.py
│   │   ├── catalog_handlers.py
│   │   ├── payment_handlers.py
│   │   ├── reservation_handlers.py
│   │   └── review_handlers.py
│   ├── keyboards/                # Клавиатуры интерфейса
│   │   ├── __init__.py
│   │   └── user_keyboard.py
│   ├── nlp/                     # Модули обработки естественного языка и LLM
│   │   ├── rag/
│   │   │   ├── __init__.py
│   │   │   └── vector_search.py
│   │   ├── __init__.py
│   │   ├── llm_client.py
│   │   └── sentiment_analyzer.py
│   │
│   ├── services/                  # Сервисы бизнес-логики
│   │   ├── __init__.py
│   │   ├── ai_service.py
│   │   ├── booking_service.py
│   │   └── reservation_draft.py
│   │
│   ├── utils/                   # Вспомогательные утилиты
│   │   ├── __init__.py
│   │   ├── catalog_utils.py
│   │   └── paginator.py
│   │
│   ├── payment.py               # Логика платежей
│   └── states.py               # FSM состояния
│
├── .dockerignore
├── .env
├── .gitignore
├── .python-version
├── docker-compose.yml
├── Dockerfile
├── start_bot.py
├── manage.py
├── pyproject.toml
├── README.md
└── uv.lock
```
## 🛠️ Технологии

| Модуль          | Описание                          |
|-----------------|-----------------------------------|
| `aiogram`       | Фреймворк для создания Telegram-ботов|
| `Django`|Веб-фреймворк с ORM и встроенной административной панелью|
| `psycopg-binary`|Предкомпилированный клиент PostgreSQL для быстрого развертывания бота|
| `pgvector`|Расширение PostgreSQL для хранения и поиска по векторным данным (эмбеддингам)|
| `python-dotenv` | Работа с переменными окружения|
| `transformers` | Библиотека для NLP и работы с трансформерами от Hugging Face|
| `sentence-transformers`|Библиотека для генерации векторных представлений текста (эмбеддингов) на основе трансформер-моделей|
| `torch` |Фреймворк PyTorch для запуска и обработки готовых нейросетевых моделей|
| `openai`|Библиотека для работы с LLM через OpenAI-совместимый API|
| **NLP-модель**  | [blanchefort/rubert-base-cased-sentiment](https://huggingface.co/blanchefort/rubert-base-cased-sentiment) |

---
## 📦 Установка

## Инструкция по использованию бота:<br />

Для успешного запуска и использования бота, выполните следующие шаги:

### Шаг 1: Заполнение файла ".env"
Файл ".env" содержит все важные параметры конфигурации, которые необходимы для работы бота. Убедитесь, что вы заполнили все требуемые поля:

- **TOKEN** — токен Telegram-бота, включая доступ к Telegram Payments [@BotFather](https://t.me/BotFather)

### Пример заполнения файла .env:
```plaintext
TOKEN=ВАШ_ТОКЕН
PAYMENTS_TOKEN=ВАШ_PAYMENT_TOKEN
```
### Шаг 2: Подключение к базе данных на PostgreSQL
Для работы с базой данных требуется указать параметры подключения в файле ".env":

- **HOST**: Адрес хоста базы данных.
- **DBNAME**: Имя базы данных.
- **USER**: Имя пользователя для доступа к базе данных.
- **PASSWORD**: Пароль к базе данных.
- **PORT**: Порт для подключения (например, 5432 по умолчанию для PostgreSQL).

### Пример заполнения:
```plaintext
HOST="db"
DBNAME="example_db"
USER="admin_user"
PASSWORD="strongpassword"
PORT="5432"
```

### Шаг 3: Подготовка виртуального окружения и запуск бота

1. Создайте виртуальное окружение для изоляции зависимостей проекта. 
   Используйте команду:
   ```bash
   uv venv
   ```

2. Активируйте виртуальное окружение:
   - На Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - На macOS и Linux:
     ```bash
     source .venv/bin/activate
     ```
3. Установка зависимостей:
      ```bash
      uv sync
      ```
4. Запуск Ollama (скачивается образ, если нет):
   ```bash
    docker-compose up -d ollama
     ```
5. Загрузка нужной модели внутрь Ollama:
   ```bash
    docker exec -it ollama /bin/ollama pull infidelis/GigaChat-20B-A3B-instruct:q4_0
     ```
6. Проверка, что модель есть:
   ```bash
   docker exec -it ollama /bin/ollama list
     ```
7. Сборка образа:
   ```bash
    docker-compose up -d --build
     ```
8. Запуск контейнера:
   ```bash
   docker-compose up
   ```
9.  Создание миграций (только при изменении моделей):
   ```bash
   docker compose exec django uv run python manage.py makemigrations
   ```
10. Применить миграции:
   ```bash
   docker compose exec django uv run python manage.py migrate
   ```
11. Создание суперпользователя (админ-доступ к Django):
   ```bash
   docker compose exec django uv run python manage.py createsuperuser
   ```
Теперь бот должен быть готов к использованию. Убедитесь, что ваше соединение с интернетом активно и все конфигурации настроены корректно. Если возникнут ошибки, проверьте файл ".env" на наличие опечаток или некорректных значений.
