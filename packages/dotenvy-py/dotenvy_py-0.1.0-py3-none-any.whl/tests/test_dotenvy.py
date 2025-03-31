import os
import tempfile
from pathlib import Path
import unittest
import shutil

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
import dotenvy_py

class TestDotenvy(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for tests
        self.test_dir = tempfile.mkdtemp()
        self.original_env = os.environ.copy()
        
    def tearDown(self):
        # Restore original environment
        os.environ.clear()
        os.environ.update(self.original_env)
        # Remove temporary directory
        shutil.rmtree(self.test_dir)
        
    def create_env_file(self, filename, content):
        path = Path(self.test_dir) / filename
        with open(path, 'w') as f:
            f.write(content)
        return path
        
    def test_basic_loading(self):
        # Create a basic .env file
        env_content = """
        TEST_VAR=test_value
        # This is a comment
        ANOTHER_VAR="quoted value"
        """
        env_path = self.create_env_file('.env', env_content)
        
        # Change to the test directory
        original_dir = os.getcwd()
        os.chdir(self.test_dir)
        
        try:
            # Load the .env file
            result = dotenvy_py.dotenv()
            self.assertEqual(result.name, env_path.name)
            
            # Check that environment variables were set
            self.assertEqual(os.environ.get('TEST_VAR'), 'test_value')
            self.assertEqual(os.environ.get('ANOTHER_VAR'), 'quoted value')
        finally:
            # Change back to original directory
            os.chdir(original_dir)
            
    def test_first_occurrence_wins(self):
        # Create a .env file with duplicate keys
        env_content = """
        DUPLICATE_VAR=first_value
        OTHER_VAR=other_value
        DUPLICATE_VAR=second_value
        """
        env_path = self.create_env_file('.env', env_content)
        
        # Set an environment variable that's also in the .env file
        os.environ['OTHER_VAR'] = 'original_value'
        
        # Change to the test directory
        original_dir = os.getcwd()
        os.chdir(self.test_dir)
        
        try:
            # Load the .env file
            dotenvy_py.dotenv()
            
            # The first occurrence of DUPLICATE_VAR should win
            self.assertEqual(os.environ.get('DUPLICATE_VAR'), 'first_value')
            
            # Existing environment variables should be preserved
            self.assertEqual(os.environ.get('OTHER_VAR'), 'original_value')
        finally:
            # Change back to original directory
            os.chdir(original_dir)
            
    def test_priority_loading(self):
        # Create two .env files
        env1_content = """
        SHARED_VAR=env1_value
        ENV1_ONLY=env1_specific
        """
        env2_content = """
        SHARED_VAR=env2_value
        ENV2_ONLY=env2_specific
        """
        
        env1_path = self.create_env_file('.env.specific', env1_content)
        env2_path = self.create_env_file('.env', env2_content)
        
        # Change to the test directory
        original_dir = os.getcwd()
        os.chdir(self.test_dir)
        
        try:
            # Load files in priority order
            loaded = dotenvy_py.load_with_priority(['.env.specific', '.env'])
            
            # Both files should have been loaded
            self.assertEqual(len(loaded), 2)
            self.assertEqual(loaded[0], env1_path)
            self.assertEqual(loaded[1], env2_path)
            
            # First file's values should win for shared variables
            self.assertEqual(os.environ.get('SHARED_VAR'), 'env1_value')
            
            # Both files' unique variables should be loaded
            self.assertEqual(os.environ.get('ENV1_ONLY'), 'env1_specific')
            self.assertEqual(os.environ.get('ENV2_ONLY'), 'env2_specific')
        finally:
            # Change back to original directory
            os.chdir(original_dir)
            
    def test_find_upwards(self):
        # Create nested directory structure
        nested_dir = Path(self.test_dir) / "level1" / "level2"
        nested_dir.mkdir(parents=True)
        
        # Create .env file in the root test directory
        env_content = "ROOT_VAR=root_value"
        env_path = self.create_env_file('.env', env_content)
        
        # Change to the nested directory
        original_dir = os.getcwd()
        os.chdir(nested_dir)
        
        try:
            # Find the .env file in a parent directory
            found_path = dotenvy_py.find_upwards()
            self.assertEqual(found_path, env_path)
            
            # Load it
            dotenvy_py.from_filename(found_path)
            self.assertEqual(os.environ.get('ROOT_VAR'), 'root_value')
        finally:
            # Change back to original directory
            os.chdir(original_dir)

if __name__ == '__main__':
    unittest.main() 