import sys
import json
import re
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
        filepath_abs = os.path.abspath(filepath)
        dirname = os.path.dirname(filepath_abs)
        # Ensure it works cross-platform with basic regex extraction
        blame_out = subprocess.run(["git", "blame", "-l", "-L", "1,1", filepath_abs], cwd=dirname, capture_output=True, text=True, check=True).stdout
        if blame_out:
            parts = blame_out.split()
            if len(parts) > 0:
                commit_hash = parts[0]
                
                match = re.search(r'\((.*?)\s+\d{4}-\d{2}-\d{2}', blame_out)
                if match:
                    author = match.group(1).strip()
                
                log_out = subprocess.run(["git", "log", "-1", "--format=%B", commit_hash], cwd=dirname, capture_output=True, text=True, check=True).stdout
                commit_msg = log_out.strip()
    except subprocess.CalledProcessError as e:
        print(json.dumps({"error": f"Git subprocess failed: {str(e)}"}), file=sys.stderr)
    except Exception as e:
        print(json.dumps({"error": f"Internal parsing error: {str(e)}"}), file=sys.stderr)

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
