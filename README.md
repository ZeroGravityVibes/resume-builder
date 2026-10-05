# Multilingual Resume Builder

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![RenderCV](https://img.shields.io/badge/RenderCV-v2.6%2B-orange.svg)](https://docs.rendercv.com/)
[![Typst](https://img.shields.io/badge/Typst-Powered-239dad.svg)](https://typst.app/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Russian Docs](https://img.shields.io/badge/docs-Русская_версия-red.svg)](README.RU.md)

> An automated, developer-friendly wrapper over **[RenderCV](https://docs.rendercv.com/)** and **[Typst](https://typst.app/docs/)** designed to maintain, synchronize, and build multilingual resumes across different target qualifications and job vacancies using Git branches.

[🇷🇺 Читать на русском языке](README.RU.md)

---

## 🎯 Purpose & Core Concept

When applying for diverse roles (e.g., *Backend Engineer*, *Data Platform Engineer*, *Scraping Specialist*, *Support Lead*, or *Mechanical Engineer*), candidates often need:
1. **Multiple Language Versions** (e.g., English, Russian, Spanish, German) kept strictly in sync.
2. **Role-Specific Focus** (different headlines, tailored highlights, prioritized skillsets) without creating messy duplicate directories.

This repository solves this through a clean architecture:
- **Language Templates as Plain YAML**: Each language is stored in a clean, ISO-coded file (e.g. `EN.yaml`, `RU.yaml`, `ES.yaml`).
- **Dynamic Auto-Discovery**: `main.py` scans the folder, parses candidate names, and generates all resumes with a single command.
- **Git Branch-Based Qualification Tracking**: Different target roles live on separate Git branches (e.g., `dev/py`, `dev/scraping`, `eng/senior_ventilation`), keeping the directory structure clean and version-controlled.

---

## 📁 Project Structure

```text
resume-builder/
├── .agents/
│   └── skills/
│       └── resume-builder/
│           └── SKILL.md               # AI Agent skill for Antigravity IDE & assistants
├── src/resume_builder/
│   ├── img/
│   │   └── portrait.jpg               # Portrait photo (keep this name!)
│   └── rendercv/master/
│       ├── RU.yaml                    # Russian CV source
│       ├── EN.yaml                    # English CV source
│       ├── ES.yaml                    # Spanish CV source
│       ├── fonts/                     # Custom typography fonts (e.g. Exo 2, TTF)
│       └── rendercv_output/           # Generated output files
│           ├── _john_doe_en.pdf
│           ├── _john_doe_en.typ
│           ├── _иван_иванов_ru.pdf
│           └── ...
├── main.py                            # Auto-discovery build script
├── pyproject.toml                     # Python project dependencies & metadata
├── uv.lock                            # Locked dependencies
├── README.md                          # Documentation (English)
└── README.RU.md                       # Documentation (Russian)
```

### Important Naming Rules (Do Not Break)
- **`src/resume_builder/img/portrait.jpg`**: Universal portrait image path. Referenced inside YAML files via relative path:
  ```yaml
  photo: "../../img/portrait.jpg"
  ```
- **`[ISO].yaml` (e.g., `RU.yaml`, `EN.yaml`, `ES.yaml`, `DE.yaml`)**: Language templates must use two-letter uppercase codes matching [ISO 639-1](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes).

---

## 🚀 Quick Start

### 1. Prerequisites & Installation

We recommend using **[uv](https://docs.astral.sh/uv/)**, an extremely fast Python package and project manager.

Clone the repository and install dependencies:
```bash
# Clone the repository
git clone https://github.com/your-username/resume-builder.git
cd resume-builder

# Install dependencies into virtual environment
uv sync
```

*(Alternatively with standard pip: `python3 -m venv .venv && source .venv/bin/activate && pip install -e .`)*

---

### 2. Building All Resumes (One-Click)

Run the build script:

```bash
uv run python main.py
```

The script automatically:
1. Scans the `src/resume_builder/rendercv/master/` folder.
2. Discovers all language files (e.g. `EN`, `ES`, `RU`).
3. Extracts candidate name from the `cv.name` field.
4. Generates production-ready **PDF** files (`.pdf`) by default.  
   *(If you also need Typst sources, pass `-f pdf,typ` or `--output-format all`)*.

Generated files appear in the directory:
`src/resume_builder/rendercv/master/rendercv_output/`:
- `_{candidate_name}_{lang_code}.pdf`

---

### 3. Build Options & CLI Flags

#### Build a single language:
The `--lang` (or `-l`) flag selects a specific language (case-insensitive):
```bash
# English only
uv run python main.py --lang en

# Russian only
uv run python main.py --lang ru

# Spanish only
uv run python main.py --lang es
```

#### Choose custom output formats:
RenderCV supports `pdf`, `typ` (`typst`), `html`, `md` (`markdown`), and `png`. Use `--output-format` (or `-f`) to specify formats (separated by commas or spaces, repeated flags, or `all`):

```bash
# Generate PDF only (default):
uv run python main.py --output-format pdf

# Generate PDF and Typst sources:
uv run python main.py --output-format pdf,typ

# Generate PDF and HTML:
uv run python main.py --output-format pdf,html

# Generate all supported formats (PDF, Typst, HTML, Markdown, PNG):
uv run python main.py --output-format all

# Combine language filter and multiple format flags:
uv run python main.py --lang en -f pdf -f html
```

---

## 🌿 Managing Roles & Vacancies with Git

Instead of maintaining a rigid "core" base branch or duplicating folders, maintain each qualification profile in an independent Git branch:

```text
├── dev/py                  # Python Backend, High-Load, Data Pipelines
├── dev/scraping            # Web Scraping, Crawling, ETL Pipelines
├── dev/technical_l2_support # Technical Support, SRE, Observability
└── eng/senior_ventilation  # Industrial Engineering & HVAC
```

### Git Workflow & Cheatsheet

```bash
# 1. List all role branches
git branch -a

# 2. Switch to a target role
git switch dev/py

# 3. Create a new branch for a vacancy or target role
git switch -c dev/ai-platform

# 4. Tailor the YAML templates, build, and commit:
uv run python main.py
git status
git commit -am "feat(cv): tailor highlights for AI Platform vacancy"
```

### Updating Universal Data Across Branches
When shared contact details (phone, email, Telegram, LinkedIn) or the portrait photo change:
- Simply instruct your AI agent:  
  > *"Update my phone number and email in all active role branches (`dev/py`, `dev/scraping`, `dev/technical_l2_support`, `eng/senior_ventilation`)."*
- The agent will check out each branch and apply the change cleanly.

---

## 🤖 AI-Powered Workflow: Jina Reader & `/grill-me`

### 💡 Pro-Tip: Clean Vacancy Markdown with Jina Reader (`r.jina.ai`)
When tailoring your resume for a job on LinkedIn, HeadHunter, or a company career page, you need to feed the job description to an AI without ads, navigation bars, and cookie banners:
1. Simply prepend `https://r.jina.ai/` before any job vacancy URL:
   ```text
   https://r.jina.ai/https://example.com/careers/senior-python-engineer
   ```
2. Jina Reader parses the page on the fly and returns pure, clean **Markdown**.
3. Paste that Markdown directly into chat with your AI agent.

### Calibrate Experience with `/grill-me`
1. Give the vacancy Markdown to your AI agent and invoke `/grill-me`.
2. The agent will run an interactive interview to:
   - Identify gaps between your background and the vacancy requirements.
   - Dig out specific, measurable metrics and architectural solutions from your past projects.
   - Format strong, impact-oriented bullet points tailored for the target role.
3. Apply changes to `RU.yaml`, `EN.yaml`, and `ES.yaml` in parallel and run `uv run python main.py`.

---

## 🖼️ Replacing or Disabling the Portrait Photo

### 1. Replacing with Your Own Photo
1. Prepare a vertical portrait photo in JPG format.
2. Replace the file at:
   `src/resume_builder/img/portrait.jpg`
3. Ensure your YAML files (`RU.yaml`, `EN.yaml`, `ES.yaml`) reference it via a relative path:
   ```yaml
   cv:
     photo: "../../img/portrait.jpg"
   ```

### 2. Disabling the Photo Completely (Text-Only Resume)
If you prefer a text-only resume (standard in US/UK markets) or do not wish to display a photo:
- Simply **comment out** (prefix with `#`) or **delete** the `photo:` line in your YAML file:
  ```yaml
  cv:
    name: John Doe
    headline: "Senior Backend Engineer | Cloud Architecture"
    location: "San Francisco, CA, USA"
    email: "john.doe@example.com"
    # photo: "../../img/portrait.jpg"   # <-- Comment out or remove this line
    phone: "+1 415 555 0192"
  ```
RenderCV will automatically adapt the layout into a clean, full-width text-only header without awkward empty boxes or margins.

> **💡 Pro-Tip:** You can similarly omit or comment out any other optional field:
> - `# phone: "+1 ..."` — hide phone number
> - `# website: https://...` — hide personal website
> - comment out specific networks under `social_networks` or entire sections under `sections:`.

---

## 📝 How to Edit Your Resume

### 1. File Location
Edit the YAML file for your target language in `src/resume_builder/rendercv/master/`:
- `RU.yaml` — Russian version
- `EN.yaml` — English version
- `ES.yaml` — Spanish version
- (or create `DE.yaml`, `FR.yaml`, etc.)

### 2. YAML Structure Explained

```yaml
# yaml-language-server: $schema=https://raw.githubusercontent.com/rendercv/rendercv/refs/tags/v2.6/schema.json
cv:
  name: John Doe
  headline: "Senior Backend Engineer | Cloud Architecture & Observability"
  location: "San Francisco, CA, USA"
  email: "john.doe@example.com"
  photo: "../../img/portrait.jpg"     # Relative path to your photo
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
        High-impact summary highlighting your architectural mindset, core stack,
        and problem-solving capabilities.

    Experience:
      - company: ACME Corp
        position: Senior Backend Engineer
        start_date: 2022-01
        end_date: present
        location: Remote
        summary: Lead developer for high-throughput analytics platform.
        highlights:
          - "Designed async ingestion microservices processing 50M+ events/day."
          - "Integrated VictoriaMetrics and Vector, slashing P99 latency by 35%."

    Skills:
      - label: Languages
        details: Python, SQL, Bash
      - label: Frameworks & Tools
        details: FastAPI, Asyncio, Docker, VictoriaMetrics, Vector, ClickHouse

design:
  theme: engineeringclassic           # Theme choice (see Available Themes section below)
  font_family:
    body: Source Sans 3
  header:
    photo_position: right

locale:
  language: english                   # RenderCV locale name (see below)
```

### 3. Agent-Supervised Resume Editing Workflow

In practice, resume editing is primarily performed by an **AI agent under user supervision**:
1. **Provide Vacancy Details**: Pass the vacancy URL (via `https://r.jina.ai/<url>`) to your AI agent.
2. **Run `/grill-me`**: The agent interviews you to draw out quantifiable achievements, architectural solutions, and metrics.
3. **Agent Updates All Resumes**: The agent automatically edits `RU.yaml`, `EN.yaml`, and `ES.yaml` in parallel to preserve content parity.
4. **Agent Builds & Validates**: The agent runs `uv run python main.py` to confirm zero compilation or syntax errors.
5. **Human Review**: The user reviews the git diff and generated PDFs, accepting or fine-tuning as needed.

---

## 🎨 Available Themes

RenderCV includes **9 built-in themes**. You can effortlessly switch the visual aesthetic and layout density of your resume without altering its content.

```text
Available themes: classic (default), ember, engineeringclassic, engineeringresumes, harvard, ink, moderncv, opal, sb2nov.
```

### Themes Comparison Table:

| Theme | Description & Visual Characteristics | Best For |
| :--- | :--- | :--- |
| **`engineeringclassic`** *(default in this project)* | Compact, dense engineering layout with neat lines maximizing page space efficiency. | Software Engineers, DevOps, Systems Engineers |
| **`classic`** *(RenderCV default)* | Traditional corporate format with horizontal rules and balanced spacing. | General corporate, business, and enterprise roles |
| **`engineeringresumes`** | Clean layout adhering to Reddit's [r/EngineeringResumes](https://reddit.com/r/EngineeringResumes) standard. | Tech professionals targeting ATS screening |
| **`sb2nov`** | Widely used minimalist layout popular among tech specialists (LaTeX port). | Software Developers, Data Engineers, SRE |
| **`moderncv`** | European-style layout with elegant modern section titles. | European job markets (Germany, Netherlands, UK) |
| **`harvard`** | Ivy League academic and corporate style (Harvard Business School aesthetic). | Management, finance, consulting, academia |
| **`ink`** | Editorial aesthetic with refined typography. | Product managers, research, technical writing |
| **`ember`** | Modern design with warm accents and contemporary structure. | Tech startups, creative engineering |
| **`opal`** | Clean, airy design with soft visual hierarchy. | Modern IT companies, agile environments |

### How to Change the Theme:

#### 1. In Existing YAML Files
Edit your target YAML file (`EN.yaml`, `RU.yaml`, `ES.yaml`, etc.) in `src/resume_builder/rendercv/master/` and change the `theme` field under `design`:

```yaml
design:
  theme: engineeringresumes   # Set any theme from the table above
```

Then rebuild your resumes:
```bash
uv run python main.py
```

#### 2. When Creating a New Template via CLI
Pass the `--theme` flag to the `rendercv new` command:

```bash
uv run rendercv new "John Doe" --theme "engineeringresumes" --locale "english"
```

---

## 🌍 Supported Languages & Quick Reference Table

RenderCV supports **22 languages out of the box**. Use the table below to find the uppercase file name and corresponding `locale.language` setting without checking external docs:

| Flag | Language | Template File | `locale.language:` | Generator Command |
| :---: | :--- | :--- | :--- | :--- |
| 🇬🇧 | English | `EN.yaml` | `english` | `uv run rendercv new "Your Name" --locale "english"` |
| 🇷🇺 | Russian | `RU.yaml` | `russian` | `uv run rendercv new "Your Name" --locale "russian"` |
| 🇪🇸 | Spanish | `ES.yaml` | `spanish` | `uv run rendercv new "Your Name" --locale "spanish"` |
| 🇩🇪 | German | `DE.yaml` | `german` | `uv run rendercv new "Your Name" --locale "german"` |
| 🇫🇷 | French | `FR.yaml` | `french` | `uv run rendercv new "Your Name" --locale "french"` |
| 🇮🇹 | Italian | `IT.yaml` | `italian` | `uv run rendercv new "Your Name" --locale "italian"` |
| 🇵🇹 | Portuguese | `PT.yaml` | `portuguese` | `uv run rendercv new "Your Name" --locale "portuguese"` |
| 🇹🇷 | Turkish | `TR.yaml` | `turkish` | `uv run rendercv new "Your Name" --locale "turkish"` |
| 🇨🇳 | Mandarin Chinese | `ZH.yaml` | `mandarin_chinese` | `uv run rendercv new "Your Name" --locale "mandarin_chinese"` |
| 🇯🇵 | Japanese | `JA.yaml` | `japanese` | `uv run rendercv new "Your Name" --locale "japanese"` |
| 🇰🇷 | Korean | `KO.yaml` | `korean` | `uv run rendercv new "Your Name" --locale "korean"` |
| 🇸🇦 | Arabic | `AR.yaml` | `arabic` | `uv run rendercv new "Your Name" --locale "arabic"` |
| 🇳🇱 | Dutch | `NL.yaml` | `dutch` | `uv run rendercv new "Your Name" --locale "dutch"` |
| 🇩🇰 | Danish | `DA.yaml` | `danish` | `uv run rendercv new "Your Name" --locale "danish"` |
| 🇮🇱 | Hebrew | `HE.yaml` | `hebrew` | `uv run rendercv new "Your Name" --locale "hebrew"` |
| 🇮🇳 | Hindi | `HI.yaml` | `hindi` | `uv run rendercv new "Your Name" --locale "hindi"` |
| 🇭🇺 | Hungarian | `HU.yaml` | `hungarian` | `uv run rendercv new "Your Name" --locale "hungarian"` |
| 🇮🇩 | Indonesian | `ID.yaml` | `indonesian` | `uv run rendercv new "Your Name" --locale "indonesian"` |
| 🇳🇴 | Norwegian Bokmål | `NB.yaml` | `norwegian_bokmål` | `uv run rendercv new "Your Name" --locale "norwegian_bokmål"` |
| 🇳🇴 | Norwegian Nynorsk | `NN.yaml` | `norwegian_nynorsk` | `uv run rendercv new "Your Name" --locale "norwegian_nynorsk"` |
| 🇮🇷 | Persian | `FA.yaml` | `persian` | `uv run rendercv new "Your Name" --locale "persian"` |
| 🇻🇳 | Vietnamese | `VI.yaml` | `vietnamese` | `uv run rendercv new "Your Name" --locale "vietnamese"` |

### How to Create a New Language File:
- **Option A (CLI Generator)**: Run `uv run rendercv new "Your Name" --locale "turkish"`, move `Your_Name_CV.yaml` to `src/resume_builder/rendercv/master/TR.yaml`, and set `photo: "../../img/portrait.jpg"`.
- **Option B (Copy & Translate)**: Duplicate `cp EN.yaml DE.yaml`, set `locale.language: german`, translate content, and run `uv run python main.py --lang de`.

---

## 🤖 AI Assistant / IDE Agent Skill

This project includes a ready-to-use Agent Skill located at [`.agents/skills/resume-builder/SKILL.md`](.agents/skills/resume-builder/SKILL.md).

### How to use with AI Agents:
- **Google Antigravity IDE / Gemini CLI**: Automatically discovered via `.agents/skills/` workspace customizations.
- **Cursor / Claude Code / Windsurf**: Reference `.agents/skills/resume-builder/SKILL.md` in your custom instructions, system prompt, or slash commands.
- The agent will automatically know:
  - How to build the resumes (`uv run python main.py`).
  - How to switch and manage Git role branches.
  - How to keep translations in sync across languages.
  - How to conduct technical interviews via `/grill-me` using clean vacancy markdown from Jina Reader.

---

## 📬 Contact & Feedback

For questions, suggestions, or contributions, feel free to reach out:
- **Email**: [0GravityVibes+github@gmail.com](mailto:0GravityVibes+github@gmail.com)
- **Repository**: [https://github.com/ZeroGravityVibes/resume-builder](https://github.com/ZeroGravityVibes/resume-builder)

---

## 🔗 Useful Links & Documentation

- **RenderCV Official Docs**: [https://docs.rendercv.com/](https://docs.rendercv.com/)
- **RenderCV YAML Input Structure**: [https://docs.rendercv.com/user_guide/yaml_input_structure/](https://docs.rendercv.com/user_guide/yaml_input_structure/)
- **RenderCV Locale Guide**: [https://docs.rendercv.com/user_guide/yaml_input_structure/locale/](https://docs.rendercv.com/user_guide/yaml_input_structure/locale/)
- **Typst Official Docs**: [https://typst.app/docs/](https://typst.app/docs/)
- **Jina Reader**: [https://r.jina.ai/](https://r.jina.ai/)
- **uv Project Manager Docs**: [https://docs.astral.sh/uv/](https://docs.astral.sh/uv/)
- **ISO 639-1 Language Codes**: [https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes)

---

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.
