# tests/test_detectors.py
import os
import unittest
# --- THIS IS THE FIX ---
# Changed from ".base" to "base"
from base import BaseTestCase
from projectdoctor.detectors import (
    file_size, long_function, complexity, duplicate_code,
    structure, dead_code, circular_import
)

class TestDetectors(BaseTestCase):

    # --- file_size ---
    def test_file_size_detector(self):
        oversized_content = "a = 1\n" * 801
        ok_content = "a = 1\n" * 100
        f1 = self.create_file("oversized.py", oversized_content)
        f2 = self.create_file("ok.py", ok_content)
        
        issues = file_size.analyze(self.project_path, {}, [f1, f2])
        self.assertEqual(len(issues), 1)
        self.assertIn("exceeds 800 lines", issues[0]['message'])
        self.assertEqual(issues[0]['file'], f1)

    # --- long_function ---
    def test_long_function_detector(self):
        long_func_content = "def my_long_function():\n" + "    print('line')\n" * 51
        f1 = self.create_file("long.py", long_func_content)
        issues = long_function.analyze(self.project_path, {}, [f1])
        self.assertEqual(len(issues), 1)
        self.assertIn("is too long", issues[0]['message'])

   # --- complexity ---
    def test_complexity_detector(self):
        # This function has a guaranteed cyclomatic complexity of 11.
        # 1 (base) + 10 (for each elif) = 11.
        complex_func = """
                def very_high_complexity(a):
                    if a == 1: return 1
                    elif a == 2: return 2
                    elif a == 3: return 3
                    elif a == 4: return 4
                    elif a == 5: return 5
                    elif a == 6: return 6
                    elif a == 7: return 7
                    elif a == 8: return 8
                    elif a == 9: return 9
                    elif a == 10: return 10
                    else: return 11
                """
        f1 = self.create_file("complex.py", complex_func)
        issues = complexity.analyze(self.project_path, {}, [f1])
        self.assertEqual(len(issues), 1)
        self.assertIn("high cyclomatic complexity", issues[0]['message'])

    # --- duplicate_code ---
    def test_duplicate_code_detector(self):
        common_block = "print('this is common code')\n" * 10
        f1 = self.create_file("module1/a.py", f"def func_a():\n{common_block}")
        f2 = self.create_file("module2/b.py", f"def func_b():\n{common_block}")
        
        issues = duplicate_code.analyze(self.project_path, {}, [f1, f2])
        self.assertEqual(len(issues), 1)
        self.assertIn("Duplicate code block", issues[0]['message'])

    # --- structure ---
    def test_structure_detector_no_tests(self):
        self.create_file("some_code.py")
        issues = structure.analyze(self.project_path, {}, [])
        self.assertEqual(len(issues), 2) # No tests, no requirements
        self.assertTrue(any("missing a 'tests/' directory" in i['message'] for i in issues))

    def test_structure_detector_with_tests(self):
        os.makedirs(os.path.join(self.project_path, 'tests'))
        self.create_file("requirements.txt")
        issues = structure.analyze(self.project_path, {}, [])
        self.assertEqual(len(issues), 0)

# --- dead_code ---
    def test_dead_code_detector(self):
        # We create a more realistic scenario with multiple files
        code_with_dead_functions = """
# This file defines various functions and classes
import os # This import is unused and should be detected as dead

class UnusedClass: # This class is never instantiated
    pass

def _internal_helper(): # This is unused
    return "secret"

def public_api_function():
    return "This function is used"

DEAD_VARIABLE = 123 # This variable is never imported or used
"""
        main_app_code = """
# This file uses some of the code from the other module
from code import public_api_function

def main():
    result = public_api_function()
    print(result)

main()
"""
        # --- THIS IS THE FIX ---
        # Create an __init__.py to make the directory a package for Vulture
        self.create_file("__init__.py")

        # Create the two files for the test
        f1 = self.create_file("code.py", code_with_dead_functions)
        f2 = self.create_file("main.py", main_app_code)
        
        # Analyze the entire project. Lower confidence to 60 to make test less brittle.
        issues = dead_code.analyze(self.project_path, {'dead_code': {'min_confidence': 60}}, [f1, f2])
        
        messages = [i['message'] for i in issues]
        
        # Check that the specific dead code items were found
        self.assertTrue(any("'os'" in m for m in messages), "Did not find dead 'os' import")
        self.assertTrue(any("'UnusedClass'" in m for m in messages), "Did not find dead 'UnusedClass'")
        self.assertTrue(any("'_internal_helper'" in m for m in messages), "Did not find dead '_internal_helper' function")
        self.assertTrue(any("'DEAD_VARIABLE'" in m for m in messages), "Did not find dead 'DEAD_VARIABLE'")
        
        # Ensure the used function is NOT in the list
        self.assertFalse(any("'public_api_function'" in m for m in messages), "Incorrectly flagged a used function as dead")

    # --- circular_import ---
    def test_circular_import_detector_direct(self):
        f_a = self.create_file("mod_a.py", "import mod_b")
        f_b = self.create_file("mod_b.py", "import mod_a")
        
        issues = circular_import.analyze(self.project_path, {}, [f_a, f_b])
        self.assertEqual(len(issues), 1)
        self.assertIn("mod_a -> mod_b -> mod_a", issues[0]['message'])

    def test_circular_import_detector_indirect(self):
        f_x = self.create_file("mod_x.py", "import mod_y")
        f_y = self.create_file("mod_y.py", "import mod_z")
        f_z = self.create_file("mod_z.py", "import mod_x")
        f_ok = self.create_file("ok.py", "import os")
        
        issues = circular_import.analyze(self.project_path, {}, [f_x, f_y, f_z, f_ok])
        self.assertEqual(len(issues), 1)
        self.assertIn("mod_x -> mod_y -> mod_z -> mod_x", issues[0]['message'])

    def test_circular_import_detector_no_cycle(self):
        f_a = self.create_file("app/main.py", "from app.utils import helper")
        f_b = self.create_file("app/utils.py", "import os")
        
        issues = circular_import.analyze(self.project_path, {}, [f_a, f_b])
        self.assertEqual(len(issues), 0)

# This allows running tests directly from this file
if __name__ == '__main__':
    unittest.main()