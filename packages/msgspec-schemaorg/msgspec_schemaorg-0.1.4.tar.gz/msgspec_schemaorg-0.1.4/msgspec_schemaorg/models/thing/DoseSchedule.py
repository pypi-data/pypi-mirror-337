from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.thing.MedicalIntangible import MedicalIntangible
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.QualitativeValue import QualitativeValue
from typing import Optional, Union, Dict, List, Any


class DoseSchedule(MedicalIntangible):
    """A specific dosing schedule for a drug or supplement."""
    type: str = field(default_factory=lambda: "DoseSchedule", name="@type")
    frequency: str | None = None
    targetPopulation: str | None = None
    doseValue: int | float | 'QualitativeValue' | None = None
    doseUnit: str | None = None