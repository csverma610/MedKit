"""
Proper unit tests for disease_info module.

Tests cover:
- Data model validation (Pydantic models)
- Model structure and required fields
- Optional fields handling
- Data serialization/deserialization
- Invalid data rejection
"""

import unittest
from typing import Optional, List
from pydantic import ValidationError

from medkit.medical.disease_info import (
    RiskFactors,
    DiagnosticCriteria,
    DiseaseIdentity,
    DiseaseBackground,
    DiseaseEpidemiology,
    DiseaseClinicalPresentation,
    DiseaseDiagnosis,
    DiseaseManagement,
    DiseaseResearch,
    DiseaseSpecialPopulations,
    DiseaseLivingWith,
    DiseaseInfo
)


# ==================== Risk Factors Tests ====================

class TestRiskFactors(unittest.TestCase):
    """Test RiskFactors data model."""

    def test_risk_factors_creation(self):
        """Test creating risk factors with valid data."""
        rf = RiskFactors(
            modifiable=["smoking", "high cholesterol"],
            non_modifiable=["age", "family history"]
        )
        self.assertEqual(rf.modifiable, ["smoking", "high cholesterol"])
        self.assertEqual(rf.non_modifiable, ["age", "family history"])

    def test_risk_factors_empty_lists(self):
        """Test risk factors with empty lists."""
        rf = RiskFactors(modifiable=[], non_modifiable=[])
        self.assertEqual(rf.modifiable, [])
        self.assertEqual(rf.non_modifiable, [])

    def test_risk_factors_missing_fields(self):
        """Test risk factors with missing required fields."""
        with self.assertRaises(ValidationError):
            RiskFactors(modifiable=["smoking"])


# ==================== Diagnostic Criteria Tests ====================

class TestDiagnosticCriteria(unittest.TestCase):
    """Test DiagnosticCriteria data model."""

    def test_diagnostic_criteria_creation(self):
        """Test creating diagnostic criteria."""
        dc = DiagnosticCriteria(
            criteria=["BP > 140/90", "On antihypertensive medication"],
            confirmation_tests=["blood pressure reading", "home BP monitoring"],
            differential_diagnoses=["secondary hypertension", "white coat effect"]
        )
        self.assertEqual(len(dc.criteria), 2)
        self.assertEqual(len(dc.confirmation_tests), 2)
        self.assertIn("secondary hypertension", dc.differential_diagnoses)

    def test_diagnostic_criteria_empty_arrays(self):
        """Test diagnostic criteria with empty arrays."""
        dc = DiagnosticCriteria(
            criteria=[],
            confirmation_tests=[],
            differential_diagnoses=[]
        )
        self.assertEqual(len(dc.criteria), 0)
        self.assertEqual(len(dc.confirmation_tests), 0)


# ==================== Disease Identity Tests ====================

class TestDiseaseIdentity(unittest.TestCase):
    """Test DiseaseIdentity data model."""

    def test_disease_identity_creation(self):
        """Test creating disease identity."""
        di = DiseaseIdentity(
            disease_name="Hypertension",
            alternative_names=["High blood pressure", "HTN"],
            icd10_codes=["I10"],
            disease_category="Cardiovascular"
        )
        self.assertEqual(di.disease_name, "Hypertension")
        self.assertIn("HTN", di.alternative_names)
        self.assertEqual(di.icd10_codes[0], "I10")

    def test_disease_identity_without_alternatives(self):
        """Test disease identity without alternative names."""
        di = DiseaseIdentity(
            disease_name="Uncommon Disease",
            alternative_names=[],
            icd10_codes=["Z00.00"],
            disease_category="Other"
        )
        self.assertEqual(len(di.alternative_names), 0)

    def test_disease_identity_required_fields(self):
        """Test disease identity with missing required field."""
        with self.assertRaises(ValidationError):
            DiseaseIdentity(
                disease_name="Test",
                icd10_codes=["I10"]
            )


# ==================== Disease Background Tests ====================

class TestDiseaseBackground(unittest.TestCase):
    """Test DiseaseBackground data model."""

    def test_disease_background_creation(self):
        """Test creating disease background."""
        db = DiseaseBackground(
            definition="Systemic arterial blood pressure > 140/90 mmHg",
            pathophysiology="Increased peripheral vascular resistance",
            etiology="Multifactorial: genetic and environmental factors"
        )
        self.assertIn("140/90", db.definition)
        self.assertIn("resistance", db.pathophysiology)

    def test_disease_background_long_text(self):
        """Test background with long descriptive text."""
        long_text = "A" * 500
        db = DiseaseBackground(
            definition=long_text,
            pathophysiology="Normal",
            etiology="Normal"
        )
        self.assertEqual(len(db.definition), 500)


# ==================== Disease Epidemiology Tests ====================

class TestDiseaseEpidemiology(unittest.TestCase):
    """Test DiseaseEpidemiology data model."""

    def test_epidemiology_creation(self):
        """Test creating epidemiology data."""
        de = DiseaseEpidemiology(
            prevalence="30% of adults",
            incidence="3 million new cases per year",
            mortality_rate="5-10%",
            affected_populations=["Adults", "African Americans"],
            geographic_distribution="Worldwide"
        )
        self.assertIn("30%", de.prevalence)
        self.assertIn("African Americans", de.affected_populations)

    def test_epidemiology_regional_variation(self):
        """Test epidemiology with regional data."""
        de = DiseaseEpidemiology(
            prevalence="5-15% depending on region",
            incidence="Variable",
            mortality_rate="2-8%",
            affected_populations=["All ages"],
            geographic_distribution="Higher in developed countries"
        )
        self.assertIn("developed countries", de.geographic_distribution)


# ==================== Clinical Presentation Tests ====================

class TestDiseaseClinicalPresentation(unittest.TestCase):
    """Test DiseaseClinicalPresentation data model."""

    def test_clinical_presentation_creation(self):
        """Test creating clinical presentation."""
        dcp = DiseaseClinicalPresentation(
            symptoms=["Headache", "Chest discomfort"],
            signs=["Elevated BP", "Left ventricular hypertrophy"],
            severity_spectrum="Asymptomatic to severe"
        )
        self.assertEqual(len(dcp.symptoms), 2)
        self.assertIn("Elevated BP", dcp.signs)

    def test_clinical_presentation_empty_symptoms(self):
        """Test presentation with asymptomatic disease."""
        dcp = DiseaseClinicalPresentation(
            symptoms=[],
            signs=["Finding 1"],
            severity_spectrum="Often asymptomatic initially"
        )
        self.assertEqual(len(dcp.symptoms), 0)


# ==================== Diagnosis Tests ====================

class TestDiseaseDiagnosis(unittest.TestCase):
    """Test DiseaseDiagnosis data model."""

    def test_diagnosis_creation(self):
        """Test creating diagnosis information."""
        dd = DiseaseDiagnosis(
            diagnostic_criteria=DiagnosticCriteria(
                criteria=["BP > 140/90 on 2+ occasions"],
                confirmation_tests=["Home BP monitoring"],
                differential_diagnoses=["White coat effect"]
            )
        )
        self.assertIsNotNone(dd.diagnostic_criteria)
        self.assertEqual(len(dd.diagnostic_criteria.criteria), 1)


# ==================== Management Tests ====================

class TestDiseaseManagement(unittest.TestCase):
    """Test DiseaseManagement data model."""

    def test_management_creation(self):
        """Test creating management information."""
        dm = DiseaseManagement(
            treatment_options=["Lifestyle modification", "ACE inhibitors"],
            medication_classes=["ACE inhibitors", "Beta blockers"],
            lifestyle_modifications=["Reduce sodium intake", "Exercise"],
            monitoring_parameters=["Blood pressure", "Kidney function"]
        )
        self.assertEqual(len(dm.treatment_options), 2)
        self.assertIn("Beta blockers", dm.medication_classes)

    def test_management_conservative_approach(self):
        """Test management with conservative treatment."""
        dm = DiseaseManagement(
            treatment_options=["Observation only"],
            medication_classes=[],
            lifestyle_modifications=["Monitoring"],
            monitoring_parameters=["Disease progression"]
        )
        self.assertEqual(len(dm.treatment_options), 1)


# ==================== Research Tests ====================

class TestDiseaseResearch(unittest.TestCase):
    """Test DiseaseResearch data model."""

    def test_research_creation(self):
        """Test creating research information."""
        dr = DiseaseResearch(
            current_research="Gene therapy approaches",
            recent_breakthroughs=["New drug class approved 2023"],
            clinical_trials="5000+ active trials"
        )
        self.assertIn("Gene therapy", dr.current_research)

    def test_research_no_breakthroughs(self):
        """Test research with no recent breakthroughs."""
        dr = DiseaseResearch(
            current_research="Ongoing studies",
            recent_breakthroughs=[],
            clinical_trials="Limited trials"
        )
        self.assertEqual(len(dr.recent_breakthroughs), 0)


# ==================== Special Populations Tests ====================

class TestDiseaseSpecialPopulations(unittest.TestCase):
    """Test DiseaseSpecialPopulations data model."""

    def test_special_populations_creation(self):
        """Test creating special populations data."""
        dsp = DiseaseSpecialPopulations(
            pediatric_considerations="Rare in children",
            geriatric_considerations="Common, often undertreated",
            pregnancy_considerations="Risk of pre-eclampsia",
            gender_differences="Higher in men before age 65"
        )
        self.assertIn("Rare", dsp.pediatric_considerations)
        self.assertIn("undertreated", dsp.geriatric_considerations)

    def test_special_populations_no_differences(self):
        """Test when there are no special considerations."""
        dsp = DiseaseSpecialPopulations(
            pediatric_considerations="No significant differences",
            geriatric_considerations="No significant differences",
            pregnancy_considerations="Generally safe",
            gender_differences="No gender differences"
        )
        self.assertIn("Generally safe", dsp.pregnancy_considerations)


# ==================== Living With Tests ====================

class TestDiseaseLivingWith(unittest.TestCase):
    """Test DiseaseLivingWith data model."""

    def test_living_with_creation(self):
        """Test creating living with information."""
        dlw = DiseaseLivingWith(
            quality_of_life="Usually good with treatment",
            support_resources=["Support groups", "Educational materials"],
            prognosis="Good with adherence",
            complications=["Stroke", "Kidney disease"]
        )
        self.assertIn("Support groups", dlw.support_resources)
        self.assertIn("Stroke", dlw.complications)

    def test_living_with_no_complications(self):
        """Test when disease has minimal complications."""
        dlw = DiseaseLivingWith(
            quality_of_life="Excellent",
            support_resources=[],
            prognosis="Excellent",
            complications=[]
        )
        self.assertEqual(len(dlw.complications), 0)


# ==================== Complete Disease Info Tests ====================

class TestDiseaseInfo(unittest.TestCase):
    """Test complete DiseaseInfo model."""

    def setUp(self):
        """Set up test data."""
        self.disease_data = {
            "identity": DiseaseIdentity(
                disease_name="Hypertension",
                alternative_names=["High blood pressure"],
                icd10_codes=["I10"],
                disease_category="Cardiovascular"
            ),
            "background": DiseaseBackground(
                definition="BP > 140/90",
                pathophysiology="Increased resistance",
                etiology="Multifactorial"
            ),
            "epidemiology": DiseaseEpidemiology(
                prevalence="30%",
                incidence="3M/year",
                mortality_rate="5%",
                affected_populations=["Adults"],
                geographic_distribution="Worldwide"
            ),
            "clinical_presentation": DiseaseClinicalPresentation(
                symptoms=["Headache"],
                signs=["Elevated BP"],
                severity_spectrum="Asymptomatic to severe"
            ),
            "diagnosis": DiseaseDiagnosis(
                diagnostic_criteria=DiagnosticCriteria(
                    criteria=["BP > 140/90"],
                    confirmation_tests=["BP reading"],
                    differential_diagnoses=["White coat effect"]
                )
            ),
            "management": DiseaseManagement(
                treatment_options=["Medication"],
                medication_classes=["ACE inhibitors"],
                lifestyle_modifications=["Reduce sodium"],
                monitoring_parameters=["BP"]
            ),
            "research": DiseaseResearch(
                current_research="Gene therapy",
                recent_breakthroughs=["New drug"],
                clinical_trials="5000 trials"
            ),
            "special_populations": DiseaseSpecialPopulations(
                pediatric_considerations="Rare",
                geriatric_considerations="Common",
                pregnancy_considerations="Risk",
                gender_differences="More in men"
            ),
            "living_with": DiseaseLivingWith(
                quality_of_life="Good",
                support_resources=["Groups"],
                prognosis="Good",
                complications=["Stroke"]
            )
        }

    def test_disease_info_creation(self):
        """Test creating complete disease info."""
        di = DiseaseInfo(**self.disease_data)
        self.assertEqual(di.identity.disease_name, "Hypertension")
        self.assertEqual(di.epidemiology.prevalence, "30%")

    def test_disease_info_serialization(self):
        """Test disease info can be serialized to dict."""
        di = DiseaseInfo(**self.disease_data)
        data_dict = di.dict()
        self.assertIn("identity", data_dict)
        self.assertIn("background", data_dict)
        self.assertEqual(data_dict["identity"]["disease_name"], "Hypertension")

    def test_disease_info_json_serialization(self):
        """Test disease info can be serialized to JSON."""
        di = DiseaseInfo(**self.disease_data)
        json_str = di.json()
        self.assertIn("Hypertension", json_str)
        self.assertIn("Cardiovascular", json_str)

    def test_disease_info_missing_required_field(self):
        """Test disease info with missing required field."""
        incomplete_data = {
            "identity": DiseaseIdentity(
                disease_name="Test",
                alternative_names=[],
                icd10_codes=["Z00"],
                disease_category="Other"
            ),
            "background": DiseaseBackground(
                definition="Test",
                pathophysiology="Test",
                etiology="Test"
            )
        }
        with self.assertRaises(ValidationError):
            DiseaseInfo(**incomplete_data)


# ==================== Integration Tests ====================

class TestDiseaseInfoIntegration(unittest.TestCase):
    """Integration tests for disease information system."""

    def test_hypertension_disease_model(self):
        """Test a realistic hypertension model."""
        hypertension = DiseaseInfo(
            identity=DiseaseIdentity(
                disease_name="Essential Hypertension",
                alternative_names=["Primary hypertension", "High blood pressure"],
                icd10_codes=["I10"],
                disease_category="Cardiovascular"
            ),
            background=DiseaseBackground(
                definition="Systemic arterial blood pressure ≥140/90 mmHg on ≥2 occasions",
                pathophysiology="Increased peripheral vascular resistance with expanded intravascular volume",
                etiology="Multifactorial: 95% have unknown etiology (primary HTN)"
            ),
            epidemiology=DiseaseEpidemiology(
                prevalence="30-45% of adults in developed countries",
                incidence="3-4 million new cases annually in USA",
                mortality_rate="High: contributes to 7.5M deaths annually",
                affected_populations=["Adults over 18", "African Americans", "Older adults"],
                geographic_distribution="Higher in developed nations and urban areas"
            ),
            clinical_presentation=DiseaseClinicalPresentation(
                symptoms=["Often asymptomatic", "Headache", "Dizziness", "Chest discomfort"],
                signs=["Elevated systolic and/or diastolic BP", "Left ventricular hypertrophy"],
                severity_spectrum="Often asymptomatic in early stages to severe with complications"
            ),
            diagnosis=DiseaseDiagnosis(
                diagnostic_criteria=DiagnosticCriteria(
                    criteria=[
                        "SBP ≥140 mmHg OR DBP ≥90 mmHg on 2+ occasions",
                        "Different BP readings at different times"
                    ],
                    confirmation_tests=[
                        "Home blood pressure monitoring",
                        "24-hour ambulatory BP monitoring",
                        "Office BP readings"
                    ],
                    differential_diagnoses=[
                        "White coat hypertension",
                        "Secondary hypertension",
                        "Masked hypertension"
                    ]
                )
            ),
            management=DiseaseManagement(
                treatment_options=[
                    "Lifestyle modification alone",
                    "Pharmacological therapy",
                    "Combined approach"
                ],
                medication_classes=[
                    "ACE inhibitors",
                    "Angiotensin II receptor blockers",
                    "Beta blockers",
                    "Calcium channel blockers",
                    "Diuretics"
                ],
                lifestyle_modifications=[
                    "DASH diet (sodium <2.3g/day)",
                    "Regular aerobic exercise (150 min/week)",
                    "Weight loss if overweight",
                    "Limit alcohol",
                    "Stress reduction"
                ],
                monitoring_parameters=[
                    "Blood pressure at home and office",
                    "Serum creatinine and eGFR",
                    "Urine protein",
                    "Potassium levels",
                    "Lipid panel"
                ]
            ),
            research=DiseaseResearch(
                current_research="Novel antihypertensive agents, gene therapy approaches",
                recent_breakthroughs=[
                    "SGLT2 inhibitors showing benefit in HTN with CKD",
                    "Renal denervation techniques under investigation"
                ],
                clinical_trials="5000+ active trials worldwide"
            ),
            special_populations=DiseaseSpecialPopulations(
                pediatric_considerations="Rare; secondary causes must be ruled out",
                geriatric_considerations="Very common; often undertreated; target BP 130-139/70-79",
                pregnancy_considerations="High risk for pre-eclampsia; specific medication restrictions",
                gender_differences="More common in men until age 65, then more common in women"
            ),
            living_with=DiseaseLivingWith(
                quality_of_life="Generally excellent with treatment adherence",
                support_resources=["American Heart Association", "Patient education programs"],
                prognosis="Excellent with medication adherence and lifestyle changes",
                complications=[
                    "Myocardial infarction",
                    "Stroke",
                    "Chronic kidney disease",
                    "Heart failure",
                    "Aortic dissection"
                ]
            )
        )

        # Verify the model structure
        self.assertEqual(hypertension.identity.disease_name, "Essential Hypertension")
        self.assertIn("I10", hypertension.identity.icd10_codes)
        self.assertGreater(len(hypertension.management.medication_classes), 3)
        self.assertGreater(len(hypertension.living_with.complications), 3)
        self.assertIn("stroke", hypertension.living_with.complications[1].lower())

    def test_disease_model_completeness(self):
        """Test that disease model captures all necessary information."""
        di = DiseaseInfo(
            identity=DiseaseIdentity(
                disease_name="Test",
                alternative_names=[],
                icd10_codes=["Z00"],
                disease_category="Other"
            ),
            background=DiseaseBackground(
                definition="def",
                pathophysiology="path",
                etiology="etio"
            ),
            epidemiology=DiseaseEpidemiology(
                prevalence="prev",
                incidence="inc",
                mortality_rate="mort",
                affected_populations=["pop"],
                geographic_distribution="geo"
            ),
            clinical_presentation=DiseaseClinicalPresentation(
                symptoms=["symp"],
                signs=["sign"],
                severity_spectrum="spec"
            ),
            diagnosis=DiseaseDiagnosis(
                diagnostic_criteria=DiagnosticCriteria(
                    criteria=["crit"],
                    confirmation_tests=["test"],
                    differential_diagnoses=["diff"]
                )
            ),
            management=DiseaseManagement(
                treatment_options=["treat"],
                medication_classes=["med"],
                lifestyle_modifications=["life"],
                monitoring_parameters=["mon"]
            ),
            research=DiseaseResearch(
                current_research="curr",
                recent_breakthroughs=["break"],
                clinical_trials="trials"
            ),
            special_populations=DiseaseSpecialPopulations(
                pediatric_considerations="ped",
                geriatric_considerations="ger",
                pregnancy_considerations="preg",
                gender_differences="gender"
            ),
            living_with=DiseaseLivingWith(
                quality_of_life="qol",
                support_resources=["support"],
                prognosis="prog",
                complications=["comp"]
            )
        )

        # Verify all main sections are present
        self.assertIsNotNone(di.identity)
        self.assertIsNotNone(di.background)
        self.assertIsNotNone(di.epidemiology)
        self.assertIsNotNone(di.clinical_presentation)
        self.assertIsNotNone(di.diagnosis)
        self.assertIsNotNone(di.management)
        self.assertIsNotNone(di.research)
        self.assertIsNotNone(di.special_populations)
        self.assertIsNotNone(di.living_with)


if __name__ == "__main__":
    unittest.main(verbosity=2)
