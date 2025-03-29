from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.thing.MedicalProcedure import MedicalProcedure
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.thing.DoseSchedule import DoseSchedule
    from msgspec_schemaorg.models.thing.Drug import Drug
    from msgspec_schemaorg.models.thing.MedicalEntity import MedicalEntity
from typing import Optional, Union, Dict, List, Any


class TherapeuticProcedure(MedicalProcedure):
    """A medical procedure intended primarily for therapeutic purposes, aimed at improving a health condition."""
    type: str = field(default_factory=lambda: "TherapeuticProcedure", name="@type")
    adverseOutcome: 'MedicalEntity' | None = None
    drug: 'Drug' | None = None
    doseSchedule: 'DoseSchedule' | None = None