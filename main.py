#!/usr/bin/env python3
"""Build script for generating multilingual CVs using RenderCV and Typst.

Scans the CV directory for language YAML files (e.g., RU.yaml, EN.yaml, ES.yaml),
extracts the candidate's name from each file, and renders outputs matching the pattern:
    _{candidate_name}_{lang_code}.{ext}
in lowercase into the rendercv_output directory.
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

import yaml

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_CV_DIR = BASE_DIR / "src" / "resume_builder" / "rendercv" / "master"
DEFAULT_OUTPUT_DIR = DEFAULT_CV_DIR / "rendercv_output"

ALL_SUPPORTED_FORMATS = {"pdf", "typ", "html", "md", "png"}
DEFAULT_FORMATS = ["pdf"]

FORMAT_ALIASES = {
    "typst": "typ",
    "markdown": "md",
}


def slugify_name(name: str) -> str:
    """Convert candidate name to a clean lowercase filename slug."""
    if not name:
        return "cv"
    # Remove characters forbidden in filenames
    cleaned = re.sub(r'[\\/*?:"<>|]', "", name.strip().lower())
    # Replace spaces and hyphens with single underscores
    cleaned = re.sub(r"[\s\-]+", "_", cleaned)
    # Strip leading/trailing underscores
    cleaned = cleaned.strip("_")
    return cleaned or "cv"


def parse_output_formats(raw_formats: list[str] | None) -> set[str]:
    """Parse output formats from CLI arguments supporting multiple flags and comma/space delimiters."""
    if not raw_formats:
        return set(DEFAULT_FORMATS)

    parsed: set[str] = set()
    for item in raw_formats:
        # Split on commas or whitespace
        parts = re.split(r"[,\s]+", item.strip())
        for part in parts:
            part = part.strip().lower()
            if not part:
                continue
            canonical = FORMAT_ALIASES.get(part, part)
            if canonical == "all":
                return set(ALL_SUPPORTED_FORMATS)
            if canonical in ALL_SUPPORTED_FORMATS:
                parsed.add(canonical)
            else:
                valid_options = ", ".join(sorted(ALL_SUPPORTED_FORMATS) + ["all", "typst", "markdown"])
                print(f"[ERROR] Unsupported format '{part}'. Valid formats: {valid_options}", file=sys.stderr)
                sys.exit(1)

    return parsed or set(DEFAULT_FORMATS)


def discover_language_files(cv_dir: Path) -> dict[str, Path]:
    """Scan cv_dir for YAML files and return a dict of {lang_code: file_path}.

    Recognizes files like RU.yaml, EN.yaml, ES.yml, DE.yaml, etc.
    """
    if not cv_dir.exists():
        print(f"[ERROR] CV directory not found: {cv_dir}", file=sys.stderr)
        return {}

    lang_files: dict[str, Path] = {}
    for p in sorted(cv_dir.iterdir()):
        if not p.is_file() or p.suffix.lower() not in {".yaml", ".yml"}:
            continue
        stem = p.stem.strip()
        # Skip temporary, hidden, or schema files
        if stem.startswith((".", "_")) or "schema" in stem.lower():
            continue
        lang_code = stem.lower()
        lang_files[lang_code] = p

    return lang_files


def extract_candidate_name(yaml_path: Path) -> str:
    """Read cv.name from the given YAML file."""
    try:
        with open(yaml_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        if isinstance(data, dict):
            cv = data.get("cv", {})
            if isinstance(cv, dict):
                return str(cv.get("name", "")).strip()
    except Exception as e:
        print(f"[WARNING] Could not parse cv.name from {yaml_path.name}: {e}", file=sys.stderr)
    return ""


def build_cv(
    input_file: Path,
    lang_code: str,
    formats: set[str],
    output_dir: Path,
) -> bool:
    """Render a single CV YAML file with RenderCV for the specified formats."""
    candidate_name = extract_candidate_name(input_file)
    slug_name = slugify_name(candidate_name)

    output_dir.mkdir(parents=True, exist_ok=True)

    # RenderCV expects output paths relative to the input file
    rel_output_dir = Path("rendercv_output")

    base_name = f"_{slug_name}_{lang_code.lower()}"
    output_pdf_rel = rel_output_dir / f"{base_name}.pdf"
    output_typ_rel = rel_output_dir / f"{base_name}.typ"
    output_html_rel = rel_output_dir / f"{base_name}.html"
    output_md_rel = rel_output_dir / f"{base_name}.md"
    output_png_rel = rel_output_dir / f"{base_name}.png"

    # Destination paths for confirmation logging
    output_pdf = output_dir / f"{base_name}.pdf"
    output_typ = output_dir / f"{base_name}.typ"
    output_html = output_dir / f"{base_name}.html"
    output_md = output_dir / f"{base_name}.md"

    keep_typst = "typ" in formats
    generate_pdf = "pdf" in formats
    generate_html = "html" in formats
    generate_md = "md" in formats
    generate_png = "png" in formats

    # Typst generation is required internally by RenderCV if PDF or PNG is requested
    typst_needed = keep_typst or generate_pdf or generate_png

    cmd = [
        sys.executable,
        "-m",
        "rendercv",
        "render",
        str(input_file),
    ]

    if generate_pdf:
        cmd.extend(["--pdf-path", str(output_pdf_rel)])
    else:
        cmd.append("--dont-generate-pdf")

    if typst_needed:
        cmd.extend(["--typst-path", str(output_typ_rel)])
    else:
        cmd.append("--dont-generate-typst")

    if generate_html:
        cmd.extend(["--html-path", str(output_html_rel)])
    else:
        cmd.append("--dont-generate-html")

    if generate_md:
        cmd.extend(["--markdown-path", str(output_md_rel)])
    else:
        cmd.append("--dont-generate-markdown")

    if generate_png:
        cmd.extend(["--png-path", str(output_png_rel)])
    else:
        cmd.append("--dont-generate-png")

    format_list_str = ", ".join(sorted(formats))
    print(f"==> [{lang_code.upper()}] Building CV from {input_file.name} (formats: {format_list_str})...")

    try:
        result = subprocess.run(cmd, check=True)

        # If typst was generated only as an intermediate for PDF/PNG, clean it up
        if not keep_typst and output_typ.exists():
            output_typ.unlink(missing_ok=True)

        print(f"[OK] {lang_code.upper()} finished:")
        if generate_pdf and output_pdf.exists():
            print(f"     ├── PDF:      {output_pdf}")
        if keep_typst and output_typ.exists():
            print(f"     ├── Typst:    {output_typ}")
        if generate_html and output_html.exists():
            print(f"     ├── HTML:     {output_html}")
        if generate_md and output_md.exists():
            print(f"     ├── Markdown: {output_md}")
        if generate_png:
            pngs = sorted(output_dir.glob(f"{base_name}*.png"))
            for p in pngs:
                print(f"     ├── PNG:      {p}")
        print()
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"[FAIL] Error building {lang_code.upper()} CV: {e}\n", file=sys.stderr)
        return False


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build multilingual CVs using RenderCV and Typst.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  uv run python main.py
  uv run python main.py --lang ru
  uv run python main.py --output-format pdf,typ,html
  uv run python main.py --lang en -f all
""",
    )
    parser.add_argument(
        "--lang",
        "-l",
        type=str,
        default="all",
        help="Specific language code to build (e.g. ru, en, es, de) or 'all' (default: all)",
    )
    parser.add_argument(
        "--output-format",
        "-f",
        action="append",
        type=str,
        dest="output_formats",
        help=(
            "Output formats to generate. Options: pdf, typ (typst), html, md (markdown), png, all. "
            "Can be specified multiple times or comma/space-separated. (default: pdf)"
        ),
    )
    parser.add_argument(
        "--cv-dir",
        type=Path,
        default=DEFAULT_CV_DIR,
        help=f"Path to directory containing language YAML files (default: {DEFAULT_CV_DIR})",
    )

    args = parser.parse_args()

    cv_dir = args.cv_dir.resolve()
    output_dir = cv_dir / "rendercv_output"

    lang_files = discover_language_files(cv_dir)
    if not lang_files:
        print(f"[ERROR] No language YAML files found in {cv_dir}", file=sys.stderr)
        print("Tip: Add language files like RU.yaml, EN.yaml, ES.yaml into that directory.", file=sys.stderr)
        sys.exit(1)

    available_langs = sorted(lang_files.keys())
    requested_lang = args.lang.strip().lower()

    if requested_lang != "all" and requested_lang not in lang_files:
        print(
            f"[ERROR] Unknown language '{args.lang}'. "
            f"Available languages in {cv_dir.name}/: {', '.join(l.upper() for l in available_langs)}",
            file=sys.stderr,
        )
        sys.exit(1)

    target_langs = available_langs if requested_lang == "all" else [requested_lang]
    formats = parse_output_formats(args.output_formats)

    print("=" * 60)
    print(f"🚀 RenderCV Multilingual CV Builder")
    print(f"   Directory: {cv_dir}")
    print(f"   Discovered languages: {', '.join(l.upper() for l in available_langs)}")
    print(f"   Target languages:     {', '.join(l.upper() for l in target_langs)}")
    print(f"   Output formats:       {', '.join(sorted(formats))}")
    print("=" * 60 + "\n")

    all_success = True
    for lang in target_langs:
        success = build_cv(
            input_file=lang_files[lang],
            lang_code=lang,
            formats=formats,
            output_dir=output_dir,
        )
        if not success:
            all_success = False

    if all_success:
        print("🎉 All CVs rendered successfully!")
        sys.exit(0)
    else:
        print("❌ Some builds failed. Check the logs above.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
