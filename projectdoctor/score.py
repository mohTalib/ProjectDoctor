# projectdoctor/score.py

def _get_total_loc(python_files):
    """Calculates the total lines of code across all python files."""
    total_loc = 0
    for file_path in python_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                total_loc += sum(1 for _ in f)
        except (IOError, UnicodeDecodeError):
            continue
    return total_loc

def calculate_score(issues, python_files):
    """
    Calculates a maintainability score from 0 to 100.
    The score starts at 100 and is penalized based on the *density* of issues
    relative to the project's size (total lines of code).
    """
    severity_weights = {
        'HIGH': 15,
        'MEDIUM': 5,
        'LOW': 1,
    }
    
    total_penalty_points = sum(severity_weights.get(issue['severity'], 1) for issue in issues)

    total_loc = _get_total_loc(python_files)
    if total_loc == 0:
        return 100

    # Calculate penalty points per 1000 lines of code to normalize
    penalty_ratio = (total_penalty_points / total_loc) * 1000

    # A scaling factor to control how harshly the ratio affects the score
    scaling_factor = 5.0
    
    score_deduction = penalty_ratio * scaling_factor
    
    final_score = 100 - score_deduction

    return max(0, int(final_score))
