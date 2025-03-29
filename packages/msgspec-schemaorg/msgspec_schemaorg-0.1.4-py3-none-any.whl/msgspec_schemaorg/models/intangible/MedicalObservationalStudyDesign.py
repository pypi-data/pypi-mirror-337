from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.MedicalEnumeration import MedicalEnumeration
from typing import Optional, Union, Dict, List, Any


class MedicalObservationalStudyDesign(MedicalEnumeration):
    """Design models for observational medical studies. Enumerated type."""
    type: str = field(default_factory=lambda: "MedicalObservationalStudyDesign", name="@type")