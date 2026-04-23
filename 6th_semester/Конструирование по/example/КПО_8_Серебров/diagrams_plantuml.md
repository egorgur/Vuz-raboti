# PlantUML-диаграммы для отчёта ПАПС №8

Каждый блок кода — отдельная диаграмма.  
Вставляй содержимое каждого блока на сайт https://www.plantuml.com/plantuml/uml/ или в Visual Paradigm.

---

## 1. C4 — Диаграмма контекста: СТАРАЯ архитектура (MVC Монолит)

```plantuml
@startuml C4_Context_Old
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Context.puml

LAYOUT_WITH_LEGEND()

title C4 Context — JobPortal (MVC Монолит, Лаб. работа №7)

Person(jobseeker, "Соискатель", "Публикует резюме,\nищет вакансии")
Person(employer, "Работодатель", "Публикует вакансии,\nпродвигает объявления")
Person(admin, "Администратор", "Модерирует контент\nи пользователей")

System(jobportal, "JobPortal (Монолит)", "Единое Java-приложение.\nMVC-архитектура.\nController + Model + Repository\nв одном развёртываемом артефакте.")

System_Ext(smtp, "SMTP-сервер", "Отправка email-уведомлений\nпользователям")
System_Ext(payment, "Платёжная система", "Обработка платежей\nза продвижение вакансий")
SystemDb_Ext(db, "База данных (SQL)", "Единая реляционная БД\nдля всех данных системы")

Rel(jobseeker, jobportal, "Использует", "HTTP")
Rel(employer, jobportal, "Использует", "HTTP")
Rel(admin, jobportal, "Администрирует", "HTTP")
Rel(jobportal, smtp, "Отправляет письма", "SMTP")
Rel(jobportal, payment, "Проводит платежи", "HTTPS/API")
Rel(jobportal, db, "Читает и пишет данные", "JDBC/SQL")

@enduml
```

---

## 2. C4 — Диаграмма контекста: НОВАЯ архитектура (Микросервисы)

```plantuml
@startuml C4_Context_New
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Context.puml

LAYOUT_WITH_LEGEND()

title C4 Context — JobPortal (Микросервисы, Лаб. работа №8)

Person(jobseeker, "Соискатель", "Публикует резюме,\nищет вакансии")
Person(employer, "Работодатель", "Публикует вакансии,\nпродвигает объявления")
Person(admin, "Администратор", "Модерирует контент\nи пользователей")
Person(mobile, "Мобильный пользователь", "Использует мобильное\nприложение платформы")

System(jobportal, "JobPortal (Микросервисы)", "Система из 6 независимых микросервисов.\nКаждый масштабируется и развёртывается\nавтономно. Связь через API Gateway\nи EventBus.")

System_Ext(smtp, "SMTP-провайдер", "Отправка email-уведомлений")
System_Ext(payment, "Платёжный шлюз", "Stripe / ЮКасса.\nОбработка платежей")

Rel(jobseeker, jobportal, "Использует", "HTTPS/REST")
Rel(employer, jobportal, "Использует", "HTTPS/REST")
Rel(admin, jobportal, "Администрирует", "HTTPS/REST")
Rel(mobile, jobportal, "Использует", "HTTPS/REST")
Rel(jobportal, smtp, "Отправляет письма", "SMTP")
Rel(jobportal, payment, "Проводит платежи", "HTTPS/API")

@enduml
```

---

## 3. C4 — Диаграмма контейнеров: СТАРАЯ архитектура (MVC Монолит)

```plantuml
@startuml C4_Container_Old
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Container.puml

LAYOUT_WITH_LEGEND()

title C4 Containers — JobPortal (MVC Монолит, Лаб. работа №7)

Person(user, "Пользователь", "Соискатель, Работодатель\nили Администратор")

System_Boundary(monolith, "JobPortal — Монолитное Java-приложение") {

    Container(controllers, "Controller Layer", "Java",
        "UserController\nRecordController\nAdministratorController\n\nОбрабатывают запросы, координируют\nбизнес-логику")

    Container(models, "Model Layer", "Java",
        "User, UserImpl, UserFactory\nRecord (abstract)\nResumeImpl, VacancyImpl\nRecordFactory (Factory Method)\n\nДоменные объекты и фабрики")

    Container(security, "Security Layer", "Java / BCrypt / AES",
        "SecurityService (interface)\nSecurityServiceImpl\n\nАутентификация, авторизация,\nшифрование данных")

    Container(repositories, "Repository Layer", "Java / JDBC",
        "UserDataRepository\nRecordDataRepository\n\nРабота с базой данных,\nшифрование при хранении")

    Container(services, "Service Layer", "Java / JavaMail",
        "EmailSystem\nPaymentSystem (Singleton)\n\nВнешние интеграции")
}

SystemDb_Ext(db, "Единая SQL БД", "PostgreSQL / MySQL.\nВсе таблицы в одной схеме.")
System_Ext(smtp, "SMTP", "Email-уведомления")
System_Ext(payment_gw, "Платёжная система", "Внешний API")

Rel(user, controllers, "HTTP-запросы", "HTTP")
Rel(controllers, models, "Создаёт / использует")
Rel(controllers, security, "Аутентификация / авторизация")
Rel(controllers, services, "Уведомления, платежи")
Rel(security, repositories, "Получает данные пользователей")
Rel(repositories, db, "CRUD-операции", "JDBC/SQL")
Rel(services, smtp, "Отправка писем", "SMTP")
Rel(services, payment_gw, "Платёж", "HTTPS")

@enduml
```

---

## 4. C4 — Диаграмма контейнеров: НОВАЯ архитектура (Микросервисы)

```plantuml
@startuml C4_Container_New
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Container.puml

LAYOUT_LEFT_RIGHT()
LAYOUT_WITH_LEGEND()

title C4 Containers — JobPortal (Микросервисы, Лаб. работа №8)

Person(user, "Пользователь", "Соискатель, Работодатель,\nАдминистратор")

System_Boundary(jobportal, "JobPortal — Микросервисная система") {

    Container(gateway, "API Gateway", "Java",
        "ApiGateway\n\nЕдиная точка входа.\nМаршрутизация запросов\nк нужному сервису.")

    Container(eventbus, "EventBus", "Java (in-memory)\n/ Kafka в production",
        "Publisher-Subscriber.\nСлабосвязанная коммуникация\nмежду сервисами.\nСобытия: UserRegistered,\nRecordCreated, PaymentCompleted")

    Container(usersvc, "UserService", "Java",
        "UserController\nUserRepository\nmodel.User\n\nРегистрация, профиль\nпользователей")

    Container(recordsvc, "RecordService", "Java",
        "RecordController\nRecordRepository\nJobRecord, VacancyImpl,\nResumeImpl, Factories\n\nВакансии и резюме")

    Container(securitysvc, "SecurityService", "Java / BCrypt / AES / JWT",
        "SecurityService (interface)\nSecurityServiceImpl\n\nАутентификация,\nавторизация, JWT-токены")

    Container(notifysvc, "NotificationService", "Java / JavaMail",
        "NotificationService\n\nПодписан на EventBus.\nОтправляет email при\nрегистрации, создании\nзаписи, оплате")

    Container(paymentsvc, "PaymentService", "Java (Singleton)",
        "PaymentService\n\nОбработка платежей.\nПубликует PaymentCompleted\nв EventBus")

    Container(adminsvc, "AdminService", "Java",
        "AdminController\n\nУдаление пользователей\nи записей. Требует\nроль ADMIN")

    ContainerDb(usersdb, "Users DB", "PostgreSQL",
        "Таблицы: users, security_log.\nЗашифрованные данные.")

    ContainerDb(recordsdb, "Records DB", "PostgreSQL",
        "Таблицы: records.\nВакансии и резюме.")
}

System_Ext(smtp, "SMTP-провайдер", "Внешний email-сервис")
System_Ext(payment_gw, "Платёжный шлюз", "Stripe / ЮКасса")

Rel(user, gateway, "HTTP-запросы", "HTTPS/REST")
Rel(gateway, usersvc, "POST /auth/*", "internal")
Rel(gateway, recordsvc, "POST /records", "internal")
Rel(gateway, adminsvc, "DELETE /admin/*", "internal")
Rel(gateway, securitysvc, "Проверка токена", "internal")

Rel(usersvc, securitysvc, "registerUser / authenticate")
Rel(usersvc, usersdb, "CRUD", "JDBC")

Rel(recordsvc, recordsdb, "CRUD", "JDBC")
Rel(recordsvc, securitysvc, "authorizeAction")

Rel(adminsvc, usersvc, "deleteUser")
Rel(adminsvc, recordsvc, "deleteRecord")
Rel(adminsvc, securitysvc, "authorizeAction")

Rel(securitysvc, eventbus, "publish(UserRegisteredEvent)")
Rel(recordsvc, eventbus, "publish(RecordCreatedEvent)")
Rel(paymentsvc, eventbus, "publish(PaymentCompletedEvent)")

Rel(notifysvc, eventbus, "subscribe(все события)", "async")
Rel(notifysvc, smtp, "sendEmail()", "SMTP")
Rel(paymentsvc, payment_gw, "processPayment()", "HTTPS")

@enduml
```

---

## 5. 4+1 — Логическая перспектива (Class Diagram)

```plantuml
@startuml Logical_View
skinparam classAttributeIconSize 0
skinparam packageStyle rectangle
skinparam linetype ortho

title 4+1 Logical View — Диаграмма классов (Микросервисы)

package "events" #LightYellow {
    abstract class Event {
        - eventId: String
        - occurredAt: Instant
        + getEventType(): String
    }
    interface EventHandler<T extends Event> {
        + handle(event: T): void
    }
    class EventBus {
        - instance: EventBus {static}
        - handlers: Map<String, List<EventHandler>>
        + getInstance(): EventBus {static}
        + subscribe(eventType: String, handler: EventHandler): void
        + publish(event: Event): void
    }
    class UserRegisteredEvent extends Event {
        - userId: String
        - email: String
        - role: String
        + getEventType(): String
    }
    class RecordCreatedEvent extends Event {
        - recordId: String
        - ownerId: String
        - recordType: String
        + getEventType(): String
    }
    class PaymentCompletedEvent extends Event {
        - userId: String
        - recordId: String
        - amount: double
        + getEventType(): String
    }
}

package "gateway" #LightBlue {
    class ApiGateway {
        - userController: UserController
        - recordController: RecordController
        - adminController: AdminController
        + handleLogin(email, password): String
        + handleRegister(email, password, role): String
        + handleCreateRecord(userId, ...): void
        + handleDeleteUser(adminId, targetId): void
    }
}

package "userservice" #LightGreen {
    class UserController {
        - securityService: SecurityService
        + login(email, password): String
        + register(email, password, role): String
        + canAccessResource(userId, role): boolean
    }
    class User {
        - id: String
        - encryptedEmail: String
        - encryptedPasswordHash: String
        - encryptedRole: String
    }
    class UserRepository {
        - connection: Connection
        + save(user: User): void
        + findById(userId: String): User
        + findByEmail(email: String): User
        + deleteById(userId: String): void
        + logSecurityEvent(...): void
    }
}

package "recordservice" #LightCoral {
    class RecordController {
        - recordFactory: RecordFactory
        - recordRepository: RecordRepository
        - securityService: SecurityService
        - eventBus: EventBus
        + registerRecord(userId, ...): void
        + promoteRecord(userId, record): void
    }
    abstract class JobRecord {
        - id: String
        - nonSpecificData: Object
    }
    abstract class RecordFactory {
        + createRecord(nonSpecific, specific): JobRecord
        # getRecordWithNonSpecificData(data): JobRecord
        # getRecordWithSpecificData(record, data): JobRecord
    }
    interface IVacancy {
        + setVacancySpecificData(data): void
    }
    interface IResume {
        + setResumeSpecificData(data): void
    }
    class VacancyImpl extends JobRecord implements IVacancy
    class ResumeImpl extends JobRecord implements IResume
    class VacancyFactoryImpl extends RecordFactory
    class ResumeFactoryImpl extends RecordFactory
    class RecordRepository {
        - connection: Connection
        + insertRecord(record: JobRecord): void
        + updateRecord(record: JobRecord): void
        + deleteRecord(recordId: String): void
    }
}

package "securityservice" #Lavender {
    interface SecurityService {
        + hasRole(userId, role): boolean
        + authenticate(email, password): String
        + registerUser(email, password, role): String
        + authorizeAction(userId, requiredRole): boolean
    }
    class SecurityServiceImpl implements SecurityService {
        - userRepository: UserRepository
        - eventBus: EventBus
        - SECRET_KEY: String {static}
        + authenticate(email, password): String
        + registerUser(email, password, role): String
        # encrypt(data): String
        # decrypt(data): String
        # generateToken(userId): String
    }
}

package "notificationservice" #PeachPuff {
    class NotificationService {
        - eventBus: EventBus
        + sendEmail(to, subject, text): void
        - subscribeToEvents(): void
    }
}

package "paymentservice" #Wheat {
    class PaymentService {
        - instance: PaymentService {static}
        - eventBus: EventBus
        + getInstance(eventBus): PaymentService {static}
        + processPayment(userId, recordId, amount): boolean
        - callExternalPaymentProvider(...): boolean
    }
}

package "adminservice" #LightGray {
    class AdminController {
        - userRepository: UserRepository
        - recordRepository: RecordRepository
        - securityService: SecurityService
        + deleteUser(adminId, targetId): void
        + deleteRecord(adminId, recordId): void
    }
}

' Связи
ApiGateway --> UserController
ApiGateway --> RecordController
ApiGateway --> AdminController

UserController --> SecurityService
SecurityServiceImpl --> UserRepository
SecurityServiceImpl --> EventBus

RecordController --> RecordFactory
RecordController --> RecordRepository
RecordController --> SecurityService
RecordController --> EventBus

AdminController --> UserRepository
AdminController --> RecordRepository
AdminController --> SecurityService

NotificationService --> EventBus
PaymentService --> EventBus

EventBus --> EventHandler

@enduml
```

---

## 6. 4+1 — Перспектива процессов: Регистрация пользователя (Sequence)

```plantuml
@startuml Process_View_Register
skinparam sequenceMessageAlign center

title 4+1 Process View — Последовательность: Регистрация пользователя

actor "Клиент\n(Web/Mobile)" as Client
participant "API Gateway" as GW
participant "UserController\n[UserService]" as UC
participant "SecurityService\n[SecurityService]" as SS
participant "UserRepository\n[UserService]" as UR
participant "EventBus" as EB
participant "NotificationService" as NS

Client -> GW : POST /auth/register\n{email, password, role}
activate GW

GW -> UC : handleRegister(email, password, role)
activate UC

UC -> SS : registerUser(email, password, role)
activate SS

SS -> SS : BCrypt.hashpw(password)
SS -> SS : AES.encrypt(email, hash, role)

SS -> UR : save(newUser)
activate UR
UR --> SS : OK
deactivate UR

SS -> EB : publish(UserRegisteredEvent)
activate EB

EB -> NS : handle(UserRegisteredEvent)
activate NS
NS --> NS : sendEmail(email,\n"Добро пожаловать!")
deactivate NS

EB --> SS : (async)
deactivate EB

SS -> SS : generateToken(userId)
SS --> UC : JWT-токен
deactivate SS

UC --> GW : JWT-токен
deactivate UC

GW --> Client : HTTP 200\n{token: "eyJ..."}
deactivate GW

@enduml
```

---

## 7. 4+1 — Перспектива процессов: Продвижение вакансии (Sequence)

```plantuml
@startuml Process_View_Payment
skinparam sequenceMessageAlign center

title 4+1 Process View — Последовательность: Продвижение вакансии

actor "Работодатель" as Employer
participant "API Gateway" as GW
participant "RecordController\n[RecordService]" as RC
participant "SecurityService" as SS
participant "RecordRepository\n[RecordService]" as RR
participant "PaymentService" as PS
participant "EventBus" as EB
participant "NotificationService" as NS

Employer -> GW : POST /records/{id}/promote\n{Authorization: Bearer JWT}
activate GW

GW -> SS : verifyToken(JWT)
SS --> GW : userId

GW -> RC : promoteRecord(userId, record)
activate RC

RC -> SS : authorizeAction(userId, "EMPLOYER")
SS --> RC : true

RC -> RR : updateRecord(record)
activate RR
RR --> RC : OK
deactivate RR

RC -> PS : processPayment(userId, recordId, 299.0)
activate PS
PS -> PS : callExternalPaymentProvider()
PS -> EB : publish(PaymentCompletedEvent)
activate EB

EB -> NS : handle(PaymentCompletedEvent)
activate NS
NS --> NS : notifyUser("Платёж принят")
deactivate NS

EB --> PS : (async)
deactivate EB

PS --> RC : true
deactivate PS

RC --> GW : OK
deactivate RC

GW --> Employer : HTTP 200\n{status: "promoted"}
deactivate GW

@enduml
```

---

## 8. 4+1 — Перспектива разработки (Component Diagram)

```plantuml
@startuml Development_View
skinparam componentStyle rectangle
skinparam linetype ortho

title 4+1 Development View — Компонентная диаграмма

package "org.example" {

    component [Main.java\n(точка входа)] as Main

    package "gateway" {
        component [ApiGateway] as GW
    }

    package "events" {
        component [EventBus] as EB
        component [Event (abstract)] as Ev
        component [UserRegisteredEvent] as UE
        component [RecordCreatedEvent] as RE
        component [PaymentCompletedEvent] as PE
    }

    package "userservice" {
        component [UserController] as UC
        package "userservice.model" {
            component [User] as UM
        }
        package "userservice.repository" {
            component [UserRepository] as UR
        }
    }

    package "recordservice" {
        component [RecordController] as RC
        package "recordservice.model" {
            component [JobRecord (abstract)] as JR
            component [VacancyImpl] as VI
            component [ResumeImpl] as RI
            component [RecordFactory (abstract)] as RF
            component [VacancyFactoryImpl] as VF
            component [ResumeFactoryImpl] as REF
            component [IVacancy] as IV
            component [IResume] as IR
        }
        package "recordservice.repository" {
            component [RecordRepository] as RR
        }
    }

    package "securityservice" {
        component [SecurityService <<interface>>] as SSI
        component [SecurityServiceImpl] as SS
    }

    package "notificationservice" {
        component [NotificationService] as NS
    }

    package "paymentservice" {
        component [PaymentService] as PS
    }

    package "adminservice" {
        component [AdminController] as AC
    }
}

Main --> GW
Main --> EB
Main --> NS
Main --> PS

GW --> UC
GW --> RC
GW --> AC

UC --> SSI
RC --> SSI
RC --> RF
RC --> RR
RC --> EB
AC --> UR
AC --> RR
AC --> SSI

SS ..|> SSI
SS --> UR
SS --> EB

NS --> EB
PS --> EB

VI ..|> IV
RI ..|> IR
VF --|> RF
REF --|> RF
VI --|> JR
RI --|> JR

UE --|> Ev
RE --|> Ev
PE --|> Ev

@enduml
```

---

## 9. 4+1 — Физическая перспектива (Deployment Diagram)

```plantuml
@startuml Physical_View
skinparam linetype ortho

title 4+1 Physical View — Диаграмма развёртывания (целевая production-конфигурация)

node "Load Balancer\n(Nginx)" as LB {
}

node "API Gateway\n(Docker Container)" as GW_NODE {
    artifact "api-gateway.jar"
}

node "UserService\nInstance 1" as US1 {
    artifact "user-service.jar"
}
node "UserService\nInstance 2" as US2 {
    artifact "user-service.jar"
}

node "RecordService\nInstance 1" as RS1 {
    artifact "record-service.jar"
}
node "RecordService\nInstance 2" as RS2 {
    artifact "record-service.jar"
}
node "RecordService\nInstance 3" as RS3 {
    artifact "record-service.jar"
}

node "SecurityService\nInstance 1" as SS1 {
    artifact "security-service.jar"
}
node "SecurityService\nInstance 2" as SS2 {
    artifact "security-service.jar"
}

node "NotificationService" as NS_NODE {
    artifact "notification-service.jar"
}

node "PaymentService" as PS_NODE {
    artifact "payment-service.jar"
}

node "AdminService" as AS_NODE {
    artifact "admin-service.jar"
}

node "Kafka Cluster\n(EventBus)" as KAFKA {
    artifact "Kafka Broker"
}

database "Users DB\n(PostgreSQL Primary)" as UDB {
}
database "Users DB\n(PostgreSQL Replica)" as UDB_R {
}

database "Records DB\n(PostgreSQL Primary)" as RDB {
}
database "Records DB\n(PostgreSQL Replica)" as RDB_R {
}

cloud "SMTP Provider\n(SendGrid)" as SMTP
cloud "Payment Gateway\n(Stripe)" as PGW

LB --> GW_NODE : HTTPS

GW_NODE --> US1 : HTTP
GW_NODE --> US2 : HTTP
GW_NODE --> RS1 : HTTP
GW_NODE --> RS2 : HTTP
GW_NODE --> RS3 : HTTP
GW_NODE --> SS1 : HTTP
GW_NODE --> SS2 : HTTP
GW_NODE --> AS_NODE : HTTP

US1 --> UDB : JDBC
US2 --> UDB : JDBC
UDB --> UDB_R : репликация

RS1 --> RDB : JDBC
RS2 --> RDB : JDBC
RS3 --> RDB : JDBC
RDB --> RDB_R : репликация

US1 --> KAFKA : publish
RS1 --> KAFKA : publish
PS_NODE --> KAFKA : publish
SS1 --> KAFKA : publish

NS_NODE --> KAFKA : subscribe
NS_NODE --> SMTP : SMTP

PS_NODE --> PGW : HTTPS

@enduml
```

---

## 10. 4+1 — Сценарии / Use Cases (+1)

```plantuml
@startuml Scenarios_View
left to right direction
skinparam actorStyle awesome

title 4+1 Scenarios View — Диаграмма прецедентов (Use Cases)

actor "Соискатель" as JS
actor "Работодатель" as EM
actor "Администратор" as AD
actor "Платёжная система" as PAY <<external>>
actor "Email-провайдер" as SMTP <<external>>

rectangle "JobPortal (Микросервисы)" {
    usecase "UC-01\nРегистрация\nпользователя" as UC1
    usecase "UC-02\nАутентификация\n(логин)" as UC2
    usecase "UC-03\nПубликация резюме" as UC3
    usecase "UC-04\nПубликация вакансии" as UC4
    usecase "UC-05\nПродвижение вакансии\n(оплата)" as UC5
    usecase "UC-06\nПоиск вакансий\n/ резюме" as UC6
    usecase "UC-07\nУдаление пользователя" as UC7
    usecase "UC-08\nУдаление записи" as UC8
    usecase "UC-09\nОтправка\nuEmail-уведомления" as UC9
}

JS --> UC1
JS --> UC2
JS --> UC3
JS --> UC6

EM --> UC1
EM --> UC2
EM --> UC4
EM --> UC5
EM --> UC6

AD --> UC2
AD --> UC7
AD --> UC8

UC5 --> PAY : <<include>>
UC1 --> UC9 : <<include>>
UC4 --> UC9 : <<include>>
UC5 --> UC9 : <<include>>
UC9 --> SMTP : <<include>>

@enduml
```

---

## Итого: список диаграмм

| № | Название | Раздел отчёта |
|---|----------|---------------|
| 1 | C4 Context — Старая архитектура | C4, раздел 5.1 |
| 2 | C4 Context — Новая архитектура | C4, раздел 5.1 |
| 3 | C4 Containers — Старая архитектура | C4, раздел 5.2 |
| 4 | C4 Containers — Новая архитектура | C4, раздел 5.2 |
| 5 | Class Diagram (Logical View) | 4+1, раздел 6.1 |
| 6 | Sequence: Регистрация (Process View) | 4+1, раздел 6.2 |
| 7 | Sequence: Продвижение вакансии (Process View) | 4+1, раздел 6.2 |
| 8 | Component Diagram (Development View) | 4+1, раздел 6.3 |
| 9 | Deployment Diagram (Physical View) | 4+1, раздел 6.4 |
| 10 | Use Case Diagram (Scenarios +1) | 4+1, раздел 6.5 |
