# Prepilo — Architecture Specification

## 1. Backend Architecture

Backend строится на **FastAPI** с **модульной архитектурой**.

Идея: каждый бизнес-модуль проекта живет отдельно и содержит свои routes, schemas, models, services и repository.

То есть не делаем кашу в одном файле `main.py`, потому что потом это будет не backend, а суп из импортов.

---

# 2. Backend Modules

Основные backend-модули:

```text
auth
users
subjects
topics
study_plans
study_tasks
quizzes
ai
progress
friends
help_requests
notifications
dashboard
```

Каждый модуль отвечает только за свою бизнес-зону.

---

# 3. Backend Folder Structure

```text
prepilo-backend/
│
├── app/
│   ├── main.py
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── security.py
│   │   ├── exceptions.py
│   │   └── dependencies.py
│   │
│   ├── modules/
│   │   ├── auth/
│   │   │   ├── router.py
│   │   │   ├── schemas.py
│   │   │   ├── service.py
│   │   │   └── utils.py
│   │   │
│   │   ├── users/
│   │   │   ├── router.py
│   │   │   ├── models.py
│   │   │   ├── schemas.py
│   │   │   ├── service.py
│   │   │   └── repository.py
│   │   │
│   │   ├── subjects/
│   │   │   ├── router.py
│   │   │   ├── models.py
│   │   │   ├── schemas.py
│   │   │   ├── service.py
│   │   │   └── repository.py
│   │   │
│   │   ├── topics/
│   │   │   ├── router.py
│   │   │   ├── models.py
│   │   │   ├── schemas.py
│   │   │   ├── service.py
│   │   │   └── repository.py
│   │   │
│   │   ├── study_plans/
│   │   │   ├── router.py
│   │   │   ├── models.py
│   │   │   ├── schemas.py
│   │   │   ├── service.py
│   │   │   └── repository.py
│   │   │
│   │   ├── quizzes/
│   │   │   ├── router.py
│   │   │   ├── models.py
│   │   │   ├── schemas.py
│   │   │   ├── service.py
│   │   │   └── repository.py
│   │   │
│   │   ├── ai/
│   │   │   ├── router.py
│   │   │   ├── schemas.py
│   │   │   ├── service.py
│   │   │   ├── prompts.py
│   │   │   └── providers.py
│   │   │
│   │   ├── friends/
│   │   │   ├── router.py
│   │   │   ├── models.py
│   │   │   ├── schemas.py
│   │   │   ├── service.py
│   │   │   └── repository.py
│   │   │
│   │   ├── help_requests/
│   │   │   ├── router.py
│   │   │   ├── models.py
│   │   │   ├── schemas.py
│   │   │   ├── service.py
│   │   │   └── repository.py
│   │   │
│   │   ├── notifications/
│   │   │   ├── router.py
│   │   │   ├── models.py
│   │   │   ├── schemas.py
│   │   │   ├── service.py
│   │   │   └── repository.py
│   │   │
│   │   └── dashboard/
│   │       ├── router.py
│   │       ├── schemas.py
│   │       └── service.py
│   │
│   └── shared/
│       ├── enums.py
│       ├── pagination.py
│       ├── permissions.py
│       └── utils.py
│
├── alembic/
├── tests/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

# 4. Backend Layer Logic

В каждом модуле можно использовать такую структуру:

```text
router.py       — принимает HTTP requests
schemas.py      — Pydantic request/response схемы
models.py       — SQLAlchemy модели
repository.py   — запросы к базе данных
service.py      — бизнес-логика
```

## Пример потока

```text
React
↓
FastAPI router
↓
Pydantic schema validation
↓
Service layer
↓
Repository layer
↓
PostgreSQL
```

---

# 5. Backend Responsibility by Layer

## router.py

Отвечает за API endpoint.

Например:

```text
POST /api/subjects
GET /api/subjects
PATCH /api/subjects/{id}
DELETE /api/subjects/{id}
```

В `router.py` не должно быть сложной бизнес-логики.

Он должен:

* принять request;
* проверить авторизацию;
* вызвать service;
* вернуть response.

---

## schemas.py

Отвечает за валидацию данных.

Например:

```text
SubjectCreate
SubjectUpdate
SubjectResponse
```

Тут проверяется:

* обязательные поля;
* типы данных;
* ограничения;
* формат ответа.

---

## models.py

Отвечает за таблицы базы данных.

Например:

```text
User
Subject
Topic
Quiz
Friendship
HelpRequest
```

---

## repository.py

Отвечает за работу с базой данных.

Например:

```text
get_subject_by_id
get_user_subjects
create_subject
delete_subject
```

В repository не надо писать бизнес-логику. Только database queries.

---

## service.py

Самый важный слой.

Тут живет бизнес-логика:

* проверка прав доступа;
* генерация учебного плана;
* расчет прогресса;
* определение weak topics;
* отправка help request;
* начисление help points;
* вызов AI;
* проверка AI-ответа.

Например:

```text
Если quiz score < 60%, topic becomes weak.
```

Это должно быть в `service.py`, а не в `router.py`.

---

# 6. Backend Module Examples

## Subjects Module

Отвечает за предметы.

```text
modules/subjects/
├── router.py
├── models.py
├── schemas.py
├── service.py
└── repository.py
```

Бизнес-логика:

* пользователь может видеть только свои предметы;
* предмет нельзя создать без названия;
* при удалении предмета удаляются или архивируются связанные темы и планы;
* study plan нельзя создать без exam_date.

---

## Topics Module

Отвечает за темы.

Бизнес-логика:

* тема принадлежит предмету;
* пользователь может управлять только темами своих предметов;
* difficulty от 1 до 5;
* priority от 1 до 3;
* если quiz score ниже 60%, topic становится weak;
* если quiz score выше 75% и задачи завершены, topic может стать done.

---

## Study Plans Module

Отвечает за учебные планы.

Бизнес-логика:

* план создается по предмету;
* план учитывает exam_date;
* high priority темы идут раньше;
* weak topics получают review tasks;
* done topics не ставятся как новые learning tasks;
* задачи не могут быть позже exam_date.

---

## AI Module

Отвечает за работу с AI provider.

```text
modules/ai/
├── router.py
├── schemas.py
├── service.py
├── prompts.py
└── providers.py
```

Бизнес-логика:

* frontend не общается с AI напрямую;
* API key хранится только на backend;
* AI response должен быть проверен через Pydantic;
* AI не меняет базу напрямую;
* backend сохраняет только валидированный результат.

---

## Friends Module

Отвечает за друзей.

Бизнес-логика:

* нельзя добавить самого себя;
* нельзя отправить duplicate request;
* friendship имеет статусы pending, accepted, declined, blocked;
* только accepted friends могут отправлять help requests;
* приватность проверяется перед показом прогресса.

---

## Help Requests Module

Отвечает за помощь между друзьями.

Бизнес-логика:

* help request можно отправить только другу;
* help request должен быть связан с topic;
* receiver может accept или decline;
* после completed другу начисляются help points;
* completed request нельзя редактировать.

---

# 7. Frontend Architecture

Frontend строится на **React + TypeScript** с архитектурой **Feature-Sliced Design**, то есть **FSD**.

FSD помогает не превратить frontend в папку `components`, где через неделю никто не понимает, где кнопка, где страница, а где логика авторизации.

---

# 8. FSD Layers

Frontend делится на слои:

```text
app
pages
widgets
features
entities
shared
```

## app

Инициализация приложения.

Тут лежит:

* router;
* providers;
* store;
* global styles;
* query client.

## pages

Страницы приложения.

Например:

* LoginPage;
* RegisterPage;
* DashboardPage;
* SubjectsPage;
* SubjectDetailsPage;
* StudyPlanPage;
* QuizPage;
* FriendsPage;
* HelpRequestsPage.

## widgets

Крупные UI-блоки, которые собирают несколько features/entities.

Например:

* Header;
* Sidebar;
* DashboardStats;
* TodayTasksWidget;
* WeakTopicsWidget;
* FriendRequestsWidget;
* StudyPlanCalendar.

## features

Пользовательские действия.

Например:

* login;
* register;
* create subject;
* create topic;
* generate study plan;
* complete task;
* submit quiz;
* send friend request;
* accept help request;
* generate AI explanation.

## entities

Бизнес-сущности.

Например:

* user;
* subject;
* topic;
* study-plan;
* study-task;
* quiz;
* friend;
* help-request;
* notification.

## shared

Переиспользуемые вещи, которые не зависят от бизнес-логики.

Например:

* UI components;
* API client;
* constants;
* helpers;
* types;
* config.

---

# 9. Frontend Folder Structure with FSD

```text
prepilo-frontend/
│
├── src/
│   ├── app/
│   │   ├── providers/
│   │   │   ├── AppProviders.tsx
│   │   │   └── QueryProvider.tsx
│   │   ├── router/
│   │   │   └── router.tsx
│   │   ├── styles/
│   │   │   └── globals.css
│   │   └── main.tsx
│   │
│   ├── pages/
│   │   ├── login/
│   │   │   └── ui/LoginPage.tsx
│   │   ├── register/
│   │   │   └── ui/RegisterPage.tsx
│   │   ├── dashboard/
│   │   │   └── ui/DashboardPage.tsx
│   │   ├── subjects/
│   │   │   └── ui/SubjectsPage.tsx
│   │   ├── subject-details/
│   │   │   └── ui/SubjectDetailsPage.tsx
│   │   ├── study-plan/
│   │   │   └── ui/StudyPlanPage.tsx
│   │   ├── quiz/
│   │   │   └── ui/QuizPage.tsx
│   │   ├── friends/
│   │   │   └── ui/FriendsPage.tsx
│   │   └── help-requests/
│   │       └── ui/HelpRequestsPage.tsx
│   │
│   ├── widgets/
│   │   ├── app-header/
│   │   │   └── ui/AppHeader.tsx
│   │   ├── sidebar/
│   │   │   └── ui/Sidebar.tsx
│   │   ├── dashboard-stats/
│   │   │   └── ui/DashboardStats.tsx
│   │   ├── today-tasks/
│   │   │   └── ui/TodayTasksWidget.tsx
│   │   ├── weak-topics/
│   │   │   └── ui/WeakTopicsWidget.tsx
│   │   ├── study-plan-calendar/
│   │   │   └── ui/StudyPlanCalendar.tsx
│   │   └── incoming-help-requests/
│   │       └── ui/IncomingHelpRequests.tsx
│   │
│   ├── features/
│   │   ├── auth-by-email/
│   │   │   ├── ui/LoginForm.tsx
│   │   │   ├── model/useLogin.ts
│   │   │   └── api/loginApi.ts
│   │   │
│   │   ├── register-user/
│   │   │   ├── ui/RegisterForm.tsx
│   │   │   ├── model/useRegister.ts
│   │   │   └── api/registerApi.ts
│   │   │
│   │   ├── create-subject/
│   │   │   ├── ui/CreateSubjectForm.tsx
│   │   │   ├── model/useCreateSubject.ts
│   │   │   └── api/createSubjectApi.ts
│   │   │
│   │   ├── create-topic/
│   │   │   ├── ui/CreateTopicForm.tsx
│   │   │   ├── model/useCreateTopic.ts
│   │   │   └── api/createTopicApi.ts
│   │   │
│   │   ├── generate-study-plan/
│   │   │   ├── ui/GenerateStudyPlanButton.tsx
│   │   │   ├── model/useGenerateStudyPlan.ts
│   │   │   └── api/generateStudyPlanApi.ts
│   │   │
│   │   ├── complete-study-task/
│   │   │   ├── ui/CompleteTaskButton.tsx
│   │   │   ├── model/useCompleteTask.ts
│   │   │   └── api/completeTaskApi.ts
│   │   │
│   │   ├── submit-quiz/
│   │   │   ├── ui/SubmitQuizButton.tsx
│   │   │   ├── model/useSubmitQuiz.ts
│   │   │   └── api/submitQuizApi.ts
│   │   │
│   │   ├── send-friend-request/
│   │   │   ├── ui/SendFriendRequestButton.tsx
│   │   │   ├── model/useSendFriendRequest.ts
│   │   │   └── api/sendFriendRequestApi.ts
│   │   │
│   │   ├── send-help-request/
│   │   │   ├── ui/SendHelpRequestForm.tsx
│   │   │   ├── model/useSendHelpRequest.ts
│   │   │   └── api/sendHelpRequestApi.ts
│   │   │
│   │   └── generate-ai-explanation/
│   │       ├── ui/GenerateAIExplanationButton.tsx
│   │       ├── model/useGenerateAIExplanation.ts
│   │       └── api/generateAIExplanationApi.ts
│   │
│   ├── entities/
│   │   ├── user/
│   │   │   ├── api/userApi.ts
│   │   │   ├── model/types.ts
│   │   │   └── ui/UserAvatar.tsx
│   │   │
│   │   ├── subject/
│   │   │   ├── api/subjectApi.ts
│   │   │   ├── model/types.ts
│   │   │   └── ui/SubjectCard.tsx
│   │   │
│   │   ├── topic/
│   │   │   ├── api/topicApi.ts
│   │   │   ├── model/types.ts
│   │   │   └── ui/TopicCard.tsx
│   │   │
│   │   ├── study-task/
│   │   │   ├── api/studyTaskApi.ts
│   │   │   ├── model/types.ts
│   │   │   └── ui/StudyTaskCard.tsx
│   │   │
│   │   ├── quiz/
│   │   │   ├── api/quizApi.ts
│   │   │   ├── model/types.ts
│   │   │   └── ui/QuizCard.tsx
│   │   │
│   │   ├── friend/
│   │   │   ├── api/friendApi.ts
│   │   │   ├── model/types.ts
│   │   │   └── ui/FriendCard.tsx
│   │   │
│   │   ├── help-request/
│   │   │   ├── api/helpRequestApi.ts
│   │   │   ├── model/types.ts
│   │   │   └── ui/HelpRequestCard.tsx
│   │   │
│   │   └── notification/
│   │       ├── api/notificationApi.ts
│   │       ├── model/types.ts
│   │       └── ui/NotificationItem.tsx
│   │
│   └── shared/
│       ├── api/
│       │   └── axiosInstance.ts
│       ├── config/
│       │   └── env.ts
│       ├── ui/
│       │   ├── Button.tsx
│       │   ├── Input.tsx
│       │   ├── Modal.tsx
│       │   ├── Select.tsx
│       │   ├── Card.tsx
│       │   └── Loader.tsx
│       ├── lib/
│       │   ├── formatDate.ts
│       │   ├── calculateProgress.ts
│       │   └── cn.ts
│       └── types/
│           └── common.ts
```

---

# 10. FSD Import Rule

Главное правило FSD:

```text
Верхние слои могут импортировать нижние.
Нижние слои не должны импортировать верхние.
```

То есть:

```text
pages → widgets → features → entities → shared
```

Можно:

```text
page импортирует widget
feature импортирует entity
entity импортирует shared
```

Нельзя:

```text
shared импортирует entity
entity импортирует feature
feature импортирует page
```

Иначе архитектура начнет ехать, как Docker контейнер без `.env`.

---

# 11. Example Frontend Flow

## Generate Study Plan

Пользователь на странице предмета нажимает кнопку:

```text
Generate Study Plan
```

Поток на frontend:

```text
pages/subject-details
↓
widgets/study-plan-calendar
↓
features/generate-study-plan
↓
entities/study-plan
↓
shared/api
```

Поток на backend:

```text
POST /api/study-plans/generate
↓
study_plans/router.py
↓
study_plans/service.py
↓
topics/repository.py
↓
ai/service.py
↓
study_plans/repository.py
↓
PostgreSQL
```

---

# 12. Example Backend + Frontend Mapping

| Business Feature        | Backend Module        | Frontend FSD Feature               |
| ----------------------- | --------------------- | ---------------------------------- |
| Login                   | `auth`                | `features/auth-by-email`           |
| Register                | `auth`                | `features/register-user`           |
| Create subject          | `subjects`            | `features/create-subject`          |
| Create topic            | `topics`              | `features/create-topic`            |
| Generate study plan     | `study_plans`, `ai`   | `features/generate-study-plan`     |
| Complete task           | `study_tasks`         | `features/complete-study-task`     |
| Generate quiz           | `quizzes`, `ai`       | `features/generate-ai-quiz`        |
| Submit quiz             | `quizzes`, `progress` | `features/submit-quiz`             |
| Send friend request     | `friends`             | `features/send-friend-request`     |
| Send help request       | `help_requests`       | `features/send-help-request`       |
| Generate AI explanation | `ai`                  | `features/generate-ai-explanation` |
| View dashboard          | `dashboard`           | `pages/dashboard` + `widgets/*`    |

---

# 13. Updated Final Stack

```text
Prepilo

Backend:
- FastAPI
- Modular Architecture
- SQLAlchemy
- Alembic
- Pydantic
- PostgreSQL
- JWT Auth
- AI Provider API
- Docker

Frontend:
- React
- TypeScript
- Vite
- Feature-Sliced Design
- React Router
- TanStack Query
- Axios
- React Hook Form
- Zod
- Tailwind CSS

DevOps:
- Docker
- Docker Compose

Optional later:
- Redis
- Celery / RQ
- WebSockets