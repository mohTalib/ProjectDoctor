# projectdoctor/reporter.py
import json
from .score import calculate_score

class Reporter:
    def __init__(self, analysis_results):
        self.issues = analysis_results['issues']
        self.python_files = analysis_results['python_files']
        self.score = calculate_score(self.issues, self.python_files)

    def to_cli(self):
        """Prints a summary report to the command line."""
        print("\n" + "="*50)
        print("🩺 ProjectDoctor Report – Code Health Overview")
        print("="*50)
        print(f"\n📊 Maintainability Score: {self.score}/100\n")

        if not self.issues:
            print("✅ No issues detected. Great job!")
            return

        print("⚠️ Issues Detected:")
        for issue in self.issues:
            severity = issue['severity']
            file = issue.get('file', 'Project-wide')
            message = issue['message']
            print(f"- [{severity}] `{file}`: {message}")

    def to_markdown(self, filename):
        """Saves a detailed report in Markdown format."""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("# 🩺 ProjectDoctor Report – Code Health Overview\n\n")
            f.write(f"📊 **Maintainability Score:** {self.score}/100\n\n")
            
            if not self.issues:
                f.write("✅ No issues detected. Great job!\n")
                return

            f.write("## ⚠️ Issues Detected\n\n")
            f.write("| Severity | File | Issue Description |\n")
            f.write("|----------|------|-------------------|\n")
            for issue in self.issues:
                severity = issue['severity']
                file = issue.get('file', 'Project-wide')
                message = issue['message']
                f.write(f"| {severity} | `{file}` | {message} |\n")

    def to_json(self):
        """Returns a JSON representation of the report."""
        report = {
            'maintainability_score': self.score,
            'issue_count': len(self.issues),
            'issues': self.issues,
        }
        return json.dumps(report, indent=2)
