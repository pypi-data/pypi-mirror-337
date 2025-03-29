from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.MedicalEnumeration import MedicalEnumeration
from typing import Optional, Union, Dict, List, Any


class MedicalStudyStatus(MedicalEnumeration):
    """The status of a medical study. Enumerated type."""
    type: str = field(default_factory=lambda: "MedicalStudyStatus", name="@type")