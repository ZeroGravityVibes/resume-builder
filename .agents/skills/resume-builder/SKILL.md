---
name: resume-builder
description: Guide for maintaining, editing, and generating multilingual CVs with RenderCV and managing qualification profiles across Git branches. Use when updating resume content, switching or adding role branches, building PDF/Typst CVs, creating new language templates, or tailoring CVs for vacancies with AI.
---

# Resume Builder Agent Skill

This skill guides AI agents on how to maintain, edit, and build multilingual CVs using [RenderCV](https://docs.rendercv.com/) and [Typst](https://typst.app/), manage role-specific profiles across Git branches, and follow the agent-supervised workflow with `/grill-me` and [Jina Reader](https://r.jina.ai/).

---

## 1. Project Purpose & Architecture

This repository is an automated wrapper over **RenderCV** and **Typst** designed to maintain a unified resume across multiple languages (`RU.yaml`, `EN.yaml`, `ES.yaml`, etc.) and adapt them quickly to target job openings or specializations.

- **Multilingual Support**: Language files are named after uppercase two-letter ISO 639-1 codes (`RU.yaml`, `EN.yaml`, `ES.yaml`, `DE.yaml`, `TR.yaml`).
- **Dynamic Discovery**: `main.py` dynamically scans the directory, extracts the candidate's name from each YAML file, and produces formatted outputs.
- **Output Naming**: Files in `rendercv_output/` follow the format:
  `_{slugified_name}_{lang_code}.{ext}` in lowercase (e.g., `_john_doe_en.pdf`, `_иван_иванов_ru.pdf`).
- **Profile Specialization via Git**: Rather than maintaining a rigid base branch or duplicate folders, each qualification profile lives in its own Git branch (e.g., `dev/py`, `dev/scraping`, `eng/senior_ventilation`). The `master` branch contains the clean, anonymized public template.

---

## 2. Quick Start & Execution Commands

### Dependency Management with `uv`
Dependencies are managed via `uv` and specified in `pyproject.toml`:
```bash
# Install / sync dependencies into virtual environment
uv sync
```

### Building Resumes with `main.py`
```bash
# Generate default format (.pdf) for ALL detected languages
uv run python main.py

# Build a specific language only (case-insensitive)
uv run python main.py --lang ru
uv run python main.py --lang en
uv run python main.py --lang es

# Generate custom output formats (pdf, typ/typst, html, md/markdown, png, or all)
uv run python main.py --output-format pdf,typ,html
uv run python main.py -f all
uv run python main.py --lang en -f pdf
```

---

## 3. Supported Languages & Quick Reference Table

RenderCV supports **22 languages out of the box**. When creating or editing a language file, use this table:

| Flag | Language | File Name | `locale.language:` in YAML | Starter Command |
| :---: | :--- | :--- | :--- | :--- |
| 🇬🇧 | English | `EN.yaml` | `english` | `uv run rendercv new "Name" --locale "english"` |
| 🇷🇺 | Russian | `RU.yaml` | `russian` | `uv run rendercv new "Name" --locale "russian"` |
| 🇪🇸 | Spanish | `ES.yaml` | `spanish` | `uv run rendercv new "Name" --locale "spanish"` |
| 🇩🇪 | German | `DE.yaml` | `german` | `uv run rendercv new "Name" --locale "german"` |
| 🇫🇷 | French | `FR.yaml` | `french` | `uv run rendercv new "Name" --locale "french"` |
| 🇮🇹 | Italian | `IT.yaml` | `italian` | `uv run rendercv new "Name" --locale "italian"` |
| 🇵🇹 | Portuguese | `PT.yaml` | `portuguese` | `uv run rendercv new "Name" --locale "portuguese"` |
| 🇹🇷 | Turkish | `TR.yaml` | `turkish` | `uv run rendercv new "Name" --locale "turkish"` |
| 🇨🇳 | Mandarin Chinese | `ZH.yaml` | `mandarin_chinese` | `uv run rendercv new "Name" --locale "mandarin_chinese"` |
| 🇯🇵 | Japanese | `JA.yaml` | `japanese` | `uv run rendercv new "Name" --locale "japanese"` |
| 🇰🇷 | Korean | `KO.yaml` | `korean` | `uv run rendercv new "Name" --locale "korean"` |
| 🇸🇦 | Arabic | `AR.yaml` | `arabic` | `uv run rendercv new "Name" --locale "arabic"` |
| 🇳🇱 | Dutch | `NL.yaml` | `dutch` | `uv run rendercv new "Name" --locale "dutch"` |
| 🇩🇰 | Danish | `DA.yaml` | `danish` | `uv run rendercv new "Name" --locale "danish"` |
| 🇮🇱 | Hebrew | `HE.yaml` | `hebrew` | `uv run rendercv new "Name" --locale "hebrew"` |
| 🇮🇳 | Hindi | `HI.yaml` | `hindi` | `uv run rendercv new "Name" --locale "hindi"` |
| 🇭🇺 | Hungarian | `HU.yaml` | `hungarian` | `uv run rendercv new "Name" --locale "hungarian"` |
| 🇮🇩 | Indonesian | `ID.yaml` | `indonesian` | `uv run rendercv new "Name" --locale "indonesian"` |
| 🇳🇴 | Norwegian Bokmål | `NB.yaml` | `norwegian_bokmål` | `uv run rendercv new "Name" --locale "norwegian_bokmål"` |
| 🇳🇴 | Norwegian Nynorsk | `NN.yaml` | `norwegian_nynorsk` | `uv run rendercv new "Name" --locale "norwegian_nynorsk"` |
| 🇮🇷 | Persian | `FA.yaml` | `persian` | `uv run rendercv new "Name" --locale "persian"` |
| 🇻🇳 | Vietnamese | `VI.yaml` | `vietnamese` | `uv run rendercv new "Name" --locale "vietnamese"` |

### How to Create a New Language Template:
1. Run: `uv run rendercv new "Candidate Name" --locale "<locale_from_table>" --theme "engineeringclassic"`
2. Move to: `src/resume_builder/rendercv/master/<XX>.yaml` (using uppercase code from table).
3. Ensure relative photo path (or comment out if the candidate prefers a text-only resume):
   ```yaml
   photo: "../../img/portrait.jpg"
   # To disable photo: simply comment out or delete the photo: line
   ```
4. Or duplicate an existing file: `cp EN.yaml DE.yaml`, set `locale.language: german`, and translate content.

### Available RenderCV Themes:
RenderCV provides **9 built-in themes** (configured via `design.theme` in YAML):
- `engineeringclassic` *(default in this repo)*: Ultra-compact, dense layout optimal for technical experience.
- `classic` *(RenderCV default)*: Traditional corporate layout with horizontal dividing rules.
- `engineeringresumes`: Minimalist format following Reddit's [r/EngineeringResumes](https://reddit.com/r/EngineeringResumes) guidelines.
- `sb2nov`: Minimalist single-column developer standard (LaTeX port).
- `moderncv`: Two-column contemporary layout common in EU job markets.
- `harvard`: Conservative Ivy League / corporate management layout.
- `ink`: Editorial aesthetic with distinct typography.
- `ember`: Contemporary tech/startup aesthetic with warm accents.
- `opal`: Clean, light, modern style.

---

## 4. Agent Editing & Supervision Workflow

Resume editing is primarily performed by the AI agent under user supervision. When updating or tailoring a resume, follow this protocol:

### Step 1: Ingest Vacancy with Jina Reader (`r.jina.ai`)
When given a job posting link (LinkedIn, HH.ru, career page), extract clean markdown without ads or tracking:
`https://r.jina.ai/<vacancy_url>`

### Step 2: Calibrate Content via `/grill-me`
Engage in an interview session with `/grill-me`:
- Probe the user's past projects for concrete metrics (throughput, latency, cost savings, team size).
- Align technical terminology with ATS keywords and the company's stack.

### Step 3: Edit All Active Resumes in Parallel
Update `RU.yaml`, `EN.yaml`, and `ES.yaml` synchronously to keep achievements and timelines in parity.

### Step 4: MANDATORY Build & Verification
Immediately after editing YAML files, the agent **MUST** run:
```bash
uv run python main.py
```
- Verify zero syntax or Typst compilation errors.
- Confirm output files are cleanly generated in `src/resume_builder/rendercv/master/rendercv_output/`.

### Step 5: Present to User for Review
Show the user the exact diff of edits made to each language file and the paths to generated PDFs for final human verification.

---

## 5. Git Workflow: Independent Role Branches

### Branch Naming
- `dev/<role>`: IT and software engineering roles (`dev/py`, `dev/scraping`, `dev/technical_l2_support`).
- `eng/<role>`: Engineering & physical systems (`eng/senior_ventilation`).
- `master`: Public, anonymized template for GitHub.

### Updating Contact Details Across Branches
When shared contact details (phone, email, links, photo) change, the user asks the agent:
> *"Update my phone number and email across all active branches (`dev/py`, `dev/scraping`, `dev/technical_l2_support`, `eng/senior_ventilation`)."*

The agent systematically checks out each branch, applies the edit, verifies the build, and commits.

---

## 6. Official References

- **RenderCV Documentation**: [https://docs.rendercv.com/](https://docs.rendercv.com/)
- **RenderCV Locale Guide**: [https://docs.rendercv.com/user_guide/yaml_input_structure/locale/](https://docs.rendercv.com/user_guide/yaml_input_structure/locale/)
- **Typst Documentation**: [https://typst.app/docs/](https://typst.app/docs/)
- **Jina Reader**: [https://r.jina.ai/](https://r.jina.ai/)
