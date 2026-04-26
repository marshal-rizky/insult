# Vibecode Diagnostic Suite Design

## Overview
The "Vibecode Roast" skill for Antigravity is being upgraded from a simple markdown prompt to a full "Crime Scene Suite." This upgrade adds a diagnostic Python script to dynamically gather real metrics and Git author information, which the AI will use to generate a highly personalized, aggressively formatted "Code Crime Report."

## Architecture & Components

The skill will consist of two main components:
1. `vibecode-roast/scripts/diagnostic_suite.py`
2. `vibecode-roast/SKILL.md` (Updated)

There are no external dependencies required; the diagnostic script will rely entirely on built-in Python libraries and standard `git` CLI availability via `subprocess`.

### Component 1: `diagnostic_suite.py`
**Purpose:** A utility script that statically analyzes a given file or directory to provide structured context (ammunition) for the AI to roast the user.

**Input:** A relative or absolute file path.
**Behavior:**
- Runs `git blame` on the file to extract the last author, commit timestamp, and commit hash.
- Runs `git log` to fetch the commit message for that change.
- Calculates basic code metrics: total lines of code, maximum nesting depth (by roughly counting indentation), and an estimated length of the longest function block.
- Generates a `vibecode_score` (1-10) heuristically, based mostly on length and depth metrics scaling against a baseline.

**Output:** A JSON string printed to stdout containing the compiled statistics.

### Component 2: `SKILL.md` Modification
**Purpose:** The prompt file driving the Gemini behavior when the skill triggers.

**Behavior:**
- Instructs the AI that it MUST run `python scripts/diagnostic_suite.py <some_file>` whenever it investigates a piece of code.
- Forces the generation of a structured "Code Crime Report" as the output format.

**Required Report Format:**
1. **Officer on Duty**: (e.g., Senior Principal Engineer AI)
2. **Crime Scene**: `<file_path>`
3. **Primary Suspect**: `<author_from_script>`
4. **Time of Offense**: `<timestamp_from_script>`
5. **Vibecode Severity Rating**: `<score_from_script>`/10
6. **The Interrogation**: A highly aggressive takedown combining the commit message, the code size, and the actual architectural flaws found by Gemini.
7. **The Mandated Refactor**: Gemini's corrected code with angry annotations.
