import sys
import json
import subprocess
import os
import re

IGNORE_DIRS = {'.git', 'node_modules', 'venv', '.venv', '__pycache__', 'dist', 'build', '.next'}
LANGUAGE_MAP = {
    '.js': 'JavaScript', '.ts': 'TypeScript', '.jsx': 'React', '.tsx': 'React TS',
    '.html': 'HTML', '.css': 'CSS', '.vue': 'Vue', '.svelte': 'Svelte',
    '.py': 'Python', '.java': 'Java', '.cpp': 'C++', '.c': 'C', '.cs': 'C#',
    '.go': 'Go', '.rs': 'Rust', '.rb': 'Ruby', '.php': 'PHP', '.sh': 'Shell',
    '.kt': 'Kotlin', '.swift': 'Swift', '.json': 'JSON', '.yml': 'YAML',
    '.yaml': 'YAML', '.xml': 'XML', '.sql': 'SQL', '.md': 'Markdown'
}

def analyze_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        loc = len(lines)
        max_indent = max((len(line) - len(line.lstrip())) for line in lines) if lines else 0
        score = (loc // 100) + (max_indent // 4)
        return loc, max_indent, score
    except Exception:
        return 0, 0, 0

def analyze(target_path):
    if not os.path.exists(target_path):
        print(json.dumps({"error": "Path not found"}))
        sys.exit(1)

    total_files = 0
    total_loc = 0
    languages = set()
    worst_offender = None
    worst_offender_loc = 0
    worst_score = -1

    target_abs = os.path.abspath(target_path)
    
    files_to_check = []
    if os.path.isdir(target_abs):
        for root, dirs, files in os.walk(target_abs):
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
            for file in files:
                files_to_check.append(os.path.join(root, file))
    else:
        files_to_check.append(target_abs)

    for filepath in files_to_check:
        ext = os.path.splitext(filepath)[1].lower()
        if ext in LANGUAGE_MAP:
            languages.add(LANGUAGE_MAP[ext])
        else:
            if not ext and os.path.basename(filepath) != "Dockerfile":
                continue # Skip extensionless unknown files
        
        loc, max_indent, score = analyze_file(filepath)
        if loc == 0: continue
        
        total_files += 1
        total_loc += loc
        
        if score > worst_score:
            worst_score = score
            worst_offender = filepath
            worst_offender_loc = loc

    # Get Git Context for the directory or file
    author = "Unknown"
    commit_msg = "Unknown"
    dirname = target_abs if os.path.isdir(target_abs) else os.path.dirname(target_abs)
    
    try:
        log_out = subprocess.run(["git", "log", "-1", "--format=%an|%B"], cwd=dirname, capture_output=True, text=True, check=True).stdout
        if log_out:
            parts = log_out.split('|', 1)
            if len(parts) == 2:
                author = parts[0].strip()
                commit_msg = parts[1].strip()
    except subprocess.CalledProcessError:
        pass # Ignore git failure if it's not a git repo
        
    # Relative path for worst offender if possible
    if worst_offender and worst_offender.startswith(dirname):
        worst_offender = os.path.relpath(worst_offender, dirname)

    output = {
        "scope": "project" if os.path.isdir(target_abs) else "file",
        "total_files": total_files,
        "total_loc": total_loc,
        "languages": list(languages),
        "worst_offender": worst_offender,
        "worst_offender_loc": worst_offender_loc,
        "last_author": author,
        "commit_message": commit_msg
    }
    
    print(json.dumps(output))

if __name__ == "__main__":
    if len(sys.argv) > 1:
        analyze(sys.argv[1])
    else:
        print(json.dumps({"error": "No path provided"}))
