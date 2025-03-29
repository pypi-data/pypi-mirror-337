from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.place.LocalBusiness import LocalBusiness
from msgspec_schemaorg.utils import parse_iso8601
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.Audience import Audience
    from msgspec_schemaorg.models.intangible.Language import Language
    from msgspec_schemaorg.models.intangible.LocationFeatureSpecification import LocationFeatureSpecification
    from msgspec_schemaorg.models.intangible.QuantitativeValue import QuantitativeValue
    from msgspec_schemaorg.models.intangible.Rating import Rating
from datetime import datetime, time
from typing import Optional, Union, Dict, List, Any


class LodgingBusiness(LocalBusiness):
    """A lodging business, such as a motel, hotel, or inn."""
    type: str = field(default_factory=lambda: "LodgingBusiness", name="@type")
    petsAllowed: bool | str | None = None
    availableLanguage: str | 'Language' | None = None
    checkoutTime: datetime | time | None = None
    checkinTime: datetime | time | None = None
    numberOfRooms: int | float | 'QuantitativeValue' | None = None
    audience: 'Audience' | None = None
    amenityFeature: 'LocationFeatureSpecification' | None = None
    starRating: 'Rating' | None = None