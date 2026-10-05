# Multilingual Resume Builder (Генератор мультиязычных резюме)

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![RenderCV](https://img.shields.io/badge/RenderCV-v2.6%2B-orange.svg)](https://docs.rendercv.com/)
[![Typst](https://img.shields.io/badge/Typst-Powered-239dad.svg)](https://typst.app/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![English Docs](https://img.shields.io/badge/docs-English_Version-blue.svg)](README.md)

> Удобная и расширяемая обёртка над **[RenderCV](https://docs.rendercv.com/)** и **[Typst](https://typst.app/docs/)** для быстрого ведения, синхронизации и пакетной сборки резюме на разных языках под разные специализации и вакансии с использованием веток Git.

[🇬🇧 Read in English](README.md)

---

## 🎯 Назначение и концепция проекта

При активном поиске работы специалисту часто требуется:
1. **Вести резюме сразу на нескольких языках** (например, русский, английский, испанский, немецкий) и при обновлении опыта не забывать обновлять каждую языковую версию.
2. **Адаптировать резюме под разные квалификации и вакансии** (например, *Python Backend*, *Data Platform*, *Web Scraping*, *Technical Support* или инженерные специальности вроде *Вентиляция и ОВиК*), не плодя хаос в папках и файлах.

Этот репозиторий решает эти задачи через строгую и элегантную архитектуру:
- **Единые файлы заготовок**: Каждый язык представлен отдельным файлом с двухбуквенным кодом стандарта ISO (например, `RU.yaml`, `EN.yaml`, `ES.yaml`).
- **Автоматическое обнаружение языков**: Скрипт `main.py` сканирует папку заготовок, достаёт имя кандидата из YAML и собирает все языки одной командой. Добавили `DE.yaml` — скрипт сразу найдет его и сгенерирует немецкую версию!
- **Ветки Git под специализации**: Разные профессиональные роли ведутся в соответствующих ветках (`dev/py`, `dev/scraping`, `eng/senior_ventilation`). Это даёт чистый git-diff и изоляцию изменений под конкретные вакансии.

---

## 📁 Структура проекта

```text
resume-builder/
├── .agents/
│   └── skills/
│       └── resume-builder/
│           └── SKILL.md               # Навык для AI-агентов (Antigravity IDE, Cursor и др.)
├── src/resume_builder/
│   ├── img/
│   │   └── portrait.jpg               # Фотография для резюме (важное имя, не менять!)
│   └── rendercv/master/
│       ├── RU.yaml                    # Резюме на русском языке
│       ├── EN.yaml                    # Резюме на английском языке
│       ├── ES.yaml                    # Резюме на испанском языке
│       ├── fonts/                     # Пользовательские шрифты (например, Exo 2)
│       └── rendercv_output/           # Папка с результатами сборки
│           ├── _john_doe_en.pdf
│           ├── _john_doe_en.typ
│           ├── _иван_иванов_ru.pdf
│           └── ...
├── main.py                            # Скрипт автопоиска языков и генерации
├── pyproject.toml                     # Зависимости проекта (RenderCV, PyYAML, Pydantic)
├── uv.lock                            # Зафиксированные версии зависимостей
├── README.md                          # Документация (на английском языке)
└── README.RU.md                       # Документация (на русском языке)
```

### 📌 Важные правила именования (не ломать)
1. **`src/resume_builder/img/portrait.jpg`** — универсальное имя и расположение файла фотографии. В YAML-файлах ссылка на фото указывается относительно файла резюме:
   ```yaml
   photo: "../../img/portrait.jpg"
   ```
2. **`[ISO].yaml` (например, `RU.yaml`, `EN.yaml`, `ES.yaml`, `DE.yaml`)** — файлы заготовок резюме именуются двухбуквенным кодом языка в верхнем регистре (upper case) по стандарту [ISO 639-1](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes).
3. **Имена выходных файлов в `rendercv_output/`** — формируются автоматически по шаблону:
   `_{имя_из_yaml}_{код_языка}.{расширение}` в нижнем регистре (lower case).  
   *Пример:* `_john_doe_en.pdf`, `_иван_иванов_ru.pdf`.

---

## 🚀 Быстрый старт с `uv`

Для управления зависимостями и виртуальным окружением рекомендуется использовать **[uv](https://docs.astral.sh/uv/)** — современный и сверхбыстрый пакетный менеджер для Python.

### 1. Установка зависимостей

Клонируйте репозиторий и выполните синхронизацию окружения:

```bash
# Клонирование репозитория
git clone https://github.com/your-username/resume-builder.git
cd resume-builder

# Установка зависимостей одной командой
uv sync
```

*(Если у вас пока не установлен `uv`, его можно поставить командой `curl -LsSf https://astral.sh/uv/install.sh | sh` либо использовать стандартный `pip install -e .`)*

---

### 2. Сборка всех резюме в один клик

Запустите скрипт сборки:

```bash
uv run python main.py
```

Скрипт автоматически:
1. Просканирует папку `src/resume_builder/rendercv/master/`.
2. Найдёт все файлы языков (например `EN`, `ES`, `RU`).
3. Извлечёт имя кандидата из поля `cv.name`.
4. Сгенерирует по умолчанию готовые файлы **PDF** (`.pdf`).  
   *(Если вам нужны исходники Typst, укажите флаг `-f pdf,typ` или `--output-format all`)*.

Готовые файлы появятся в директории:
`src/resume_builder/rendercv/master/rendercv_output/`

---

### 3. Опции запуска и флаги CLI

#### Сборка только одного языка:
Флаг `--lang` (или `-l`) позволяет выбрать конкретный язык (регистр не важен):
```bash
# Только русский
uv run python main.py --lang ru

# Только английский
uv run python main.py --lang en

# Только испанский
uv run python main.py --lang es
```

#### Выбор форматов вывода:
RenderCV поддерживает форматы `pdf`, `typ` (`typst`), `html`, `md` (`markdown`), `png`. Флаг `--output-format` (или `-f`) позволяет задать нужные типы файлов через запятую, пробел или указать флаг несколько раз, а также поддерживает значение `all`:

```bash
# Собрать только PDF (без typst):
uv run python main.py --output-format pdf

# Собрать PDF и HTML:
uv run python main.py --output-format pdf,html

# Сгенерировать сразу ВСЕ форматы (PDF, Typst, HTML, Markdown, PNG):
uv run python main.py --output-format all

# Комбинация языка и нескольких флагов формата:
uv run python main.py --lang en -f pdf -f html
```

---

## 🌿 Ведение вакансий и специализаций через Git

Вместо того чтобы поддерживать громоздкую общую ветку `core` или плодить дубликаты папок, каждая профессиональная специализация ведётся в отдельной независимой ветке Git:

```text
├── dev/py                   # Python Backend, High-Load, Data Pipelines
├── dev/scraping             # Веб-скрейпинг, Парсинг, ETL-конвейеры
├── dev/technical_l2_support  # Техническая поддержка L2/L3, SRE, Observability
└── eng/senior_ventilation   # Инженерные системы, ОВиК и вентиляция
```

### Быстрый справочник по Git

```bash
# 1. Посмотреть все существующие ветки
git branch -a

# 2. Переключиться на нужную роль
git switch dev/py

# 3. Создать новую ветку под новую специальность или компанию
git switch -c dev/ai-platform

# 4. Внести правки в заготовки RU.yaml, EN.yaml, ES.yaml, собрать и закоммитить:
uv run python main.py
git status
git commit -am "feat(cv): адаптировал опыт под требования платформы данных"
```

### Обновление общих данных во всех ветках
Если у вас изменился телефон, email, Telegram, ссылка на соцсети или фото:
- Достаточно попросить AI-агента:  
  > *"Обнови мой номер телефона и email во всех активных ветках (`dev/py`, `dev/scraping`, `dev/technical_l2_support`, `eng/senior_ventilation`)."*
- Агент сам переключится по очереди на каждую ветку и внесет точечные коммиты.

---

## 🤖 Прокачанный воркфлоу с AI: Jina Reader и `/grill-me`

### 💡 Лайфхак: Чистый Markdown вакансии через Jina Reader (`r.jina.ai`)
Когда вы находите вакансию на HeadHunter, LinkedIn, Habr Карьере или сайте работодателя, в ней куча визуального мусора: реклама, меню, cookie-баннеры и скрипты. Нейросети гораздо проще и точнее работать с чистым Markdown.

**Супер-простой способ получить чистый текст:**
1. В адресной строке браузера перед URL вакансии добавьте `https://r.jina.ai/`:
   ```text
   https://r.jina.ai/https://hh.ru/vacancy/12345678
   ```
2. Jina Reader моментально распарсит страницу и отдаст вам структурированный Markdown без лишнего шума.
3. Скопируйте полученный текст и отправьте агенту!

### Калибровка резюме через `/grill-me`
1. Скиньте Markdown вакансии агенту и запустите команду `/grill-me`.
2. Агент проведёт с вами глубокое техническое интервью:
   - Сопоставит ваш стек с требованиями работодателя и выявит пробелы.
   - Задаст наводящие вопросы по вашим прошлым проектам, чтобы вытащить реальные оцифрованные метрики (RPS, latency, SLA, экономия бюджета).
   - Поможет сформулировать сильные буллеты для секции опыта.
3. Внесите изменения параллельно в `RU.yaml`, `EN.yaml` и `ES.yaml` и выполните сборку: `uv run python main.py`.

---

## 🖼️ Как заменить или отключить фотографию (портрет)

### 1. Замена фотографии на свою
1. Подготовьте вертикальный портрет в формате JPG.
2. Замените файл по пути:
   `src/resume_builder/img/portrait.jpg`
3. В файлах резюме `RU.yaml`, `EN.yaml`, `ES.yaml` убедитесь, что указан относительный путь:
   ```yaml
   cv:
     photo: "../../img/portrait.jpg"
   ```

### 2. Как полностью отключить фото (текстовое резюме)
Если вы не хотите прикреплять фото (например, для англоязычных рынков США/Великобритании, где фото не принято, или если вы просто не хотите его публиковать):
- Достаточно **закомментировать** (поставив `#` в начале строки) или **удалить** поле `photo:`:
  ```yaml
  cv:
    name: Иван Иванов
    headline: "Senior Python Backend Engineer"
    location: "Москва, Россия"
    email: "ivan.ivanov@example.com"
    # photo: "../../img/portrait.jpg"   # <-- Закомментируйте эту строку
    phone: "+7 (999) 000-00-00"
  ```
RenderCV автоматически перестроит верстку документа: шапка станет строгой и текстовой во всю ширину страницы, без пустых рамок и отступов.

> **💡 Подсказка:** Точно так же можно временно отключить или скрыть любые другие поля в YAML:
> - `# phone: "+7 ..."` — скрыть телефон
> - `# location: "..."` — скрыть город проживания
> - `# website: https://...` — скрыть сайт
> - закомментировать отдельные соцсети в списке `social_networks` или целые разделы в `sections:`.

---

## 📝 Руководство: Как редактировать резюме

### 1. Где вносить изменения
Все исходные тексты находятся в каталоге `src/resume_builder/rendercv/master/`:
- `RU.yaml` — русская версия
- `EN.yaml` — английская версия
- `ES.yaml` — испанская версия
- `DE.yaml` — (при необходимости) немецкая версия и т.д.

> **💡 Важное правило**: Обновляя опыт или навыки, редактируйте **все** активные языковые файлы синхронно, чтобы ваши резюме всегда соответствовали друг другу.

### 2. Структура YAML-файла

Каждый файл содержит 4 основных блока:

#### Блок `cv:` (Личные данные и контент)
- `name`: Имя кандидата на языке файла (например, `Иван Иванов` в `RU.yaml` и `John Doe` в `EN.yaml`).
- `headline`: Ёмкое профессиональное позиционирование под роль ветки.
- `location`, `email`, `phone`, `photo`: Контактные данные.
- `social_networks`: Профили LinkedIn, GitHub, Telegram и др.
- `sections`: Содержательная часть резюме:
  - **О себе / About**: 1-2 ёмких абзаца о вашем инженерном подходе и ключевых компетенциях.
  - **Опыт / Experience**: Список мест работы (`company`, `position`, `start_date`, `end_date`, `location`, `summary`, `highlights`).
  - **Образование / Education**: Вузы, факультеты, курсы.
  - **Навыки / Skills**: Сгруппированные по категориям технологии и инструменты.

```yaml
# yaml-language-server: $schema=https://raw.githubusercontent.com/rendercv/rendercv/refs/tags/v2.6/schema.json
cv:
  name: John Doe
  headline: "Senior Backend Engineer | Cloud Architecture & Observability"
  location: "San Francisco, CA, USA"
  email: "john.doe@example.com"
  photo: "../../img/portrait.jpg"
  phone: "+1 415 555 0192"
  social_networks:
    - network: LinkedIn
      username: johndoe-example
    - network: GitHub
      username: johndoe-example
    - network: Telegram
      username: "@johndoe_example"

  sections:
    About:
      - >
        Python Backend Engineer с опытом проектирования отказоустойчивых систем...

    Experience:
      - company: ООО "Платформа"
        position: Senior Python Engineer
        start_date: 2022-03
        end_date: present
        location: Удаленно
        summary: Разработка бэкенда платформы потоковой аналитики.
        highlights:
          - "Спроектировал асинхронный сервис на FastAPI, выдерживающий до 15 000 RPS."
          - "Внедрил сквозной мониторинг на VictoriaMetrics и Vector, снизив MTTR на 40%."

    Skills:
      - label: Языки программирования
        details: Python (Asyncio, FastAPI), SQL, Bash
      - label: Хранилища и брокеры
        details: PostgreSQL, ClickHouse, Redis, RabbitMQ
```

#### Блок `design:` (Оформление и тема)
Позволяет настроить тему, шрифты, отступы и расположение фотографии:
```yaml
design:
  theme: engineeringclassic     # Выбранная тема оформления (см. раздел тем ниже)
  font_family:
    body: Source Sans 3
  header:
    photo_position: right        # Положение фото: right или left
```

#### Блок `locale:` (Языковая локаль RenderCV)
Задаёт язык встроенных системных надписей (даты, «настоящее время», разделители):
```yaml
locale:
  language: russian              # Значения: russian, english, spanish, german и др.
```

---

## 🎨 Доступные темы оформления (Themes)

RenderCV включает **9 встроенных тем оформления**. Вы можете легко менять стиль и подачу резюме без изменения текста самого документа.

```text
Доступные темы: classic (default), ember, engineeringclassic, engineeringresumes, harvard, ink, moderncv, opal, sb2nov.
```

### Сравнительная таблица тем:

| Тема | Описание и визуальные особенности | Рекомендуемое применение |
| :--- | :--- | :--- |
| **`engineeringclassic`** *(по умолчанию в проекте)* | Плотный, строгий технический стиль с максимальной эффективностью пространства и аккуратными линиями. | Разработчики, инженеры, DevOps (когда важно уместить максимум опыта) |
| **`classic`** *(дефолт RenderCV)* | Классический формат с традиционными горизонтальными линиями и акцентами. | Универсально для любых корпоративных и бизнес-позиций |
| **`engineeringresumes`** | Лаконичный стиль по канонам сообщества [r/EngineeringResumes](https://reddit.com/r/EngineeringResumes). | Технические специалисты, прохождение зарубежных ATS-систем |
| **`sb2nov`** | Популярный минималистичный шаблон для программистов (портирован из экосистемы LaTeX). | Software Engineers, Data Engineers, SRE |
| **`moderncv`** | Европейский стиль с элегантными заголовками и современным оформлением. | Рынок труда Европы (Германия, Нидерланды, Великобритания) |
| **`harvard`** | Традиционный академический и консалтинговый стиль Harvard / Ivy League. | Менеджмент, консалтинг, финансы, академическая среда |
| **`ink`** | Изящный книжный стиль с выразительной типографикой. | Аналитики, продуктовые роли, исследователи |
| **`ember`** | Современный дизайн с тёплыми акцентами и свежей композицией. | Стартапы, технологические компании |
| **`opal`** | Чистый, воздушный стиль с мягкими разделителями. | Современные IT-компании, дизайн/продукт |

### Как и где изменить тему:

#### 1. В существующих файлах резюме
Откройте нужный файл (`RU.yaml`, `EN.yaml`, `ES.yaml` и т.д.) в директории `src/resume_builder/rendercv/master/` и укажите желаемую тему в секции `design.theme`:

```yaml
design:
  theme: engineeringresumes   # Замените на любую из 9 доступных тем
```

После сохранения файла пересоберите резюме:
```bash
uv run python main.py
```

#### 2. При генерации нового файла через CLI
При создании нового шаблона с помощью команды `rendercv new` передайте флаг `--theme`:

```bash
uv run rendercv new "Иван Иванов" --theme "engineeringresumes" --locale "russian"
```

---

## 🌍 Поддерживаемые языки и сводная таблица

RenderCV поддерживает **22 языка из коробки**. Используйте эту таблицу, чтобы сразу узнать двухбуквенный код файла и значение поля `locale.language` без поиска по внешним справочникам:

| Флаг | Язык | Имя файла | Значение `locale.language:` | Команда генерации |
| :---: | :--- | :--- | :--- | :--- |
| 🇷🇺 | Русский | `RU.yaml` | `russian` | `uv run rendercv new "Имя" --locale "russian"` |
| 🇬🇧 | Английский | `EN.yaml` | `english` | `uv run rendercv new "Имя" --locale "english"` |
| 🇪🇸 | Испанский | `ES.yaml` | `spanish` | `uv run rendercv new "Имя" --locale "spanish"` |
| 🇩🇪 | Немецкий | `DE.yaml` | `german` | `uv run rendercv new "Имя" --locale "german"` |
| 🇫🇷 | Французский | `FR.yaml` | `french` | `uv run rendercv new "Имя" --locale "french"` |
| 🇮🇹 | Итальянский | `IT.yaml` | `italian` | `uv run rendercv new "Имя" --locale "italian"` |
| 🇵🇹 | Португальский | `PT.yaml` | `portuguese` | `uv run rendercv new "Имя" --locale "portuguese"` |
| 🇹🇷 | Турецкий | `TR.yaml` | `turkish` | `uv run rendercv new "Имя" --locale "turkish"` |
| 🇨🇳 | Китайский (путунхуа) | `ZH.yaml` | `mandarin_chinese` | `uv run rendercv new "Имя" --locale "mandarin_chinese"` |
| 🇯🇵 | Японский | `JA.yaml` | `japanese` | `uv run rendercv new "Имя" --locale "japanese"` |
| 🇰🇷 | Корейский | `KO.yaml` | `korean` | `uv run rendercv new "Имя" --locale "korean"` |
| 🇸🇦 | Арабский | `AR.yaml` | `arabic` | `uv run rendercv new "Имя" --locale "arabic"` |
| 🇳🇱 | Нидерландский | `NL.yaml` | `dutch` | `uv run rendercv new "Имя" --locale "dutch"` |
| 🇩🇰 | Датский | `DA.yaml` | `danish` | `uv run rendercv new "Имя" --locale "danish"` |
| 🇮🇱 | Иврит | `HE.yaml` | `hebrew` | `uv run rendercv new "Имя" --locale "hebrew"` |
| 🇮🇳 | Хинди | `HI.yaml` | `hindi` | `uv run rendercv new "Имя" --locale "hindi"` |
| 🇭🇺 | Венгерский | `HU.yaml` | `hungarian` | `uv run rendercv new "Имя" --locale "hungarian"` |
| 🇮🇩 | Индонезийский | `ID.yaml` | `indonesian` | `uv run rendercv new "Имя" --locale "indonesian"` |
| 🇳🇴 | Норвежский (букмол) | `NB.yaml` | `norwegian_bokmål` | `uv run rendercv new "Имя" --locale "norwegian_bokmål"` |
| 🇳🇴 | Норвежский (нюнорск) | `NN.yaml` | `norwegian_nynorsk` | `uv run rendercv new "Имя" --locale "norwegian_nynorsk"` |
| 🇮🇷 | Персидский (фарси) | `FA.yaml` | `persian` | `uv run rendercv new "Имя" --locale "persian"` |
| 🇻🇳 | Вьетнамский | `VI.yaml` | `vietnamese` | `uv run rendercv new "Имя" --locale "vietnamese"` |

### Создание нового файла языка:
- **Способ А (генератор CLI)**: Выполните `uv run rendercv new "Ваше Имя" --locale "turkish"`, переместите файл `Ваше_Имя_CV.yaml` в `src/resume_builder/rendercv/master/TR.yaml` и укажите `photo: "../../img/portrait.jpg"`.
- **Способ Б (копирование)**: Скопируйте `cp EN.yaml DE.yaml`, укажите `locale.language: german`, переведите содержимое и запустите сборку `uv run python main.py --lang de`.

---

## 🤖 Навык для AI-агентов (Antigravity IDE, Cursor, Claude Code)

В репозиторий встроен готовый навык для интеллектуальных ассистентов, расположенный в:
[`.agents/skills/resume-builder/SKILL.md`](.agents/skills/resume-builder/SKILL.md).

### Как подключить и использовать:
- **Google Antigravity IDE / Gemini CLI**: Подхватывает навык автоматически при открытии каталога проекта (Customization Root: `.agents/skills/`).
- **Cursor / Windsurf / Claude Code**: Добавьте ссылку на `.agents/skills/resume-builder/SKILL.md` в правила проекта (`.cursorrules` или системный промпт).
- **Что умеет агент с этим навыком**:
  - Мгновенно понимает правила сборки через `uv run python main.py`.
  - Знает схему независимых веток Git (`dev/py`, `dev/scraping`, `eng/*`) и помогает переключать и создавать ветки под новые вакансии.
  - Помогает синхронно переводить и форматировать пункты опыта на всех языках сразу (`RU.yaml`, `EN.yaml`, `ES.yaml`), сохраняя сильный технический тон и оцифрованные метрики.
  - Умеет проводить техническое интервью через `/grill-me` по вакансии, спарсенной через Jina Reader.
  - После редактирования обязательно запускает сборку `uv run python main.py` и передает результат на проверку пользователю.

---

## 📬 Контакты и обратная связь

Если у вас есть вопросы, идеи по улучшению или предложения:
- **Email**: [0GravityVibes+github@gmail.com](mailto:0GravityVibes+github@gmail.com)
- **GitHub**: [https://github.com/ZeroGravityVibes/resume-builder](https://github.com/ZeroGravityVibes/resume-builder)

---

## 🔗 Полезные ссылки и документация

- **Документация RenderCV**: [https://docs.rendercv.com/](https://docs.rendercv.com/)
- **Структура YAML в RenderCV**: [https://docs.rendercv.com/user_guide/yaml_input_structure/](https://docs.rendercv.com/user_guide/yaml_input_structure/)
- **Каталог локалей RenderCV**: [https://docs.rendercv.com/user_guide/yaml_input_structure/locale/](https://docs.rendercv.com/user_guide/yaml_input_structure/locale/)
- **Документация Typst**: [https://typst.app/docs/](https://typst.app/docs/)
- **Парсер Markdown Jina Reader**: [https://r.jina.ai/](https://r.jina.ai/)
- **Менеджер пакетов Astral uv**: [https://docs.astral.sh/uv/](https://docs.astral.sh/uv/)
- **Стандарт кодов языков ISO 639-1**: [https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes)

---

## 📄 Лицензия

MIT License. См. файл [LICENSE](LICENSE) для подробностей.
