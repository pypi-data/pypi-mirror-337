from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.MedicalEnumeration import MedicalEnumeration
from typing import Optional, Union, Dict, List, Any


class MedicineSystem(MedicalEnumeration):
    """Systems of medical practice."""
    type: str = field(default_factory=lambda: "MedicineSystem", name="@type")