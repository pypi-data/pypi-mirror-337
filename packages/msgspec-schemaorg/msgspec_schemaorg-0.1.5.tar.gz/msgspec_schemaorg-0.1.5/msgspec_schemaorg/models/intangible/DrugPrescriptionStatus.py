from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.MedicalEnumeration import MedicalEnumeration
from typing import Optional, Union, Dict, List, Any


class DrugPrescriptionStatus(MedicalEnumeration):
    """Indicates whether this drug is available by prescription or over-the-counter."""
    type: str = field(default_factory=lambda: "DrugPrescriptionStatus", name="@type")