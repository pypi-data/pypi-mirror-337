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
    activityFrequency: str | 'QuantitativeValue' | None = None
    activityDuration: 'Duration' | 'QuantitativeValue' | None = None
    intensity: str | 'QuantitativeValue' | None = None
    additionalVariable: str | None = None
    restPeriods: str | 'QuantitativeValue' | None = None
    repetitions: int | float | 'QuantitativeValue' | None = None
    workload: 'QuantitativeValue' | 'Energy' | None = None
    exerciseType: str | None = None