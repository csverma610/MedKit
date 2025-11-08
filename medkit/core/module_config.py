"""
Module Configuration Management - Centralized LLM model configuration for all modules.

This module provides centralized configuration management for all MedKit modules,
ensuring consistent model naming and easy updates across the entire codebase.

USAGE:
    from medkit.core.module_config import ModuleConfig, get_module_config

    # Get default config for a module
    config = get_module_config("medical_dictionary")
    print(config.model_name)  # Output: gemini-1.5-flash

    # Get custom config
    config = get_module_config("drug_comparison", model_name="gemini-2.0-pro")

    # Access all available modules
    available = ModuleConfig.get_available_modules()
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, List
from pathlib import Path
import sys


def _is_running_tests() -> bool:
    """Detect if code is running under pytest."""
    return "pytest" in sys.modules or "PYTEST_CURRENT_TEST" in sys.environ


@dataclass
class ModuleConfig:
    """Configuration container for a module with LLM model specification.

    Attributes:
        module_name: Name of the module
        module_path: Module path (e.g., medkit.drug.medicine_info)
        model_name: LLM model name for this module
        description: Module description
        category: Module category (drug, medical, mental_health, diagnostics, utils)
        output_dir: Output directory for module results
        db_path: Path to LMDB database cache
        db_capacity_mb: Database capacity in MB
        db_store: Whether to store results in database
        log_file: Path to log file
    """

    module_name: str
    module_path: str
    model_name: str
    description: str
    category: str
    output_dir: Optional[Path] = None
    db_path: Optional[str] = None
    db_capacity_mb: int = 500
    db_store: bool = True
    log_file: Optional[Path] = None

    def __post_init__(self):
        """Initialize default paths if not provided."""
        if self.output_dir is None:
            self.output_dir = Path("outputs")

        if self.db_path is None and self.module_name:
            self.db_path = str(
                Path(__file__).parent.parent / "storage" / f"{self.module_name}.lmdb"
            )

        if self.log_file is None and self.module_name:
            self.log_file = Path(__file__).parent.parent / "logs" / f"{self.module_name}.log"

        # Disable database storage during tests to avoid side effects
        if _is_running_tests():
            self.db_store = False


class ModuleRegistry:
    """Central registry of all MedKit modules with their configurations."""

    # ============================================================================
    # DRUG MODULES
    # ============================================================================

    MEDICINE_INFO = ModuleConfig(
        module_name="medicine_info",
        module_path="medkit.drug.medicine_info",
        model_name="gemini-1.5-flash",
        description="Generate comprehensive medicine information including indications, side effects, dosage, and interactions",
        category="drug"
    )

    DRUG_COMPARISON = ModuleConfig(
        module_name="drugs_comparison",
        module_path="medkit.drug.drugs_comparison",
        model_name="gemini-1.5-flash",
        description="Compare medicines side-by-side across clinical, regulatory, and practical metrics",
        category="drug"
    )

    DRUG_DRUG_INTERACTION = ModuleConfig(
        module_name="drug_drug_interaction",
        module_path="medkit.drug.drug_drug_interaction",
        model_name="gemini-1.5-pro",
        description="Analyze drug-drug interactions and provide clinical guidance",
        category="drug"
    )

    DRUG_DISEASE_INTERACTION = ModuleConfig(
        module_name="drug_disease_interaction",
        module_path="medkit.drug.drug_disease_interaction",
        model_name="gemini-1.5-pro",
        description="Analyze drug-disease interactions and provide clinical recommendations",
        category="drug"
    )

    DRUG_FOOD_INTERACTION = ModuleConfig(
        module_name="drug_food_interaction",
        module_path="medkit.drug.drug_food_interaction",
        model_name="gemini-1.5-flash",
        description="Analyze drug-food interactions and dietary considerations",
        category="drug"
    )

    SIMILAR_DRUGS = ModuleConfig(
        module_name="similar_drugs",
        module_path="medkit.drug.similar_drugs",
        model_name="gemini-1.5-flash",
        description="Find similar drugs with comparable therapeutic effects and mechanisms",
        category="drug"
    )

    RXNORM_CLIENT = ModuleConfig(
        module_name="rxnorm_client",
        module_path="medkit.drug.rxnorm_client",
        model_name="gemini-1.5-flash",
        description="Interface with RxNorm drug database for comprehensive drug information",
        category="drug"
    )

    RX_MED_INFO = ModuleConfig(
        module_name="rx_med_info",
        module_path="medkit.drug.rx_med_info",
        model_name="gemini-1.5-flash",
        description="RxNorm-based medication information generator",
        category="drug"
    )

    RXCLASS_EXAMPLES = ModuleConfig(
        module_name="rxclass_examples",
        module_path="medkit.drug.rxclass_examples",
        model_name="gemini-1.5-flash",
        description="RxClass drug classification examples and categorization",
        category="drug"
    )

    # ============================================================================
    # MEDICAL MODULES
    # ============================================================================

    MEDICAL_DICTIONARY = ModuleConfig(
        module_name="medical_dictionary",
        module_path="medkit.medical.medical_dictionary",
        model_name="gemini-1.5-flash",
        description="AI-generated medical term definitions and explanations",
        category="medical"
    )

    MEDICAL_ANATOMY = ModuleConfig(
        module_name="medical_anatomy",
        module_path="medkit.medical.medical_anatomy",
        model_name="gemini-1.5-flash",
        description="Generate comprehensive medical anatomy information",
        category="medical"
    )

    DISEASE_INFO = ModuleConfig(
        module_name="disease_info",
        module_path="medkit.medical.disease_info",
        model_name="gemini-1.5-pro",
        description="Generate comprehensive disease information including symptoms, diagnosis, and treatment",
        category="medical"
    )

    MEDICAL_IMPLANT = ModuleConfig(
        module_name="medical_implant",
        module_path="medkit.medical.medical_implant",
        model_name="gemini-1.5-flash",
        description="Generate comprehensive medical implant documentation",
        category="medical"
    )

    MEDICAL_PROCEDURE_INFO = ModuleConfig(
        module_name="medical_procedure_info",
        module_path="medkit.medical.medical_procedure_info",
        model_name="gemini-1.5-flash",
        description="Generate medical procedure information and guidelines",
        category="medical"
    )

    SURGICAL_TOOL_INFO = ModuleConfig(
        module_name="surgical_tool_info",
        module_path="medkit.medical.surgical_tool_info",
        model_name="gemini-1.5-flash",
        description="Generate surgical tool and instrument information",
        category="medical"
    )

    SURGERY_INFO = ModuleConfig(
        module_name="surgery_info",
        module_path="medkit.medical.surgery_info",
        model_name="gemini-1.5-flash",
        description="Generate surgical procedure information",
        category="medical"
    )

    MEDICAL_FAQ = ModuleConfig(
        module_name="medical_faq",
        module_path="medkit.medical.medical_faq",
        model_name="gemini-1.5-flash",
        description="Generate medical FAQs and common questions",
        category="medical"
    )

    MEDICAL_SPECIALITY = ModuleConfig(
        module_name="medical_speciality",
        module_path="medkit.medical.medical_speciality",
        model_name="gemini-1.5-flash",
        description="Generate medical specialty information",
        category="medical"
    )

    MEDICAL_TOPIC = ModuleConfig(
        module_name="medical_topic",
        module_path="medkit.medical.medical_topic",
        model_name="gemini-1.5-flash",
        description="Generate comprehensive medical topic information",
        category="medical"
    )

    MEDICAL_TERM_EXTRACTOR = ModuleConfig(
        module_name="medical_term_extractor",
        module_path="medkit.medical.medical_term_extractor",
        model_name="gemini-1.5-flash",
        description="Extract and categorize medical terms from text",
        category="medical"
    )

    MEDICAL_FACTS_CHECKER = ModuleConfig(
        module_name="medical_facts_checker",
        module_path="medkit.medical.medical_facts_checker",
        model_name="gemini-1.5-pro",
        description="Verify and validate medical facts and claims",
        category="medical"
    )

    MEDICAL_DECISION_GUIDE = ModuleConfig(
        module_name="medical_decision_guide",
        module_path="medkit.medical.medical_decision_guide",
        model_name="gemini-1.5-pro",
        description="Generate medical decision support guides",
        category="medical"
    )

    MEDICAL_TEST_INFO = ModuleConfig(
        module_name="medical_test_info",
        module_path="medkit.medical.medical_test_info",
        model_name="gemini-1.5-flash",
        description="Generate medical test and diagnostic information",
        category="medical"
    )

    MEDICAL_TEST_DEVICES = ModuleConfig(
        module_name="medical_test_devices",
        module_path="medkit.medical.medical_test_devices",
        model_name="gemini-1.5-flash",
        description="Generate medical testing device information",
        category="medical"
    )

    HERBAL_INFO = ModuleConfig(
        module_name="herbal_info",
        module_path="medkit.medical.herbal_info",
        model_name="gemini-1.5-flash",
        description="Generate herbal and botanical medicine information",
        category="medical"
    )

    PRESCRIPTION_ANALYZER = ModuleConfig(
        module_name="prescription_analyzer",
        module_path="medkit.medical.prescription_analyzer",
        model_name="gemini-1.5-flash",
        description="Analyze and validate prescriptions",
        category="medical"
    )

    PRESCRIPTION_EXTRACTOR = ModuleConfig(
        module_name="prescription_extractor",
        module_path="medkit.medical.prescription_extractor",
        model_name="gemini-1.5-flash",
        description="Extract structured data from prescriptions",
        category="medical"
    )

    EXAM_SPECIFICATIONS = ModuleConfig(
        module_name="exam_specifications",
        module_path="medkit.medical.exam_specifications",
        model_name="gemini-1.5-flash",
        description="Medical exam specifications and protocols",
        category="medical"
    )

    PATIENT_MEDICAL_HISTORY = ModuleConfig(
        module_name="patient_medical_history",
        module_path="medkit.medical.patient_medical_history",
        model_name="gemini-1.5-pro",
        description="Manage and analyze patient medical history",
        category="medical"
    )

    SYNTHETIC_CASE_REPORT = ModuleConfig(
        module_name="synthetic_case_report",
        module_path="medkit.medical.synthetic_case_report",
        model_name="gemini-1.5-pro",
        description="Generate synthetic case reports for educational purposes",
        category="medical"
    )

    USER_GUIDE = ModuleConfig(
        module_name="user_guide",
        module_path="medkit.medical.user_guide",
        model_name="gemini-1.5-flash",
        description="Generate user guides and educational materials",
        category="medical"
    )

    EXAM_NUTRITION_GROWTH = ModuleConfig(
        module_name="exam_nutrition_growth",
        module_path="medkit.phyexams.exam_nutrition_growth",
        model_name="gemini-2.5-flash",
        description="Comprehensive nutrition and growth measurements assessment with clinical recommendations",
        category="medical"
    )

    EXAM_MUSCULOSKELETAL = ModuleConfig(
        module_name="exam_musculoskeletal",
        module_path="medkit.phyexams.exam_musculoskeletal",
        model_name="gemini-1.5-flash",
        description="Musculoskeletal examination and assessment",
        category="medical"
    )

    # ============================================================================
    # MENTAL HEALTH MODULES
    # ============================================================================

    MENTAL_HEALTH_ASSESSMENT = ModuleConfig(
        module_name="mental_health_assessment",
        module_path="medkit.mental_health.mental_health_assessment",
        model_name="gemini-1.5-pro",
        description="Comprehensive mental health assessment framework",
        category="mental_health"
    )

    MENTAL_HEALTH_CHAT = ModuleConfig(
        module_name="mental_health_chat",
        module_path="medkit.mental_health.mental_health_chat",
        model_name="gemini-1.5-pro",
        description="Mental health chatbot with therapeutic capabilities",
        category="mental_health"
    )

    MENTAL_HEALTH_REPORT = ModuleConfig(
        module_name="mental_health_report",
        module_path="medkit.mental_health.mental_health_report",
        model_name="gemini-1.5-pro",
        description="Generate mental health assessment reports",
        category="mental_health"
    )

    SANE_INTERVIEW = ModuleConfig(
        module_name="sane_interview",
        module_path="medkit.mental_health.sane_interview",
        model_name="gemini-1.5-pro",
        description="SANE interview assessment protocol",
        category="mental_health"
    )

    LLM_SANE_INTERVIEW = ModuleConfig(
        module_name="llm_sane_interview",
        module_path="medkit.mental_health.llm_sane_interview",
        model_name="gemini-1.5-pro",
        description="LLM-powered SANE interview assessment",
        category="mental_health"
    )

    SYMPTON_DETECTION_CHAT = ModuleConfig(
        module_name="sympton_detection_chat",
        module_path="medkit.mental_health.sympton_detection_chat",
        model_name="gemini-1.5-pro",
        description="Symptom detection and analysis chatbot",
        category="mental_health"
    )

    MENTAL_HEALTH_CHAT_APP = ModuleConfig(
        module_name="mental_health_chat_app",
        module_path="medkit.mental_health.mental_health_chat_app",
        model_name="gemini-1.5-pro",
        description="Full-featured mental health chat application",
        category="mental_health"
    )

    # ============================================================================
    # DIAGNOSTICS MODULES
    # ============================================================================

    MEDICAL_TESTS_GRAPH = ModuleConfig(
        module_name="medical_tests_graph",
        module_path="medkit.diagnostics.medical_tests_graph",
        model_name="gemini-1.5-flash",
        description="Graph representation of medical tests and relationships",
        category="diagnostics"
    )

    MEDICAL_DECISION_GUIDE_DIAG = ModuleConfig(
        module_name="medical_decision_guide_diag",
        module_path="medkit.diagnostics.medical_decision_guide",
        model_name="gemini-1.5-pro",
        description="Diagnostic decision support guide",
        category="diagnostics"
    )

    EXAM_SPECIFICATIONS_DIAG = ModuleConfig(
        module_name="exam_specifications_diag",
        module_path="medkit.diagnostics.exam_specifications",
        model_name="gemini-1.5-flash",
        description="Diagnostic exam specifications",
        category="diagnostics"
    )

    MEDICAL_PHYSICAL_EXAMS_QUESTIONS = ModuleConfig(
        module_name="medical_physical_exams_questions",
        module_path="medkit.diagnostics.medical_physical_exams_questions",
        model_name="gemini-1.5-flash",
        description="Physical exam questions and protocols",
        category="diagnostics"
    )

    EVAL_PHYSICAL_EXAM_QUESTIONS = ModuleConfig(
        module_name="eval_physical_exam_questions",
        module_path="medkit.diagnostics.eval_physical_exam_questions",
        model_name="gemini-1.5-flash",
        description="Evaluation of physical exam questions",
        category="diagnostics"
    )

    PRESCRIPTION_EXTRACTOR_DIAG = ModuleConfig(
        module_name="prescription_extractor_diag",
        module_path="medkit.diagnostics.prescription_extractor",
        model_name="gemini-1.5-flash",
        description="Diagnostic prescription extraction",
        category="diagnostics"
    )

    PRESCRIPTION_ANALYZER_DIAG = ModuleConfig(
        module_name="prescription_analyzer_diag",
        module_path="medkit.diagnostics.prescription_analyzer",
        model_name="gemini-1.5-flash",
        description="Diagnostic prescription analysis",
        category="diagnostics"
    )

    # ============================================================================
    # UTILITY MODULES
    # ============================================================================

    LMDB_STORAGE = ModuleConfig(
        module_name="lmdb_storage",
        module_path="medkit.utils.lmdb_storage",
        model_name="gemini-1.5-flash",
        description="LMDB database storage utility",
        category="utils"
    )

    PYDANTIC_PROMPT_GENERATOR = ModuleConfig(
        module_name="pydantic_prompt_generator",
        module_path="medkit.utils.pydantic_prompt_generator",
        model_name="gemini-1.5-flash",
        description="Generate prompts from Pydantic models",
        category="utils"
    )

    PRIVACY_COMPLIANCE = ModuleConfig(
        module_name="privacy_compliance",
        module_path="medkit.utils.privacy_compliance",
        model_name="gemini-1.5-flash",
        description="Privacy and compliance utilities",
        category="utils"
    )

    REFACTORING_AUTOMATION = ModuleConfig(
        module_name="refactoring_automation",
        module_path="medkit.utils.refactoring_automation",
        model_name="gemini-1.5-flash",
        description="Automated code refactoring utilities",
        category="utils"
    )

    UPDATE_QUESTION_IDS = ModuleConfig(
        module_name="update_question_ids",
        module_path="medkit.utils.update_question_ids",
        model_name="gemini-1.5-flash",
        description="Question ID update utility",
        category="utils"
    )

    # ============================================================================
    # VISUALIZATION MODULES
    # ============================================================================

    VISUALIZE_DECISION_GUIDE_MED = ModuleConfig(
        module_name="visualize_decision_guide_med",
        module_path="medkit.medical.visualize_decision_guide",
        model_name="gemini-1.5-flash",
        description="Visualization of medical decision guides",
        category="medical"
    )

    VISUALIZE_DECISION_GUIDE_VIS = ModuleConfig(
        module_name="visualize_decision_guide_vis",
        module_path="medkit.vistools.visualize_decision_guide",
        model_name="gemini-1.5-flash",
        description="Visualization tools for decision guides",
        category="utils"
    )

    # ============================================================================
    # CORE MODULES
    # ============================================================================

    GEMINI_CLIENT = ModuleConfig(
        module_name="gemini_client",
        module_path="medkit.core.gemini_client",
        model_name="gemini-1.5-pro",
        description="Gemini API client for LLM operations",
        category="core"
    )

    MEDKIT_CLIENT = ModuleConfig(
        module_name="medkit_client",
        module_path="medkit.core.medkit_client",
        model_name="gemini-1.5-pro",
        description="MedKit client for unified API operations",
        category="core"
    )

    @classmethod
    def get_all_modules(cls) -> Dict[str, ModuleConfig]:
        """Get all registered modules."""
        modules = {}
        for attr_name in dir(cls):
            attr = getattr(cls, attr_name)
            if isinstance(attr, ModuleConfig):
                modules[attr.module_name] = attr
        return modules

    @classmethod
    def get_module_by_name(cls, module_name: str) -> Optional[ModuleConfig]:
        """Get a module configuration by name."""
        modules = cls.get_all_modules()
        return modules.get(module_name)

    @classmethod
    def get_modules_by_category(cls, category: str) -> Dict[str, ModuleConfig]:
        """Get all modules in a specific category."""
        return {
            name: config
            for name, config in cls.get_all_modules().items()
            if config.category == category
        }

    @classmethod
    def list_available_modules(cls) -> List[str]:
        """List all available module names."""
        return sorted(cls.get_all_modules().keys())


def get_module_config(
    module_name: str,
    model_name: Optional[str] = None
) -> ModuleConfig:
    """
    Get configuration for a module.

    Args:
        module_name: Name of the module
        model_name: Optional override for model name

    Returns:
        ModuleConfig instance

    Raises:
        ValueError: If module_name is not found in registry
    """
    config = ModuleRegistry.get_module_by_name(module_name)

    if config is None:
        available = ModuleRegistry.list_available_modules()
        raise ValueError(
            f"Module '{module_name}' not found in registry. "
            f"Available modules: {', '.join(available)}"
        )

    # Override model_name if provided
    if model_name:
        config.model_name = model_name

    return config


# Export commonly used items
__all__ = [
    'ModuleConfig',
    'ModuleRegistry',
    'get_module_config',
]
