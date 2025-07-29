# projectdoctor/detectors/duplicate_code.py
import hashlib
from collections import defaultdict

def analyze(project_path, thresholds, python_files):
    """Finds blocks of duplicated code across different files."""
    min_lines = thresholds.get('duplicate_code', {}).get('min_lines', 8)
    hashes = defaultdict(list)
    issues = []

    # Phase 1: Collect all block hashes and their locations
    for file_path in python_files:
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = [line.strip() for line in f.readlines() if line.strip()]
            if len(lines) < min_lines:
                continue
            for i in range(len(lines) - min_lines + 1):
                block = "".join(lines[i:i + min_lines])
                block_hash = hashlib.md5(block.encode('utf-8')).hexdigest()
                hashes[block_hash].append(file_path)
        except Exception:
            continue
            
    # Phase 2: Find hashes that appear in more than one unique file
    reported_hashes = set()
    for block_hash, locations in hashes.items():
        unique_files = sorted(list(set(locations)))
        if len(unique_files) > 1 and block_hash not in reported_hashes:
            issues.append({
                'file': unique_files[0],
                'severity': 'MEDIUM',
                'message': f"Duplicated code block also found in: {', '.join(unique_files[1:])}"
            })
            reported_hashes.add(block_hash)
    return issues