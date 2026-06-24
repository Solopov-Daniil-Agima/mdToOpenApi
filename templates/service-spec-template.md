# Service Specification: {{SERVICE_NAME}}

> Промежуточный документ по популярному шаблону **API Design Document** (используется в Swagger/OpenAPI ecosystem, Zalando Guidelines, GitHub API docs).  
> Заполняется после разбора ТЗ, перед генерацией `openapi.yaml`.

---

## 1. Overview

| Поле | Значение |
|------|----------|
| **Service** | {{SERVICE_NAME}} |
| **Version** | {{VERSION}} |
| **Owner** | {{OWNER}} |
| **Status** | Draft |

### 1.1 Purpose

{{PURPOSE}}

### 1.2 Scope

**In scope:**  
{{IN_SCOPE}}

**Out of scope:**  
{{OUT_OF_SCOPE}}

---

## 2. Architecture Context

```text
[Client / Mobile App] --> [API Gateway / Bitrix Module] --> [{{SERVICE_NAME}}] --> [DB / External systems]
```

### 2.1 Dependencies

- {{DEPENDENCY_1}}
- {{DEPENDENCY_2}}

---

## 3. API Conventions

| Convention | Value |
|------------|-------|
| Base URL | `{{BASE_URL}}` |
| API Version | `v1` |
| Content-Type | `application/json` |
| Charset | `UTF-8` |
| Date format | ISO 8601 `date-time` |

### 3.1 Authentication

{{AUTH_DESCRIPTION}}

### 3.2 Authorization

{{AUTHORIZATION_ROLES}}

### 3.3 Rate Limiting

{{RATE_LIMITS}}

---

## 4. Resources

### 4.1 {{RESOURCE_NAME_1}}

| Method | Path | Summary | Auth |
|--------|------|---------|------|
| GET | `/api/v1/...` | … | … |
| POST | `/api/v1/...` | … | … |

#### Request / Response

{{REQUEST_RESPONSE_DETAILS}}

---

## 5. Data Models

### 5.1 {{ModelName}}

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | string (uuid) | yes | … |

### 5.2 Enumerations

| Enum | Values |
|------|--------|
| {{StatusEnum}} | `draft`, `submitted`, … |

---

## 6. Error Handling

Стандартный формат ошибки:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Human readable message",
    "details": []
  }
}
```

| HTTP | code | When |
|------|------|------|
| 400 | VALIDATION_ERROR | … |
| 401 | UNAUTHORIZED | … |
| 403 | FORBIDDEN | … |
| 404 | NOT_FOUND | … |
| 500 | INTERNAL_ERROR | … |

---

## 7. Open Questions (TODO)

- [ ] {{TODO_1}}
- [ ] {{TODO_2}}

---

## 8. Mapping to OpenAPI

| Spec section | OpenAPI location |
|--------------|------------------|
| Resources | `paths` |
| Models | inline `schema` в `requestBody` / `responses` |
| Auth | `security` на уровне operation (если указано в ТЗ) |
| Errors | inline `schema` в `responses` (если указано в ТЗ) |
