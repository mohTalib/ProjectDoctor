# projectdoctor/detectors/complexity.py
from radon.visitors import Function
from radon.cli.harvest import cc_visit

def analyze(project_path, thresholds, python_files):
    """
    ADVANCED DETECTOR: complexity
    Purpose: Measures cyclomatic complexity of functions.
    Improvement: Uses Radon's most reliable programmatic API (cc_visit).
    """
    max_complexity = thresholds.get('complexity', {}).get('max_complexity', 10)
    issues = []
    for file_path in python_files:
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            results = cc_visit(content)
            
            for result in results:
                if isinstance(result, Function) and result.complexity > max_complexity:
                    issues.append({
                        'file': file_path,
                        'severity': 'HIGH',
                        'message': f"Function '{result.name}' on line {result.lineno} has high cyclomatic complexity ({result.complexity})."
                    })
        except Exception:
            continue
    return issues