from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.thing.Thing import Thing
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.Grant import Grant
    from msgspec_schemaorg.models.intangible.MedicalEnumeration import MedicalEnumeration
    from msgspec_schemaorg.models.intangible.MedicalSpecialty import MedicalSpecialty
    from msgspec_schemaorg.models.intangible.MedicineSystem import MedicineSystem
    from msgspec_schemaorg.models.organization.Organization import Organization
    from msgspec_schemaorg.models.thing.DrugLegalStatus import DrugLegalStatus
    from msgspec_schemaorg.models.thing.MedicalCode import MedicalCode
    from msgspec_schemaorg.models.thing.MedicalGuideline import MedicalGuideline
    from msgspec_schemaorg.models.thing.MedicalStudy import MedicalStudy
from typing import Optional, Union, Dict, List, Any


class MedicalEntity(Thing):
    """The most generic type of entity related to health and the practice of medicine."""
    type: str = field(default_factory=lambda: "MedicalEntity", name="@type")
    legalStatus: str | 'DrugLegalStatus' | 'MedicalEnumeration' | None = None
    relevantSpecialty: 'MedicalSpecialty' | None = None
    funding: 'Grant' | None = None
    recognizingAuthority: 'Organization' | None = None
    medicineSystem: 'MedicineSystem' | None = None
    guideline: 'MedicalGuideline' | None = None
    study: 'MedicalStudy' | None = None
    code: 'MedicalCode' | None = None