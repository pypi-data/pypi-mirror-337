from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.MedicalEnumeration import MedicalEnumeration
from typing import Optional, Union, Dict, List, Any


class MedicalEvidenceLevel(MedicalEnumeration):
    """Level of evidence for a medical guideline. Enumerated type."""
    type: str = field(default_factory=lambda: "MedicalEvidenceLevel", name="@type")