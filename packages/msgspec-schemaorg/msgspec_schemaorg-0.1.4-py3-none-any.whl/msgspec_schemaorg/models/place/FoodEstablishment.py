from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.place.LocalBusiness import LocalBusiness
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.Menu import Menu
    from msgspec_schemaorg.models.intangible.Rating import Rating
from typing import Optional, Union, Dict, List, Any


class FoodEstablishment(LocalBusiness):
    """A food-related business."""
    type: str = field(default_factory=lambda: "FoodEstablishment", name="@type")
    servesCuisine: str | None = None
    menu: 'URL' | str | 'Menu' | None = None
    hasMenu: 'URL' | str | 'Menu' | None = None
    acceptsReservations: 'URL' | bool | str | None = None
    starRating: 'Rating' | None = None