from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.thing.AnatomicalStructure import AnatomicalStructure
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.thing.MedicalEntity import MedicalEntity
from typing import Optional, Union, Dict, List, Any


class Joint(AnatomicalStructure):
    """The anatomical location at which two or more bones make contact."""
    type: str = field(default_factory=lambda: "Joint", name="@type")
    functionalClass: str | 'MedicalEntity' | None = None
    structuralClass: str | None = None
    biomechnicalClass: str | None = None