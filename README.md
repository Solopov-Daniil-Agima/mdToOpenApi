# ТЗ → OpenAPI

Автоматизация для PHP/Bitrix-разработчика: из технического задания получить черновик **OpenAPI 3.0.3**.

---

## Требования

| Компонент | Версия |
|-----------|--------|
| **Python** | **3.11+** (рекомендуется **3.12**) |
| **pypdf** | только для PDF; ставится через `pip` (см. ниже) |

Скрипты конвертации DOCX используют только стандартную библиотеку Python.
### Зависимости для PDF (опционально)

Нужны только если конвертируешь `.pdf`. Один раз из корня проекта:

```powershell
pip install -r scripts/requirements.txt
```

---

## Что на входе и выходе

| | |
|---|---|
| **Вход** | Файл ТЗ в `input/` — `.md`, `.txt`, `.docx` или `.pdf` |
| **Выход 1** | `output/{имя}-analysis.md` — структурированный разбор |
| **Выход 2** | `output/{имя}-openapi.yaml` — спецификация API |

Папка `output/` в `.gitignore` — артефакты генерируются локально.

---

## Быстрый старт

### Шаг 1. Конвертация (если не `.md`)

AI-агент **не читает `.docx` и `.pdf` напрямую**. Сначала конвертируй:

```powershell
# DOCX — без доп. зависимостей
python scripts/docx-to-md.py "input/my-spec.docx"

# PDF — сначала pip install -r scripts/requirements.txt
python scripts/pdf-to-md.py "input/my-spec.pdf"
```

Появится `input/my-spec.md` (то же имя, расширение `.md`). Явный путь: `-o input/my-spec.md`.

### Шаг 2. Запуск пайплайна

В чате AI-агента (IDE):

```
Прочитай @AGENTS.md и выполни пайплайн TZ → OpenAPI для @input/my-spec.md

1. Разбор по @templates/tz-extraction-checklist.md → output/my-spec-analysis.md
2. OpenAPI по @templates/openapi-base.yaml → output/my-spec-openapi.yaml

Роли: @.claude/agents/tz-analyst.md и @.claude/agents/openapi-architect.md
```

**Slash-команда:**

```
/tz-to-openapi @input/my-spec.md
```

### Шаг 3. Проверка

1. `output/my-spec-analysis.md` — endpoints, модели, TODO
2. `output/my-spec-openapi.yaml` — спецификация; preview в IDE (расширение OpenAPI/Swagger)
3. [Swagger Editor](https://editor.swagger.io/) — визуальная проверка в браузере

---

## Пайплайн

```text
input/spec.docx | spec.pdf
    │
    ▼  docx-to-md.py | pdf-to-md.py
input/spec.md
    │
    ▼  tz-analyst
output/spec-analysis.md
    │
    ▼  openapi-architect
output/spec-openapi.yaml
```

| Файл | Назначение |
|------|------------|
| `AGENTS.md` | Контекст проекта и соглашения API |
| `scripts/docx-to-md.py` | DOCX → Markdown (stdlib) |
| `scripts/pdf-to-md.py` | PDF → Markdown (pypdf) |
| `scripts/requirements.txt` | Зависимости для PDF-конвертера |
| `templates/tz-extraction-checklist.md` | Чек-лист разбора ТЗ |
| `templates/openapi-base.yaml` | Минимальный каркас OpenAPI 3.0.3 (`info` + `paths`) |
| `.claude/agents/` | Суб-агенты analyst + architect |
| `.claude/commands/tz-to-openapi.md` | Slash-команда |

---

## Частые проблемы

| Проблема | Решение |
|----------|---------|
| `python` не найден | Переустанови Python с галочкой **Add to PATH** или используй `py -3.12` |
| Агент не видит docx/pdf | Конвертируй в `.md` скриптами из `scripts/` |
| PDF пустой | Скан без текстового слоя — нужен OCR |
| `No module named pypdf` | `pip install -r scripts/requirements.txt` |
| OpenAPI preview не открывается | Невалидный YAML: строки с `TODO:` в кавычках, у schema обязателен `type` |
| Таблицы в md «кривые» | Поправь `.md` вручную после конвертации |

---
