#!/usr/bin/env python3
"""
Comprehensive script to generate test templates for all modules.

This script automatically discovers all Python modules in medkit/ and generates
corresponding test files for any modules that don't have tests yet.

Usage:
    python generate_tests.py              # Generate all missing tests
    python generate_tests.py --module-name    # Generate test for specific module
"""

import os
from pathlib import Path
from typing import Dict, Tuple

# Base template for test files
BASE_TEST_TEMPLATE = '''"""
Unit tests for {module_name} module.

This is an auto-generated test template. Please add:
- Proper test cases specific to module functionality
- Realistic test data and assertions
- Edge cases and error handling
- Integration tests where applicable
"""

import unittest
from unittest.mock import Mock, patch, MagicMock

# TODO: Import the module under test
# from medkit.{module_path} import ClassName


class Test{class_name}Models(unittest.TestCase):
    """Test {module_name} data models and classes."""

    def setUp(self):
        """Set up test fixtures."""
        # TODO: Initialize test data and objects
        pass

    def tearDown(self):
        """Clean up after tests."""
        pass

    def test_module_import(self):
        """Test that module can be imported."""
        # TODO: Replace with actual module import
        self.assertTrue(True)

    def test_basic_functionality(self):
        """Test basic module functionality."""
        # TODO: Add actual test cases
        self.assertTrue(True)

    def test_data_validation(self):
        """Test data validation."""
        # TODO: Add validation test cases
        self.assertTrue(True)


class Test{class_name}Integration(unittest.TestCase):
    """Integration tests for {module_name} module."""

    def setUp(self):
        """Set up integration tests."""
        pass

    def test_module_integration(self):
        """Test module integration with other components."""
        # TODO: Add integration test cases
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main(verbosity=2)
'''


def camel_case(snake_str: str) -> str:
    """Convert snake_case to CamelCase."""
    components = snake_str.split('_')
    return ''.join(x.title() for x in components)


def find_all_modules(base_path: str = "medkit") -> list:
    """Find all Python modules in the medkit directory."""
    modules = []
    for root, dirs, files in os.walk(base_path):
        # Skip __pycache__ and __init__.py
        dirs[:] = [d for d in dirs if d != '__pycache__']

        for file in files:
            if file.endswith('.py') and file != '__init__.py':
                module_path = os.path.join(root, file)
                modules.append(module_path)

    return sorted(modules)


def module_path_to_test_name(module_path: str) -> Tuple[str, str]:
    """
    Convert module path to test file name and class name.

    Args:
        module_path: e.g., "medkit/drug/medicine_info.py"

    Returns:
        Tuple of (test_filename, class_name)
        e.g., ("test_medicine_info.py", "MedicineInfo")
    """
    # Get filename without extension
    filename = Path(module_path).stem

    # Create test filename
    test_filename = f"test_{filename}.py"

    # Create class name (CamelCase)
    class_name = camel_case(filename)

    return test_filename, class_name


def get_module_import_path(module_path: str) -> str:
    """
    Convert file path to Python import path.

    Args:
        module_path: e.g., "medkit/drug/medicine_info.py"

    Returns:
        e.g., "medkit.drug.medicine_info"
    """
    return module_path.replace('/', '.').replace('.py', '')


def generate_test_file(module_path: str, test_file_path: str) -> bool:
    """
    Generate a test file for the given module.

    Args:
        module_path: Path to the module file
        test_file_path: Path where test file should be created

    Returns:
        True if generated, False if already exists
    """
    if os.path.exists(test_file_path):
        return False

    test_filename, class_name = module_path_to_test_name(module_path)
    module_name = Path(module_path).stem

    # Generate test content
    test_content = BASE_TEST_TEMPLATE.format(
        module_name=module_name,
        class_name=class_name,
        module_path=get_module_import_path(module_path)
    )

    # Create test file
    os.makedirs(os.path.dirname(test_file_path), exist_ok=True)

    with open(test_file_path, 'w') as f:
        f.write(test_content)

    return True


def main():
    """Generate test files for all modules missing tests."""
    base_path = "medkit"
    tests_dir = "tests"

    print("=" * 80)
    print("MedKit Test Generator - Generating Tests for All Modules")
    print("=" * 80)
    print()

    # Find all modules
    all_modules = find_all_modules(base_path)
    print(f"Found {len(all_modules)} modules in {base_path}/")
    print()

    # Generate tests for missing modules
    generated_count = 0
    skipped_count = 0

    print("Generating test files...")
    print("-" * 80)

    for module_path in all_modules:
        test_filename, _ = module_path_to_test_name(module_path)
        test_file_path = os.path.join(tests_dir, test_filename)

        if generate_test_file(module_path, test_file_path):
            print(f"✓ Generated: {test_file_path}")
            print(f"    for module: {module_path}")
            generated_count += 1
        else:
            skipped_count += 1

    print()
    print("=" * 80)
    print(f"Summary:")
    print(f"  Total modules: {len(all_modules)}")
    print(f"  Test files generated: {generated_count}")
    print(f"  Test files skipped (already exist): {skipped_count}")
    print("=" * 80)
    print()

    if generated_count > 0:
        print(f"✅ Successfully generated {generated_count} test file(s)")
        print()
        print("Next steps:")
        print("  1. Run the generated tests: pytest tests/ -v")
        print("  2. Update test_*.py files with proper test cases")
        print("  3. Replace TODO comments with actual test implementations")
        print("  4. Run coverage: pytest tests/ --cov=medkit")
    else:
        print("✅ All modules already have test files")

    print()


if __name__ == "__main__":
    main()
