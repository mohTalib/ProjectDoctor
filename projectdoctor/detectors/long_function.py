# projectdoctor/detectors/long_function.py
import ast

def analyze(project_path, thresholds, python_files):
    """Identifies functions that are too long using Python's AST."""
    max_lines = thresholds.get('long_function', {}).get('max_lines', 50)
    issues = []
    for file_path in python_files:
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    start_line = node.lineno
                    end_line = node.end_lineno
                    if end_line and start_line:
                        length = end_line - start_line + 1
                        if length > max_lines:
                            issues.append({
                                'file': file_path,
                                'severity': 'MEDIUM',
                                'message': f"Function '{node.name}' on line {start_line} is too long ({length} lines)."
                            })
        except Exception:
            continue # Skip files that cannot be parsed
    return issues