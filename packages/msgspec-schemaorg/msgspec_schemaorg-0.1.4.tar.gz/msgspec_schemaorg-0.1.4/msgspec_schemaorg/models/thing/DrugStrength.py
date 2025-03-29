from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.thing.MedicalIntangible import MedicalIntangible
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.place.AdministrativeArea import AdministrativeArea
    from msgspec_schemaorg.models.thing.MaximumDoseSchedule import MaximumDoseSchedule
from typing import Optional, Union, Dict, List, Any


class DrugStrength(MedicalIntangible):
    """A specific strength in which a medical drug is available in a specific country."""
    type: str = field(default_factory=lambda: "DrugStrength", name="@type")
    activeIngredient: str | None = None
    availableIn: 'AdministrativeArea' | None = None
    strengthUnit: str | None = None
    maximumIntake: 'MaximumDoseSchedule' | None = None
    strengthValue: int | float | None = None