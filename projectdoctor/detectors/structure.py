# projectdoctor/detectors/structure.py
import os

def analyze(project_path, thresholds, python_files):
    """Checks for common project structure best practices."""
    issues = []

    # Check for a 'tests' or 'test' directory
    if not (os.path.isdir(os.path.join(project_path, 'tests')) or \
            os.path.isdir(os.path.join(project_path, 'test'))):
        issues.append({
            'file': project_path,
            'severity': 'MEDIUM',
            'message': "Project is missing a 'tests/' directory for automated tests."
        })

    # Check for a requirements file or pyproject.toml
    has_deps_file = any(os.path.exists(os.path.join(project_path, f)) for f in [
        'requirements.txt', 'pyproject.toml'
    ])
    if not has_deps_file:
        issues.append({
            'file': project_path,
            'severity': 'LOW',
            'message': "Project is missing a dependency file like 'requirements.txt' or 'pyproject.toml'."
        })

    return issues
