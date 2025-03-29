from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.MedicalEnumeration import MedicalEnumeration
from typing import Optional, Union, Dict, List, Any


class MedicalAudienceType(MedicalEnumeration):
    """Target audiences types for medical web pages. Enumerated type."""
    type: str = field(default_factory=lambda: "MedicalAudienceType", name="@type")