from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Audience import Audience
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.GenderType import GenderType
    from msgspec_schemaorg.models.intangible.QuantitativeValue import QuantitativeValue
    from msgspec_schemaorg.models.thing.MedicalCondition import MedicalCondition
from typing import Optional, Union, Dict, List, Any


class PeopleAudience(Audience):
    """A set of characteristics belonging to people, e.g. who compose an item's target audience."""
    type: str = field(default_factory=lambda: "PeopleAudience", name="@type")
    suggestedAge: 'QuantitativeValue' | None = None
    suggestedMinAge: int | float | None = None
    suggestedGender: str | 'GenderType' | None = None
    requiredMinAge: int | None = None
    suggestedMeasurement: 'QuantitativeValue' | None = None
    healthCondition: 'MedicalCondition' | None = None
    requiredGender: str | None = None
    requiredMaxAge: int | None = None
    suggestedMaxAge: int | float | None = None