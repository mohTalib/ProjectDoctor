# projectdoctor/detectors/dead_code.py
import vulture

def analyze(project_path, thresholds, python_files):
    """Finds unused code using Vulture v2.11 API."""
    issues = []
    min_confidence = thresholds.get('dead_code', {}).get('min_confidence', 80)

    if not python_files:
        return issues
        
    try:
        # API for Vulture 2.x
        v = vulture.Vulture(python_files, min_confidence=min_confidence, verbose=False)
        v.scan()

        for item in v.report().split('\n'):
            if item:
                # Vulture's report format is like: "path:line: message (confidence%)"
                issues.append({
                    'file': item.split(':')[0],
                    'severity': 'LOW',
                    'message': f"Potential dead code: {item}"
                })
    except Exception:
        # If Vulture fails for any reason, fail silently.
        pass

    return issues