from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.organization.MedicalOrganization import MedicalOrganization
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.CategoryCode import CategoryCode
    from msgspec_schemaorg.models.intangible.MedicalSpecialty import MedicalSpecialty
    from msgspec_schemaorg.models.place.Hospital import Hospital
    from msgspec_schemaorg.models.thing.MedicalProcedure import MedicalProcedure
    from msgspec_schemaorg.models.thing.MedicalTest import MedicalTest
    from msgspec_schemaorg.models.thing.MedicalTherapy import MedicalTherapy
from typing import Optional, Union, Dict, List, Any


class Physician(MedicalOrganization):
    """An individual physician or a physician's office considered as a [[MedicalOrganization]]."""
    type: str = field(default_factory=lambda: "Physician", name="@type")
    availableService: Union[List[Union['MedicalTest', 'MedicalTherapy', 'MedicalProcedure']], Union['MedicalTest', 'MedicalTherapy', 'MedicalProcedure'], None] = None
    hospitalAffiliation: Union[List['Hospital'], 'Hospital', None] = None
    medicalSpecialty: Union[List['MedicalSpecialty'], 'MedicalSpecialty', None] = None
    occupationalCategory: Union[List[Union[str, 'CategoryCode']], Union[str, 'CategoryCode'], None] = None
    usNPI: Union[List[str], str, None] = None