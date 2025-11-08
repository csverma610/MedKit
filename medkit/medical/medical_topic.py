"""medical_topic - Generate comprehensive medical topic documentation with FAQs.

This module generates detailed, evidence-based medical information for any health topic,
disease, or medical condition. It creates complete documentation including epidemiology,
pathophysiology, clinical presentation, diagnosis, treatment, and prognosis. The module
automatically generates and embeds patient-friendly FAQs using the MedKit AI client with
structured Pydantic schemas.

QUICK START:
    Generate medical topic information with embedded FAQ:

    >>> from medical_topic import MedicalTopicGenerator
    >>> generator = MedicalTopicGenerator()
    >>> result = generator.generate("Diabetes")
    >>> print(result.overview.topic_name)
    Diabetes

    Or use the CLI:

    $ python medical_topic.py -i "Hypertension"
    $ python medical_topic.py -i "Asthma" -o custom_output.json

COMMON USES:
    1. Patient education portals - comprehensive yet accessible health information
    2. Medical reference - detailed topic documentation for healthcare providers
    3. Content creation - source material for health blogs and educational websites
    4. Diagnostic guides - symptom patterns, differential diagnosis information
    5. Treatment planning - evidence-based treatment options and prognosis data

KEY FEATURES AND COVERAGE AREAS:
    - Topic overview: definition, classification, medical specialties
    - Epidemiology: incidence, prevalence, demographics, at-risk populations
    - Etiology: causes, genetic factors, environmental triggers, risk factors
    - Pathophysiology: disease mechanisms, cellular changes, progression stages
    - Clinical presentation: symptoms, severity spectrum, onset patterns
    - Diagnosis: diagnostic tests, imaging, lab findings, differential diagnosis
    - Complications: acute and chronic complications, mortality and disability outcomes
    - Treatment: first-line therapies, medications, lifestyle modifications
    - Prognosis: expected outcomes, remission potential, quality of life impact
    - Prevention: primary and secondary prevention, screening recommendations
    - Research and evidence: clinical guidelines, emerging treatments, clinical trials
    - Psychosocial impact: mental health effects, coping strategies, support resources
    - Special populations: pediatric, geriatric, pregnancy, gender-specific aspects
    - Cost and impact: healthcare costs, productivity loss, insurance considerations
    - Patient education: key takeaways, misconceptions, when to seek care
    - Embedded patient FAQ: 8-10 common questions, misconceptions, care guidance
"""

import json
import sys
import logging
import argparse
from pathlib import Path
from dataclasses import dataclass, field
from pydantic import BaseModel, Field
from typing import Optional

from medkit.core.medkit_client import MedKitClient
from medkit.core.module_config import get_module_config
from medkit.medical.medical_faq import FAQGenerator, PatientFAQ

from medkit.utils.logging_config import setup_logger

import hashlib
from medkit.utils.lmdb_storage import LMDBStorage, LMDBConfig
from medkit.utils.storage_config import StorageConfig

# Configure logging
logger = setup_logger(__name__)

# ============================================================================ 
# CONFIGURATION
# ============================================================================ 

@dataclass
class Config(StorageConfig):
    """Configuration for the medical topic generator."""
    output_dir: Path = field(default_factory=lambda: Path("outputs"))
    log_file: Path = field(default_factory=lambda: Path(__file__).parent / "logs" / f"{Path(__file__).stem}.log")
    verbosity: int = 2  # Verbosity level: 0=CRITICAL, 1=ERROR, 2=WARNING, 3=INFO, 4=DEBUG

    def __post_init__(self):
        """Set default db_path if not provided, then validate."""
        if self.db_path is None:
            self.db_path = str(
                Path(__file__).parent.parent / "storage" / "medical_topic.lmdb"
            )
        # Call parent validation
        super().__post_init__()
# ============================================================================ 
# PYDANTIC MODELS FOR TOPIC STRUCTURE
# ============================================================================ 

class TopicOverview(BaseModel):
    """Basic information about the medical topic."""
    topic_name: str = Field(description="Official name of the medical topic")
    alternative_names: str = Field(description="Other names or abbreviations for this topic, comma-separated")
    topic_category: str = Field(description="Category (disease, condition, syndrome, disorder, etc)")
    medical_specialties: str = Field(description="Primary medical specialties that focus on this topic, comma-separated")
    prevalence: str = Field(description="How common this condition is in the population")


class Definition(BaseModel):
    """Definition and basic understanding of the topic."""
    plain_language_explanation: str = Field(description="Simple explanation for general audience")
    medical_definition: str = Field(description="Formal medical definition")
    key_characteristics: str = Field(description="Main defining characteristics, comma-separated")
    disease_classification: str = Field(description="How this condition is classified medically")


class Epidemiology(BaseModel):
    """Statistical and demographic information."""
    incidence_rate: str = Field(description="How many new cases occur per year")
    prevalence_rate: str = Field(description="What percentage of population has this condition")
    age_of_onset: str = Field(description="Typical age when condition appears")
    gender_differences: str = Field(description="Whether males or females are more affected")
    geographic_variation: str = Field(description="Whether condition varies by geography or population")
    risk_groups: str = Field(description="Populations at highest risk, comma-separated")


class Etiology(BaseModel):
    """Causes and risk factors."""
    primary_causes: str = Field(description="Main causes of this condition, comma-separated")
    genetic_factors: str = Field(description="Genetic predisposition or inheritance patterns")
    environmental_factors: str = Field(description="Environmental triggers or exposures, comma-separated")
    lifestyle_factors: str = Field(description="Lifestyle factors that increase risk, comma-separated")
    infectious_agents: str = Field(description="If applicable, organisms that cause this condition")
    contributing_factors: str = Field(description="Other factors that contribute to development, comma-separated")


class Pathophysiology(BaseModel):
    """How the condition develops and progresses."""
    mechanism_of_disease: str = Field(description="Biological mechanism of how disease develops")
    affected_systems: str = Field(description="Body systems or organs affected, comma-separated")
    cellular_changes: str = Field(description="Changes at cellular or molecular level")
    progression_stages: str = Field(description="How condition progresses over time, comma-separated")
    inflammatory_response: str = Field(description="Role of inflammation if applicable")
    immune_involvement: str = Field(description="Role of immune system if applicable")


class ClinicalPresentation(BaseModel):
    """Symptoms and clinical signs."""
    primary_symptoms: str = Field(description="Main symptoms patients experience, comma-separated")
    secondary_symptoms: str = Field(description="Associated or secondary symptoms, comma-separated")
    symptom_onset: str = Field(description="How symptoms typically begin and develop")
    severity_spectrum: str = Field(description="Range from mild to severe presentations")
    acute_vs_chronic: str = Field(description="Whether condition is acute, chronic, or can be both")
    symptom_triggers: str = Field(description="What triggers or worsens symptoms, comma-separated")
    asymptomatic_presentation: str = Field(description="Whether condition can exist without symptoms")


class Diagnosis(BaseModel):
    """Diagnostic methods and criteria."""
    diagnostic_tests: str = Field(description="Tests used to diagnose this condition, comma-separated")
    imaging_studies: str = Field(description="Imaging procedures if applicable, comma-separated")
    laboratory_findings: str = Field(description="Lab results indicative of condition")
    diagnostic_criteria: str = Field(description="Clinical criteria used to confirm diagnosis")
    differential_diagnosis: str = Field(description="Similar conditions to rule out, comma-separated")
    diagnostic_challenges: str = Field(description="Difficulties in diagnosis and why")
    time_to_diagnosis: str = Field(description="Average time from symptom onset to diagnosis")


class Complications(BaseModel):
    """Potential complications and sequelae."""
    acute_complications: str = Field(description="Short-term complications, comma-separated")
    chronic_complications: str = Field(description="Long-term complications from untreated disease, comma-separated")
    complication_rates: str = Field(description="How often complications occur")
    organ_system_effects: str = Field(description="Which organ systems can be affected, comma-separated")
    mortality_rate: Optional[str] = Field(description="Risk of death if applicable")
    disability_outcomes: str = Field(description="Potential long-term disability or functional impairment")


class Treatment(BaseModel):
    """Treatment options and management."""
    first_line_treatment: str = Field(description="Standard initial treatment")
    medications: str = Field(description="Common medications used, comma-separated")
    surgical_interventions: str = Field(description="Surgical options if applicable, comma-separated")
    physical_therapy: str = Field(description="Role of physical therapy or rehabilitation")
    lifestyle_modifications: str = Field(description="Lifestyle changes recommended, comma-separated")
    dietary_management: str = Field(description="Dietary modifications if applicable")
    complementary_approaches: str = Field(description="Alternative or complementary therapies, comma-separated")
    treatment_duration: str = Field(description="How long treatment typically lasts")


class Prognosis(BaseModel):
    """Expected outcomes and long-term outlook."""
    overall_prognosis: str = Field(description="General expected outcome")
    remission_possibility: str = Field(description="Whether condition can go into remission or resolve")
    cure_potential: str = Field(description="Whether condition is curable")
    recovery_rates: str = Field(description="Percentage of people who recover or improve")
    factors_affecting_prognosis: str = Field(description="What factors influence outcomes, comma-separated")
    long_term_outlook: str = Field(description="What to expect over years or decades")
    quality_of_life_impact: str = Field(description="Expected impact on daily functioning and quality of life")


class Prevention(BaseModel):
    """Prevention and risk reduction strategies."""
    primary_prevention: str = Field(description="Strategies to prevent disease onset, comma-separated")
    secondary_prevention: str = Field(description="Early detection and intervention strategies, comma-separated")
    screening_recommendations: str = Field(description="Who should be screened and how often")
    protective_factors: str = Field(description="Factors that reduce risk, comma-separated")
    lifestyle_prevention: str = Field(description="Lifestyle choices that prevent condition, comma-separated")
    vaccinations: str = Field(description="Vaccines if applicable")


class ResearchAndEvidence(BaseModel):
    """Current evidence and research."""
    evidence_quality: str = Field(description="Quality of current evidence")
    current_research_areas: str = Field(description="Active areas of research, comma-separated")
    emerging_treatments: str = Field(description="Promising new treatments in development")
    clinical_trials: str = Field(description="Availability and types of clinical trials")
    guideline_sources: str = Field(description="Major clinical guidelines and organizations, comma-separated")


class PsychosocialImpact(BaseModel):
    """Mental health and quality of life aspects."""
    mental_health_effects: str = Field(description="Psychological effects like depression or anxiety")
    emotional_burden: str = Field(description="Emotional challenges patients face")
    social_impact: str = Field(description="Impact on relationships and social functioning")
    occupational_impact: str = Field(description="Effect on work and employment")
    coping_strategies: str = Field(description="Strategies to manage psychological impact, comma-separated")
    support_resources: str = Field(description="Mental health and support resources, comma-separated")


class TopicEducation(BaseModel):
    """Patient education and communication."""
    key_takeaways: str = Field(description="3-5 most important points, comma-separated")
    common_misconceptions: str = Field(description="Common myths about this condition, comma-separated")
    frequently_asked_questions: str = Field(description="Common patient questions and answers")
    when_to_see_doctor: str = Field(description="Symptoms or situations requiring medical attention")


class SpecialPopulations(BaseModel):
    """Considerations for specific groups."""
    pediatric_considerations: str = Field(description="Special aspects in children if applicable")
    geriatric_considerations: str = Field(description="Special aspects in elderly if applicable")
    pregnancy_considerations: str = Field(description="Implications for pregnant women if applicable")
    gender_specific_aspects: str = Field(description="Differences between genders if applicable")
    ethnic_variations: str = Field(description="Variations across ethnic or genetic groups")


class CostAndImpact(BaseModel):
    """Economic and healthcare impact."""
    healthcare_costs: str = Field(description="Typical treatment and management costs")
    productivity_loss: str = Field(description="Economic impact from lost productivity")
    burden_on_healthcare_system: str = Field(description="Healthcare resource utilization")
    insurance_considerations: str = Field(description="Insurance coverage and costs")


class SeeAlso(BaseModel):
    """Cross-references to related medical topics."""
    related_topics: str = Field(description="Related medical topics worth exploring, comma-separated")
    connection_types: str = Field(description="Types of connections (similar condition, related treatment, complication, risk factor, prevention, differential diagnosis, etc.), comma-separated")
    reason: str = Field(description="Brief explanation of how these topics relate to the main topic")


class TopicMetadata(BaseModel):
    """Metadata and information structure."""
    last_updated: str = Field(description="When this information was last reviewed")
    information_sources: str = Field(description="Primary sources of information, comma-separated")
    confidence_level: str = Field(description="Confidence in provided information (high, medium, low)")
    complexity_level: str = Field(description="Complexity of topic (basic, intermediate, advanced)")


class MedicalTopic(BaseModel):
    """
    Comprehensive medical topic information.
    """
    # Basic identification
    overview: TopicOverview

    # Understanding the topic
    definition: Definition
    epidemiology: Epidemiology

    # Causes and mechanisms
    etiology: Etiology
    pathophysiology: Pathophysiology

    # Clinical aspects
    clinical_presentation: ClinicalPresentation
    diagnosis: Diagnosis
    complications: Complications

    # Management and outcomes
    treatment: Treatment
    prognosis: Prognosis
    prevention: Prevention

    # Evidence and research
    research_and_evidence: ResearchAndEvidence

    # Human impact
    psychosocial_impact: PsychosocialImpact
    special_populations: SpecialPopulations
    cost_and_impact: CostAndImpact

    # Patient communication
    education: TopicEducation
    faq: Optional[PatientFAQ] = Field(default=None, description="Patient-friendly FAQ for this topic")

    # Cross-references
    see_also: SeeAlso

    # Metadata
    metadata: TopicMetadata

# ============================================================================ 
# MEDICAL TOPIC GENERATOR CLASS
# ============================================================================ 

class MedicalTopicGenerator:
    """Generate comprehensive information for medical topics."""

    def __init__(self, config: Optional[Config] = None):
        """Initialize the generator."""
        self.config = config or Config()
        # Load model name from ModuleConfig

        try:

            module_config = get_module_config("medical_topic")

            model_name = module_config.model_name

        except ValueError:

            # Fallback to default if not registered yet

            model_name = "gemini-1.5-flash"

        

        self.client = MedKitClient(model_name=model_name)
        self.topic_name: Optional[str] = None
        self.output_path: Optional[Path] = None

        # Apply verbosity level to logger
        verbosity_levels = {0: "CRITICAL", 1: "ERROR", 2: "WARNING", 3: "INFO", 4: "DEBUG"}
        logger.setLevel(verbosity_levels.get(self.config.verbosity, "WARNING"))
        logging.getLogger("medkit").setLevel(verbosity_levels.get(self.config.verbosity, "WARNING"))

    def generate(self, topic_name: str, output_path: Optional[Path] = None) -> MedicalTopic:
        """
        Generate and save comprehensive medical topic information.

        Args:
            topic_name: Name of the medical topic.
            output_path: Optional path to save the JSON output.

        Returns:
            The generated MedicalTopic object.
        
        Raises:
            ValueError: If topic_name is empty.
        """
        if not topic_name or not topic_name.strip():
            raise ValueError("Topic name cannot be empty")

        self.topic_name = topic_name

        if output_path is None:
            output_path = self.config.output_dir / f"{topic_name.lower().replace(' ', '_')}_topic.json"
        
        self.output_path = output_path

        logger.info(f"Starting medical topic information generation for: {topic_name}")

        topic_info = self._generate_info()
        
        self._embed_faq(topic_info)

        self.save(topic_info, self.output_path)
        self.print_summary(topic_info)
        
        return topic_info

    def _generate_info(self) -> MedicalTopic:
        """Generates the topic information."""
        prompt = f"""Generate comprehensive medical information for the topic: {self.topic_name}

Include:
1. Definition and overview
2. Epidemiology (prevalence, incidence, demographics)
3. Pathophysiology and mechanisms
4. Risk factors and etiology
5. Clinical presentation and symptoms
6. Diagnostic criteria and tests
7. Differential diagnosis
8. Treatment options
9. Prognosis and complications
10. Prevention strategies
11. Cross-references to related topics (see_also) - include similar conditions, related treatments, complications that can become independent conditions, conditions that may co-occur, and preventive topics

For see_also cross-references, identify:
- Related medical topics that help readers understand the full context
- Types of connections (similar condition, related treatment, complication, risk factor, prevention, differential diagnosis, co-occurrence, etc.)
- Brief explanation of why each topic is relevant

Provide accurate, evidence-based medical information."""

        result = self.client.generate_text(
            prompt,
            schema=MedicalTopic
        )
        return result

    def _embed_faq(self, topic_info: MedicalTopic) -> None:
        """Generates and embeds a patient-friendly FAQ."""
        logger.info(f"Generating FAQs for: {self.topic_name}")
        try:
            faq_generator = FAQGenerator()
            faq = faq_generator.generate_patient_faq(self.topic_name)
            topic_info.faq = faq
            logger.info(f"✓ FAQ generated and embedded: {len(faq.faqs)} questions")
        except Exception as e:
            logger.warning(f"Warning: FAQ generation failed: {e}")
            topic_info.faq = None

    def save(self, topic_info: MedicalTopic, output_path: Path) -> Path:
        """
        Save the generated topic information to a JSON file.
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(topic_info.model_dump(), f, indent=2)
        
        logger.info(f"✓ Topic information with FAQ saved to {output_path}")
        return output_path

    def print_summary(self, topic_info: MedicalTopic) -> None:
        """
        Print a summary of the generated topic information.
        """
        if not self.config.verbose:
            return

        print("\n" + "="*70)
        print(f"MEDICAL TOPIC SUMMARY: {topic_info.overview.topic_name}")
        print("="*70)
        print(f"  - Category: {topic_info.overview.topic_category}")
        print(f"  - Specialties: {topic_info.overview.medical_specialties}")

        if topic_info.faq:
            print("\n📋 FAQ Summary:")
            print(f"  - Questions: {len(topic_info.faq.faqs)}")
            print(f"  - When to Seek Care: {len(topic_info.faq.when_to_seek_care)} criteria")
            print(f"  - Misconceptions: {len(topic_info.faq.misconceptions)} addressed")

        print(f"\n✓ Generation complete. Saved to {self.output_path}")

def get_topic_info(topic_name: str, output_path: Optional[Path] = None, verbose: bool = False) -> MedicalTopic:
    """
    High-level function to generate and optionally save topic information.
    """
    config = Config(verbose=verbose)
    generator = MedicalTopicGenerator(config=config)
    return generator.generate(topic_name, output_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate comprehensive information for a medical topic.")
    parser.add_argument("-i", "--topic", type=str, required=True, help="The name of the medical topic to generate information for.")
    parser.add_argument("-o", "--output", type=str, help="Optional: The path to save the output JSON file.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show verbose console output.")

    args = parser.parse_args()
    print("Starting ...")
    get_topic_info( args.topic, args.output, args.verbose)
    print(f"Success: output stored in outputs/{args.output}")



    def close(self):
        """Close LMDB storage and release resources."""
        if self.storage:
            try:
                self.storage.close()
                logger.info("LMDB storage closed successfully.")
            except Exception as e:
                logger.error(f"Error closing LMDB storage: {e}")

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
