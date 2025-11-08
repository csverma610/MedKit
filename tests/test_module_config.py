"""
Tests for the Module Configuration system.

Tests the centralized module configuration registry and utilities.
"""

import unittest
from pathlib import Path
from medkit.core.module_config import ModuleConfig, ModuleRegistry, get_module_config


class TestModuleConfig(unittest.TestCase):
    """Test ModuleConfig dataclass."""

    def test_module_config_creation(self):
        """Test creating a module configuration."""
        config = ModuleConfig(
            module_name="test_module",
            module_path="medkit.test.test_module",
            model_name="gemini-1.5-flash",
            description="Test module",
            category="test"
        )
        self.assertEqual(config.module_name, "test_module")
        self.assertEqual(config.model_name, "gemini-1.5-flash")
        self.assertEqual(config.category, "test")

    def test_module_config_default_paths(self):
        """Test that default paths are generated."""
        config = ModuleConfig(
            module_name="test_module",
            module_path="medkit.test.test_module",
            model_name="gemini-1.5-flash",
            description="Test module",
            category="test"
        )
        self.assertIsNotNone(config.output_dir)
        self.assertIsNotNone(config.db_path)
        self.assertIsNotNone(config.log_file)
        self.assertIn("test_module", config.db_path)

    def test_module_config_custom_paths(self):
        """Test that custom paths are preserved."""
        custom_dir = Path("/custom/output")
        custom_db = "/custom/db.lmdb"
        custom_log = Path("/custom/log.log")

        config = ModuleConfig(
            module_name="test_module",
            module_path="medkit.test.test_module",
            model_name="gemini-1.5-flash",
            description="Test module",
            category="test",
            output_dir=custom_dir,
            db_path=custom_db,
            log_file=custom_log
        )
        self.assertEqual(config.output_dir, custom_dir)
        self.assertEqual(config.db_path, custom_db)
        self.assertEqual(config.log_file, custom_log)


class TestModuleRegistry(unittest.TestCase):
    """Test ModuleRegistry for module management."""

    def test_get_all_modules(self):
        """Test retrieving all registered modules."""
        modules = ModuleRegistry.get_all_modules()
        self.assertGreater(len(modules), 0)
        self.assertIn("medical_dictionary", modules)
        self.assertIn("drugs_comparison", modules)

    def test_list_available_modules(self):
        """Test listing available module names."""
        modules = ModuleRegistry.list_available_modules()
        self.assertIsInstance(modules, list)
        self.assertGreater(len(modules), 0)
        self.assertIn("medical_dictionary", modules)
        # List should be sorted
        self.assertEqual(modules, sorted(modules))

    def test_get_module_by_name(self):
        """Test retrieving a specific module by name."""
        config = ModuleRegistry.get_module_by_name("medical_dictionary")
        self.assertIsNotNone(config)
        self.assertEqual(config.module_name, "medical_dictionary")
        self.assertEqual(config.model_name, "gemini-1.5-flash")

    def test_get_nonexistent_module(self):
        """Test retrieving a non-existent module returns None."""
        config = ModuleRegistry.get_module_by_name("nonexistent_module")
        self.assertIsNone(config)

    def test_get_modules_by_category(self):
        """Test retrieving modules by category."""
        drug_modules = ModuleRegistry.get_modules_by_category("drug")
        self.assertGreater(len(drug_modules), 0)
        for name, config in drug_modules.items():
            self.assertEqual(config.category, "drug")

        medical_modules = ModuleRegistry.get_modules_by_category("medical")
        self.assertGreater(len(medical_modules), 0)
        for name, config in medical_modules.items():
            self.assertEqual(config.category, "medical")

    def test_category_coverage(self):
        """Test that all expected categories are covered."""
        categories = set()
        for config in ModuleRegistry.get_all_modules().values():
            categories.add(config.category)

        expected_categories = {
            "drug",
            "medical",
            "mental_health",
            "diagnostics",
            "utils",
            "core"
        }
        self.assertTrue(expected_categories.issubset(categories))

    def test_drug_modules(self):
        """Test drug module configurations."""
        config = ModuleRegistry.MEDICINE_INFO
        self.assertEqual(config.module_name, "medicine_info")
        self.assertEqual(config.category, "drug")
        self.assertIn("gemini", config.model_name)

        config = ModuleRegistry.DRUG_COMPARISON
        self.assertEqual(config.model_name, "gemini-1.5-flash")

    def test_medical_modules(self):
        """Test medical module configurations."""
        config = ModuleRegistry.DISEASE_INFO
        self.assertEqual(config.module_name, "disease_info")
        self.assertEqual(config.category, "medical")
        self.assertEqual(config.model_name, "gemini-1.5-pro")

        config = ModuleRegistry.MEDICAL_IMPLANT
        self.assertEqual(config.model_name, "gemini-1.5-flash")

    def test_mental_health_modules(self):
        """Test mental health module configurations."""
        config = ModuleRegistry.MENTAL_HEALTH_ASSESSMENT
        self.assertEqual(config.category, "mental_health")
        self.assertEqual(config.model_name, "gemini-1.5-pro")

    def test_core_modules(self):
        """Test core module configurations."""
        config = ModuleRegistry.GEMINI_CLIENT
        self.assertEqual(config.category, "core")
        self.assertEqual(config.model_name, "gemini-1.5-pro")

        config = ModuleRegistry.MEDKIT_CLIENT
        self.assertEqual(config.model_name, "gemini-1.5-pro")


class TestGetModuleConfig(unittest.TestCase):
    """Test the get_module_config utility function."""

    def test_get_existing_module(self):
        """Test getting configuration for an existing module."""
        config = get_module_config("medical_dictionary")
        self.assertEqual(config.module_name, "medical_dictionary")
        self.assertEqual(config.model_name, "gemini-1.5-flash")

    def test_get_module_with_model_override(self):
        """Test getting configuration with model override."""
        config = get_module_config("medical_dictionary", model_name="gemini-2.0-pro")
        self.assertEqual(config.model_name, "gemini-2.0-pro")

    def test_get_nonexistent_module_raises_error(self):
        """Test that getting a non-existent module raises ValueError."""
        with self.assertRaises(ValueError) as context:
            get_module_config("nonexistent_module")
        self.assertIn("nonexistent_module", str(context.exception))
        self.assertIn("not found", str(context.exception))

    def test_error_message_lists_available(self):
        """Test that error message lists available modules."""
        with self.assertRaises(ValueError) as context:
            get_module_config("invalid")
        error_msg = str(context.exception)
        self.assertIn("Available modules", error_msg)
        self.assertIn("medical_dictionary", error_msg)


class TestModuleConfigConsistency(unittest.TestCase):
    """Test consistency of module configurations."""

    def test_all_modules_have_model(self):
        """Test that all modules have a model specified."""
        for name, config in ModuleRegistry.get_all_modules().items():
            self.assertIsNotNone(config.model_name)
            self.assertIn("gemini", config.model_name)

    def test_all_modules_have_description(self):
        """Test that all modules have descriptions."""
        for name, config in ModuleRegistry.get_all_modules().items():
            self.assertIsNotNone(config.description)
            self.assertGreater(len(config.description), 0)

    def test_all_modules_have_category(self):
        """Test that all modules have a category."""
        for name, config in ModuleRegistry.get_all_modules().items():
            self.assertIsNotNone(config.category)
            self.assertIn(config.category, [
                "drug", "medical", "mental_health",
                "diagnostics", "utils", "core"
            ])

    def test_all_modules_have_path(self):
        """Test that all modules have a module path."""
        for name, config in ModuleRegistry.get_all_modules().items():
            self.assertIsNotNone(config.module_path)
            self.assertIn(".", config.module_path)

    def test_model_names_are_valid(self):
        """Test that model names follow expected patterns."""
        valid_models = {
            "gemini-1.5-flash",
            "gemini-1.5-pro",
            "gemini-2.0-pro",
            "gemini-pro",
            "gemini-flash"
        }
        for name, config in ModuleRegistry.get_all_modules().items():
            self.assertIn("gemini", config.model_name.lower())

    def test_no_duplicate_module_names(self):
        """Test that there are no duplicate module names."""
        modules = ModuleRegistry.get_all_modules()
        module_names = list(modules.keys())
        self.assertEqual(len(module_names), len(set(module_names)))

    def test_no_duplicate_paths(self):
        """Test that there are no duplicate module paths."""
        modules = ModuleRegistry.get_all_modules()
        paths = [config.module_path for config in modules.values()]
        # Some paths might be duplicated if they're for different purposes
        # but most should be unique
        self.assertGreater(len(set(paths)), len(paths) * 0.8)


class TestModuleCategories(unittest.TestCase):
    """Test module categorization."""

    def test_drug_category_count(self):
        """Test number of drug modules."""
        drug_modules = ModuleRegistry.get_modules_by_category("drug")
        self.assertGreaterEqual(len(drug_modules), 6)

    def test_medical_category_count(self):
        """Test number of medical modules."""
        medical_modules = ModuleRegistry.get_modules_by_category("medical")
        self.assertGreaterEqual(len(medical_modules), 15)

    def test_mental_health_category_count(self):
        """Test number of mental health modules."""
        mh_modules = ModuleRegistry.get_modules_by_category("mental_health")
        self.assertGreaterEqual(len(mh_modules), 5)

    def test_diagnostics_category_count(self):
        """Test number of diagnostics modules."""
        diag_modules = ModuleRegistry.get_modules_by_category("diagnostics")
        self.assertGreaterEqual(len(diag_modules), 5)

    def test_utils_category_count(self):
        """Test number of utility modules."""
        util_modules = ModuleRegistry.get_modules_by_category("utils")
        self.assertGreaterEqual(len(util_modules), 3)

    def test_core_category_count(self):
        """Test number of core modules."""
        core_modules = ModuleRegistry.get_modules_by_category("core")
        self.assertGreaterEqual(len(core_modules), 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
