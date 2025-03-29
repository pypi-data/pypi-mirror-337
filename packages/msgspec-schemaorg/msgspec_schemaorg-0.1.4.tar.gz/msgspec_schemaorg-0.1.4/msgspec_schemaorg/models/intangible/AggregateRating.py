from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Rating import Rating
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.thing.Thing import Thing
from typing import Optional, Union, Dict, List, Any


class AggregateRating(Rating):
    """The average rating based on multiple ratings or reviews."""
    type: str = field(default_factory=lambda: "AggregateRating", name="@type")
    reviewCount: int | None = None
    itemReviewed: 'Thing' | None = None
    ratingCount: int | None = None