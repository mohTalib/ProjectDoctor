# projectdoctor/detectors/file_size.py

def analyze(project_path, thresholds, python_files):
    """
    ADVANCED DETECTOR: file_size
    Purpose: Detects files that exceed a recommended line count.
    Improvement: More resilient to file reading errors.
    """
    max_lines = thresholds.get('file_size', {}).get('max_lines', 800)
    issues = []
    for file_path in python_files:
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                line_count = sum(1 for _ in f)
                if line_count > max_lines:
                    issues.append({
                        'file': file_path,
                        'severity': 'LOW',
                        'message': f"File exceeds {max_lines} lines (has {line_count} lines)."
                    })
        except IOError as e:
            # If a file can't be read, we can report it as a low-level warning.
            issues.append({
                'file': file_path,
                'severity': 'LOW',
                'message': f"Could not read or parse file: {e}"
            })
            continue
    return issues