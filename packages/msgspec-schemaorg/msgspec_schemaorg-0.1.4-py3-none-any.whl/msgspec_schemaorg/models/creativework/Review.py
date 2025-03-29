from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.Review import Review
    from msgspec_schemaorg.models.creativework.WebContent import WebContent
    from msgspec_schemaorg.models.intangible.ItemList import ItemList
    from msgspec_schemaorg.models.intangible.ListItem import ListItem
    from msgspec_schemaorg.models.intangible.Rating import Rating
    from msgspec_schemaorg.models.thing.Thing import Thing
from typing import Optional, Union, Dict, List, Any


class Review(CreativeWork):
    """A review of an item - for example, of a restaurant, movie, or store."""
    type: str = field(default_factory=lambda: "Review", name="@type")
    reviewRating: 'Rating' | None = None
    associatedMediaReview: 'Review' | None = None
    associatedReview: 'Review' | None = None
    negativeNotes: str | 'ListItem' | 'ItemList' | 'WebContent' | None = None
    itemReviewed: 'Thing' | None = None
    reviewBody: str | None = None
    positiveNotes: str | 'WebContent' | 'ItemList' | 'ListItem' | None = None
    reviewAspect: str | None = None
    associatedClaimReview: 'Review' | None = None