# projectdoctor/analyzer.py
import os
import sys
from .detectors import file_size, long_function, duplicate_code, circular_import, complexity, structure, dead_code

class Analyzer:
    def __init__(self, project_path, thresholds=None):
        self.project_path = project_path
        self.thresholds = thresholds or {}
        self.python_files = self._get_python_files()
    def run(self):
        sys.path.insert(0, self.project_path)
        all_issues = []
        try:
            detectors = [file_size, long_function, duplicate_code, circular_import, complexity, structure, dead_code]
            for detector in detectors:
                issues = detector.analyze(self.project_path, self.thresholds, self.python_files)
                all_issues.extend(issues)
        finally:
            sys.path.pop(0)
        return {"issues": sorted(all_issues, key=lambda i: (self._severity_order(i['severity']), str(i.get('file')))), "python_files": self.python_files}
    def _get_python_files(self):
        python_files, excluded_dirs = [], {'venv', '.venv', 'env', '__pycache__', 'node_modules', '.git'}
        for root, dirs, files in os.walk(self.project_path, topdown=True):
            dirs[:] = [d for d in dirs if d not in excluded_dirs]
            for file in files:
                if file.endswith('.py'):
                    python_files.append(os.path.join(root, file))
        return python_files
    @staticmethod
    def _severity_order(severity):
        return {'HIGH': 0, 'MEDIUM': 1, 'LOW': 2}.get(severity, 3)