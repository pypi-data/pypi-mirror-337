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
    suggestedAge: Union[List['QuantitativeValue'], 'QuantitativeValue', None] = None
    suggestedMinAge: Union[List[int | float], int | float, None] = None
    suggestedGender: Union[List[Union[str, 'GenderType']], Union[str, 'GenderType'], None] = None
    requiredMinAge: Union[List[int], int, None] = None
    suggestedMeasurement: Union[List['QuantitativeValue'], 'QuantitativeValue', None] = None
    healthCondition: Union[List['MedicalCondition'], 'MedicalCondition', None] = None
    requiredGender: Union[List[str], str, None] = None
    requiredMaxAge: Union[List[int], int, None] = None
    suggestedMaxAge: Union[List[int | float], int | float, None] = None