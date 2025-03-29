from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.organization.Organization import Organization
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.MedicalSpecialty import MedicalSpecialty
from typing import Optional, Union, Dict, List, Any


class MedicalOrganization(Organization):
    """A medical organization (physical or not), such as hospital, institution or clinic."""
    type: str = field(default_factory=lambda: "MedicalOrganization", name="@type")
    medicalSpecialty: 'MedicalSpecialty' | None = None
    isAcceptingNewPatients: bool | None = None
    healthPlanNetworkId: str | None = None