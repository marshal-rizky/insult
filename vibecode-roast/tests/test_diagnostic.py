import json
import subprocess
import os

def test_diagnostic_output():
    script_path = os.path.join(os.path.dirname(__file__), "..", "scripts", "diagnostic_suite.py")
    target_file = os.path.abspath(__file__)
    
    result = subprocess.run(
        ["python", script_path, target_file],
        capture_output=True, text=True
    )
    
    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        assert False, f"Failed to parse JSON. stdout: {result.stdout}, stderr: {result.stderr}"
        
    assert "lines_of_code" in data
    assert "vibecode_score" in data
    print("Test passed!")

if __name__ == "__main__":
    test_diagnostic_output()
