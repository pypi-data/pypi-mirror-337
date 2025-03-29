from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.thing.MedicalProcedure import MedicalProcedure
from typing import Optional, Union, Dict, List, Any


class PhysicalExam(MedicalProcedure):
    """A type of physical examination of a patient performed by a physician. """
    type: str = field(default_factory=lambda: "PhysicalExam", name="@type")