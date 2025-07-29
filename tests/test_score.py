# tests/test_score.py
import unittest

from base import BaseTestCase
from projectdoctor.score import calculate_score

class TestScore(BaseTestCase):
    def test_perfect_score(self):
        """Test score is 100 for no issues."""
        py_file = self.create_file("main.py", "print('hello')\n" * 100)
        score = calculate_score([], [py_file])
        self.assertEqual(score, 100)

    def test_score_with_high_severity_issue(self):
        """Test score reduction for HIGH severity issues."""
        issues = [{'severity': 'HIGH', 'file': 'main.py', 'message': '...'}]
        py_file = self.create_file("main.py", "print('hello')\n" * 100)
        score = calculate_score(issues, [py_file])
        self.assertLess(score, 50) # High severity should have a big impact

    def test_score_with_medium_severity_issue(self):
        """Test score reduction for MEDIUM severity issues."""
        issues = [{'severity': 'MEDIUM', 'file': 'main.py', 'message': '...'}]
        py_file = self.create_file("main.py", "print('hello')\n" * 1000)
        score = calculate_score(issues, [py_file])
        self.assertEqual(score, 75)

    def test_score_with_low_severity_issue(self):
        """Test score reduction for LOW severity issues."""
        issues = [{'severity': 'LOW', 'file': 'main.py', 'message': '...'}]
        py_file = self.create_file("main.py", "print('hello')\n" * 1000)
        score = calculate_score(issues, [py_file])
        self.assertEqual(score, 95)
        
    def test_score_normalization(self):
        """Test that score is normalized by project size."""
        issues = [{'severity': 'MEDIUM', 'file': 'main.py', 'message': '...'}]
        
        # Small project, higher penalty density
        small_project_file = self.create_file("small.py", "pass\n" * 100)
        score1 = calculate_score(issues, [small_project_file])

        # Large project, lower penalty density
        large_project_file = self.create_file("large.py", "pass\n" * 2000)
        score2 = calculate_score(issues, [large_project_file])

        self.assertLess(score1, score2)
        
    def test_empty_project(self):
        """Test that an empty project gets a perfect score."""
        score = calculate_score([], [])
        self.assertEqual(score, 100)