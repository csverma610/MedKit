"""
Proper unit tests for drug-drug interaction module.

Tests cover:
- Drug interaction model validation
- Interaction severity levels
- Clinical effect descriptions
- Mechanism of interaction
- Management recommendations
- Data serialization
"""

import unittest
from pydantic import ValidationError

from medkit.drug.drug_drug_interaction import (
    InteractionMechanism,
    ClinicalEffect,
    ManagementRecommendation,
    DrugDrugInteractionResult
)


# ==================== Interaction Mechanism Tests ====================

class TestInteractionMechanism(unittest.TestCase):
    """Test InteractionMechanism data model."""

    def test_mechanism_creation(self):
        """Test creating interaction mechanism."""
        im = InteractionMechanism(
            type="Pharmacodynamic",
            description="Both drugs inhibit platelet aggregation"
        )
        self.assertEqual(im.type, "Pharmacodynamic")
        self.assertIn("platelet", im.description.lower())

    def test_mechanism_pharmacokinetic(self):
        """Test pharmacokinetic mechanism."""
        im = InteractionMechanism(
            type="Pharmacokinetic",
            description="CYP3A4 inhibitor increases levels of second drug"
        )
        self.assertIn("CYP", im.description)

    def test_mechanism_types(self):
        """Test different mechanism types."""
        mechanisms = [
            InteractionMechanism(type="Pharmacokinetic", description="desc1"),
            InteractionMechanism(type="Pharmacodynamic", description="desc2"),
            InteractionMechanism(type="Physicochemical", description="desc3")
        ]
        self.assertEqual(len(mechanisms), 3)
        self.assertEqual(mechanisms[0].type, "Pharmacokinetic")


# ==================== Clinical Effect Tests ====================

class TestClinicalEffect(unittest.TestCase):
    """Test ClinicalEffect data model."""

    def test_clinical_effect_creation(self):
        """Test creating clinical effect."""
        ce = ClinicalEffect(
            effect="Increased bleeding risk",
            symptoms=["Easy bruising", "Prolonged bleeding"],
            manifestation="Can occur within hours to days"
        )
        self.assertEqual(ce.effect, "Increased bleeding risk")
        self.assertIn("bruising", ce.symptoms[0])

    def test_clinical_effect_severity_levels(self):
        """Test effects of different severity."""
        minor = ClinicalEffect(
            effect="Mild headache",
            symptoms=["Slight discomfort"],
            manifestation="Rare"
        )
        severe = ClinicalEffect(
            effect="Severe hypoglycemia",
            symptoms=["Loss of consciousness", "Seizures"],
            manifestation="Can occur suddenly"
        )
        self.assertEqual(len(minor.symptoms), 1)
        self.assertEqual(len(severe.symptoms), 2)

    def test_clinical_effect_empty_symptoms(self):
        """Test clinical effect with minimal symptoms."""
        ce = ClinicalEffect(
            effect="No apparent effect",
            symptoms=[],
            manifestation="Not observed"
        )
        self.assertEqual(len(ce.symptoms), 0)


# ==================== Management Recommendation Tests ====================

class TestManagementRecommendation(unittest.TestCase):
    """Test ManagementRecommendation data model."""

    def test_management_creation(self):
        """Test creating management recommendation."""
        mr = ManagementRecommendation(
            action="Avoid combination",
            reasoning="Risk outweighs benefits",
            monitoring="Not applicable"
        )
        self.assertEqual(mr.action, "Avoid combination")
        self.assertIn("outweighs", mr.reasoning)

    def test_management_recommendations_types(self):
        """Test different types of recommendations."""
        recommendations = [
            ManagementRecommendation(
                action="Use alternative medication",
                reasoning="Safer option available",
                monitoring="Not required"
            ),
            ManagementRecommendation(
                action="Adjust dosage",
                reasoning="Reduced drug levels expected",
                monitoring="Monitor therapeutic levels"
            ),
            ManagementRecommendation(
                action="Monitor closely",
                reasoning="Interaction manageable with vigilance",
                monitoring="Check for adverse effects"
            ),
            ManagementRecommendation(
                action="No action needed",
                reasoning="Minimal or no interaction",
                monitoring="Routine monitoring only"
            )
        ]
        self.assertEqual(len(recommendations), 4)
        self.assertEqual(recommendations[2].action, "Monitor closely")

    def test_management_with_details(self):
        """Test recommendation with detailed monitoring."""
        mr = ManagementRecommendation(
            action="Reduce second drug dose by 50%",
            reasoning="First drug increases second drug levels 2-3 fold",
            monitoring="Check INR levels weekly for 2 weeks, then monthly"
        )
        self.assertIn("50%", mr.action)
        self.assertIn("weekly", mr.monitoring)


# ==================== Drug-Drug Interaction Result Tests ====================

class TestDrugDrugInteractionResult(unittest.TestCase):
    """Test complete DrugDrugInteractionResult model."""

    def setUp(self):
        """Set up test data."""
        self.interaction_data = {
            "drug_a": "Warfarin",
            "drug_b": "Aspirin",
            "severity": "High",
            "mechanism": InteractionMechanism(
                type="Pharmacodynamic",
                description="Both drugs inhibit hemostasis via different mechanisms"
            ),
            "clinical_effect": ClinicalEffect(
                effect="Increased bleeding risk",
                symptoms=["Easy bruising", "Prolonged bleeding", "Blood in stool"],
                manifestation="Can occur within days"
            ),
            "management": ManagementRecommendation(
                action="Avoid combination; use alternative antipyretic",
                reasoning="Risk of serious bleeding outweighs benefits",
                monitoring="If combination necessary, monitor INR and bleeding signs"
            )
        }

    def test_interaction_result_creation(self):
        """Test creating drug interaction result."""
        result = DrugDrugInteractionResult(**self.interaction_data)
        self.assertEqual(result.drug_a, "Warfarin")
        self.assertEqual(result.drug_b, "Aspirin")
        self.assertEqual(result.severity, "High")

    def test_interaction_severity_levels(self):
        """Test different severity levels."""
        severities = ["Minor", "Moderate", "High"]
        for severity in severities:
            data = self.interaction_data.copy()
            data["severity"] = severity
            result = DrugDrugInteractionResult(**data)
            self.assertEqual(result.severity, severity)

    def test_interaction_serialization(self):
        """Test interaction result serialization."""
        result = DrugDrugInteractionResult(**self.interaction_data)
        data_dict = result.dict()
        self.assertIn("drug_a", data_dict)
        self.assertIn("severity", data_dict)
        self.assertEqual(data_dict["drug_a"], "Warfarin")

    def test_interaction_json_serialization(self):
        """Test JSON serialization."""
        result = DrugDrugInteractionResult(**self.interaction_data)
        json_str = result.json()
        self.assertIn("Warfarin", json_str)
        self.assertIn("High", json_str)
        self.assertIn("Aspirin", json_str)

    def test_interaction_missing_required_field(self):
        """Test with missing required field."""
        incomplete = self.interaction_data.copy()
        del incomplete["severity"]
        with self.assertRaises(ValidationError):
            DrugDrugInteractionResult(**incomplete)


# ==================== Common Drug Interactions Tests ====================

class TestCommonDrugInteractions(unittest.TestCase):
    """Test realistic drug interactions."""

    def test_warfarin_aspirin_interaction(self):
        """Test warfarin-aspirin interaction."""
        interaction = DrugDrugInteractionResult(
            drug_a="Warfarin",
            drug_b="Aspirin",
            severity="High",
            mechanism=InteractionMechanism(
                type="Pharmacodynamic",
                description="Both inhibit hemostasis via different mechanisms"
            ),
            clinical_effect=ClinicalEffect(
                effect="Increased bleeding risk",
                symptoms=["Easy bruising", "GI bleeding", "Hematuria"],
                manifestation="Within days to weeks"
            ),
            management=ManagementRecommendation(
                action="Avoid combination",
                reasoning="High risk of serious bleeding",
                monitoring="Use alternative analgesic (acetaminophen)"
            )
        )

        self.assertEqual(interaction.severity, "High")
        self.assertIn("Aspirin", interaction.drug_b)

    def test_metformin_contrast_interaction(self):
        """Test metformin-contrast dye interaction."""
        interaction = DrugDrugInteractionResult(
            drug_a="Metformin",
            drug_b="Iodinated contrast",
            severity="High",
            mechanism=InteractionMechanism(
                type="Pharmacokinetic",
                description="Contrast dye impairs renal function, decreasing metformin clearance"
            ),
            clinical_effect=ClinicalEffect(
                effect="Lactic acidosis",
                symptoms=["Fatigue", "Muscle pain", "Difficulty breathing"],
                manifestation="24-48 hours after contrast"
            ),
            management=ManagementRecommendation(
                action="Hold metformin before and after contrast",
                reasoning="Prevent accumulation and lactic acidosis risk",
                monitoring="Resume only if renal function stable"
            )
        )

        self.assertEqual(interaction.severity, "High")
        self.assertIn("metformin", interaction.drug_a.lower())

    def test_simvastatin_clarithromycin_interaction(self):
        """Test simvastatin-clarithromycin interaction."""
        interaction = DrugDrugInteractionResult(
            drug_a="Simvastatin",
            drug_b="Clarithromycin",
            severity="High",
            mechanism=InteractionMechanism(
                type="Pharmacokinetic",
                description="Clarithromycin inhibits CYP3A4, increasing simvastatin levels 16-fold"
            ),
            clinical_effect=ClinicalEffect(
                effect="Increased myopathy/rhabdomyolysis risk",
                symptoms=["Muscle pain", "Dark urine", "Weakness"],
                manifestation="Within days to weeks"
            ),
            management=ManagementRecommendation(
                action="Avoid combination or suspend simvastatin",
                reasoning="High risk of statin-induced muscle injury",
                monitoring="Use alternative antibiotic (azithromycin)"
            )
        )

        self.assertEqual(interaction.severity, "High")

    def test_lisinopril_potassium_interaction(self):
        """Test ACE inhibitor-potassium supplement interaction."""
        interaction = DrugDrugInteractionResult(
            drug_a="Lisinopril",
            drug_b="Potassium supplement",
            severity="Moderate",
            mechanism=InteractionMechanism(
                type="Pharmacodynamic",
                description="ACE inhibitor reduces aldosterone, both increase potassium retention"
            ),
            clinical_effect=ClinicalEffect(
                effect="Hyperkalemia",
                symptoms=["Weakness", "Palpitations", "Cardiac arrhythmias"],
                manifestation="Within 1-2 weeks"
            ),
            management=ManagementRecommendation(
                action="Monitor potassium levels",
                reasoning="Combined effect increases hyperkalemia risk",
                monitoring="Check K+ at baseline, 1 week, 4 weeks; do EKG if K+ >6.0"
            )
        )

        self.assertEqual(interaction.severity, "Moderate")
        self.assertIn("baseline", interaction.management.monitoring.lower())

    def test_omeprazole_clopidogrel_interaction(self):
        """Test proton pump inhibitor-clopidogrel interaction."""
        interaction = DrugDrugInteractionResult(
            drug_a="Clopidogrel",
            drug_b="Omeprazole",
            severity="Moderate",
            mechanism=InteractionMechanism(
                type="Pharmacokinetic",
                description="Omeprazole inhibits CYP2C19, reducing clopidogrel activation"
            ),
            clinical_effect=ClinicalEffect(
                effect="Reduced antiplatelet effect",
                symptoms=["Recurrent stent thrombosis", "Myocardial infarction"],
                manifestation="Ongoing throughout combination therapy"
            ),
            management=ManagementRecommendation(
                action="Use pantoprazole or H2 blocker instead",
                reasoning="Alternative PPIs have less CYP2C19 inhibition",
                monitoring="Monitor for thrombotic events"
            )
        )

        self.assertIn("pantoprazole", interaction.management.action.lower())

    def test_minor_interaction(self):
        """Test a minor interaction."""
        interaction = DrugDrugInteractionResult(
            drug_a="Acetaminophen",
            drug_b="Ibuprofen",
            severity="Minor",
            mechanism=InteractionMechanism(
                type="Pharmacodynamic",
                description="Both are NSAIDs/analgesics"
            ),
            clinical_effect=ClinicalEffect(
                effect="Potential for additive GI irritation",
                symptoms=["Mild stomach upset"],
                manifestation="Rare"
            ),
            management=ManagementRecommendation(
                action="Use one agent at a time",
                reasoning="No additional benefit from combination",
                monitoring="Routine"
            )
        )

        self.assertEqual(interaction.severity, "Minor")


# ==================== Integration Tests ====================

class TestDrugDrugInteractionIntegration(unittest.TestCase):
    """Integration tests for drug interaction system."""

    def test_multiple_interactions_patient(self):
        """Test scenario with patient on multiple medications."""
        patient_drugs = ["Warfarin", "Aspirin", "Ibuprofen", "Metformin"]

        # Test critical interactions
        warfarin_aspirin = DrugDrugInteractionResult(
            drug_a="Warfarin",
            drug_b="Aspirin",
            severity="High",
            mechanism=InteractionMechanism(
                type="Pharmacodynamic",
                description="Additive anticoagulation"
            ),
            clinical_effect=ClinicalEffect(
                effect="Bleeding",
                symptoms=["Bleeding"],
                manifestation="High risk"
            ),
            management=ManagementRecommendation(
                action="Avoid",
                reasoning="High risk",
                monitoring="None"
            )
        )

        warfarin_ibuprofen = DrugDrugInteractionResult(
            drug_a="Warfarin",
            drug_b="Ibuprofen",
            severity="High",
            mechanism=InteractionMechanism(
                type="Pharmacodynamic",
                description="Both affect hemostasis"
            ),
            clinical_effect=ClinicalEffect(
                effect="Bleeding",
                symptoms=["Bleeding"],
                manifestation="High risk"
            ),
            management=ManagementRecommendation(
                action="Avoid",
                reasoning="High risk",
                monitoring="None"
            )
        )

        interactions = [warfarin_aspirin, warfarin_ibuprofen]
        high_severity = [i for i in interactions if i.severity == "High"]
        self.assertEqual(len(high_severity), 2)

    def test_interaction_verification_workflow(self):
        """Test workflow for checking interactions."""
        interaction = DrugDrugInteractionResult(
            drug_a="Drug A",
            drug_b="Drug B",
            severity="Moderate",
            mechanism=InteractionMechanism(
                type="Pharmacokinetic",
                description="Inhibition"
            ),
            clinical_effect=ClinicalEffect(
                effect="Increased levels",
                symptoms=["Toxicity"],
                manifestation="2-3 days"
            ),
            management=ManagementRecommendation(
                action="Monitor",
                reasoning="Important but manageable",
                monitoring="Check drug levels"
            )
        )

        # Verify workflow: identify → assess severity → recommend action
        self.assertIsNotNone(interaction.drug_a)
        self.assertIsNotNone(interaction.drug_b)
        self.assertEqual(interaction.severity, "Moderate")
        self.assertIn("Monitor", interaction.management.action)


if __name__ == "__main__":
    unittest.main(verbosity=2)
