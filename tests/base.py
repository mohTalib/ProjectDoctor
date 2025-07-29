# tests/base.py
import unittest
import os
import shutil
import tempfile

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        """Set up a temporary directory to act as the project root."""
        self.project_path = tempfile.mkdtemp()

    def tearDown(self):
        """Remove the temporary directory and its contents."""
        shutil.rmtree(self.project_path)

    def create_file(self, path, content=""):
        """Helper to create a file with content within the test project."""
        full_path = os.path.join(self.project_path, path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return full_path