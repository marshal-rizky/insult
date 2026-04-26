# Vibecode Roast: Project-Wide Scan & Dynamic Scaling Design

## Overview
The Vibecode Roast skill is being upgraded from single-file analysis to full project-wide analysis. It will recursively scan directories, identify a broad array of programming languages, calculate overall metrics, pinpoint the "worst offender" file, and dynamically scale the length and aggression of the AI's response based on the project's total size.

## Architecture

### 1. `diagnostic_suite.py` (The Python Backend)
- **Directory Walking:** If given a directory path, the script will use `os.walk` to scan all files. It will explicitly ignore standard non-code directories: `.git`, `node_modules`, `venv`, `.venv`, `__pycache__`, `dist`, `build`, `.next`.
- **Comprehensive Language Detection:** The script will maintain a vast dictionary mapping of extensions to languages. This will ensure we catch everything, including:
  - **Web:** `.js`, `.ts`, `.jsx`, `.tsx`, `.html`, `.css`, `.vue`, `.svelte`
  - **Backend/Systems:** `.py`, `.java`, `.cpp`, `.c`, `.cs`, `.go`, `.rs`, `.rb`, `.php`, `.sh`, `.kt`, `.swift`
  - **Data/Config:** `.json`, `.yml`, `.yaml`, `.xml`, `.sql`
- **Global Metrics Tracking:**
  - `total_files`: Integer count of all valid files parsed.
  - `total_loc`: Integer sum of all lines of code across all files.
  - `languages`: Array of strings identifying all detected languages.
- **Worst Offender Identification:** As the script reads each file, it will calculate a basic "badness" score (lines of code + max indentation depth). It will keep track of the highest scoring file and designate it as the `worst_offender`.
- **Git Context:** The script will run `git log -1` at the directory root to grab the latest `commit_message` and `last_author` for the project.
- **Output:** A flat JSON object matching this schema:
  ```json
  {
    "scope": "project",
    "total_files": 10,
    "total_loc": 2500,
    "languages": ["Python", "JavaScript", "HTML", "C++", "Rust"],
    "worst_offender": "src/spaghetti.js",
    "worst_offender_loc": 1000,
    "last_author": "marshal Rizky",
    "commit_message": "update"
  }
  ```

### 2. `SKILL.md` (The AI Prompt)
- **Context Injection:** The prompt will expect the new JSON structure.
- **Dynamic Scaling Rules:**
  - **Small Projects (< 500 lines):** Brief, highly dismissive roast. Max 2 sentences per section. Treat it like a meaningless toy project.
  - **Medium Projects (500 - 2000 lines):** Standard detailed roast. Include targeted architectural insults.
  - **Large Projects (> 2000 lines):** Massive, multi-paragraph architectural takedown. Rip apart dependencies, bloat, and the overarching system design.
  - **Massive Projects (> 10000 lines):** Absolute zero-mercy system failure rant. 
- **Targeting the Worst Offender:** The prompt will mandate heavy emphasis specifically dragging the `worst_offender` file through the mud, requiring the AI to single it out.
