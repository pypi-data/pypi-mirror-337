from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.Duration import Duration
    from msgspec_schemaorg.models.intangible.Energy import Energy
    from msgspec_schemaorg.models.intangible.QuantitativeValue import QuantitativeValue
from typing import Optional, Union, Dict, List, Any


class ExercisePlan(CreativeWork):
    """Fitness-related activity designed for a specific health-related purpose, including defined exercise routines as well as activity prescribed by a clinician."""
    type: str = field(default_factory=lambda: "ExercisePlan", name="@type")
    activityFrequency: Union[List[Union[str, 'QuantitativeValue']], Union[str, 'QuantitativeValue'], None] = None
    activityDuration: Union[List[Union['Duration', 'QuantitativeValue']], Union['Duration', 'QuantitativeValue'], None] = None
    intensity: Union[List[Union[str, 'QuantitativeValue']], Union[str, 'QuantitativeValue'], None] = None
    additionalVariable: Union[List[str], str, None] = None
    restPeriods: Union[List[Union[str, 'QuantitativeValue']], Union[str, 'QuantitativeValue'], None] = None
    repetitions: Union[List[Union[int | float, 'QuantitativeValue']], Union[int | float, 'QuantitativeValue'], None] = None
    workload: Union[List[Union['QuantitativeValue', 'Energy']], Union['QuantitativeValue', 'Energy'], None] = None
    exerciseType: Union[List[str], str, None] = None