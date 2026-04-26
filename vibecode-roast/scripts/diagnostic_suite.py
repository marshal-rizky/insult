import sys
import json
import subprocess
import os

def analyze(filepath):
    if not os.path.exists(filepath):
        print(json.dumps({"error": "File not found"}))
        sys.exit(1)

    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    loc = len(lines)
    max_indent = max((len(line) - len(line.lstrip())) for line in lines) if lines else 0
    score = min(10, max(1, (loc // 100) + (max_indent // 4)))

    author = "Unknown"
    timestamp = "Unknown"
    commit_msg = "Unknown"
    
    try:
        dirname = os.path.dirname(os.path.abspath(filepath))
        # Ensure it works cross-platform with basic text extraction
        blame_out = subprocess.run(["git", "blame", "-l", "-L", "1,1", filepath], cwd=dirname, capture_output=True, text=True).stdout
        if blame_out:
            parts = blame_out.split()
            if len(parts) > 0:
                commit_hash = parts[0]
                author_start = blame_out.find('(') + 1
                author_end = blame_out.find(' 202', author_start)
                if author_end != -1:
                    author = blame_out[author_start:author_end].strip()
                
                log_out = subprocess.run(["git", "log", "-1", "--format=%B", commit_hash], cwd=dirname, capture_output=True, text=True).stdout
                commit_msg = log_out.strip()
    except Exception:
        pass

    output = {
        "lines_of_code": loc,
        "max_indentation_depth": max_indent,
        "vibecode_score": score,
        "last_author": author,
        "commit_message": commit_msg,
        "last_touched_timestamp": timestamp
    }
    
    print(json.dumps(output))

if __name__ == "__main__":
    if len(sys.argv) > 1:
        analyze(sys.argv[1])
    else:
        print(json.dumps({"error": "No file provided"}))
