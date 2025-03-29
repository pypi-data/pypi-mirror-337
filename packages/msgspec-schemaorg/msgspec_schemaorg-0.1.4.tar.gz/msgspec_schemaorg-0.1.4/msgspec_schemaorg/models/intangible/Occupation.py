from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Intangible import Intangible
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.EducationalOccupationalCredential import EducationalOccupationalCredential
    from msgspec_schemaorg.models.intangible.CategoryCode import CategoryCode
    from msgspec_schemaorg.models.intangible.DefinedTerm import DefinedTerm
    from msgspec_schemaorg.models.intangible.MonetaryAmount import MonetaryAmount
    from msgspec_schemaorg.models.intangible.MonetaryAmountDistribution import MonetaryAmountDistribution
    from msgspec_schemaorg.models.intangible.OccupationalExperienceRequirements import OccupationalExperienceRequirements
    from msgspec_schemaorg.models.place.AdministrativeArea import AdministrativeArea
from typing import Optional, Union, Dict, List, Any


class Occupation(Intangible):
    """A profession, may involve prolonged training and/or a formal qualification."""
    type: str = field(default_factory=lambda: "Occupation", name="@type")
    responsibilities: str | None = None
    educationRequirements: str | 'EducationalOccupationalCredential' | None = None
    skills: str | 'DefinedTerm' | None = None
    occupationLocation: 'AdministrativeArea' | None = None
    occupationalCategory: str | 'CategoryCode' | None = None
    qualifications: str | 'EducationalOccupationalCredential' | None = None
    estimatedSalary: int | float | 'MonetaryAmountDistribution' | 'MonetaryAmount' | None = None
    experienceRequirements: str | 'OccupationalExperienceRequirements' | None = None