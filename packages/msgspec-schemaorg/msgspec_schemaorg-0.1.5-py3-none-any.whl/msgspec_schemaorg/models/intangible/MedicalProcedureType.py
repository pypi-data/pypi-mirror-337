from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.MedicalEnumeration import MedicalEnumeration
from typing import Optional, Union, Dict, List, Any


class MedicalProcedureType(MedicalEnumeration):
    """An enumeration that describes different types of medical procedures."""
    type: str = field(default_factory=lambda: "MedicalProcedureType", name="@type")