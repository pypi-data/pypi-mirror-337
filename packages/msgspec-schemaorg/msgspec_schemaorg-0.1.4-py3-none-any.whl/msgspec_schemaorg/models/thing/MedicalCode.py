from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.thing.MedicalIntangible import MedicalIntangible
from typing import Optional, Union, Dict, List, Any


class MedicalCode(MedicalIntangible):
    """A code for a medical entity."""
    type: str = field(default_factory=lambda: "MedicalCode", name="@type")
    codeValue: str | None = None
    codingSystem: str | None = None