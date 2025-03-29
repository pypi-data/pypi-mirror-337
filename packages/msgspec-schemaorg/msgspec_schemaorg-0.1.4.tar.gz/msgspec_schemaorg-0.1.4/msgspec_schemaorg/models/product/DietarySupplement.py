from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.product.Product import Product
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.MedicalEnumeration import MedicalEnumeration
    from msgspec_schemaorg.models.thing.DrugLegalStatus import DrugLegalStatus
    from msgspec_schemaorg.models.thing.MaximumDoseSchedule import MaximumDoseSchedule
    from msgspec_schemaorg.models.thing.RecommendedDoseSchedule import RecommendedDoseSchedule
from typing import Optional, Union, Dict, List, Any


class DietarySupplement(Product):
    """A product taken by mouth that contains a dietary ingredient intended to supplement the diet. Dietary ingredients may include vitamins, minerals, herbs or other botanicals, amino acids, and substances such as enzymes, organ tissues, glandulars and metabolites."""
    type: str = field(default_factory=lambda: "DietarySupplement", name="@type")
    legalStatus: str | 'DrugLegalStatus' | 'MedicalEnumeration' | None = None
    recommendedIntake: 'RecommendedDoseSchedule' | None = None
    nonProprietaryName: str | None = None
    isProprietary: bool | None = None
    mechanismOfAction: str | None = None
    activeIngredient: str | None = None
    targetPopulation: str | None = None
    proprietaryName: str | None = None
    maximumIntake: 'MaximumDoseSchedule' | None = None
    safetyConsideration: str | None = None