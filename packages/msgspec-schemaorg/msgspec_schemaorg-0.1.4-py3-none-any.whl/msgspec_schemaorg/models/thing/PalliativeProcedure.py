from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.thing.MedicalTherapy import MedicalTherapy
from typing import Optional, Union, Dict, List, Any


class PalliativeProcedure(MedicalTherapy):
    """A medical procedure intended primarily for palliative purposes, aimed at relieving the symptoms of an underlying health condition."""
    type: str = field(default_factory=lambda: "PalliativeProcedure", name="@type")