from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.StructuredValue import StructuredValue
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.PostalAddress import PostalAddress
    from msgspec_schemaorg.models.place.Country import Country
from typing import Optional, Union, Dict, List, Any


class GeoCoordinates(StructuredValue):
    """The geographic coordinates of a place or event."""
    type: str = field(default_factory=lambda: "GeoCoordinates", name="@type")
    addressCountry: str | 'Country' | None = None
    latitude: int | float | str | None = None
    elevation: int | float | str | None = None
    address: str | 'PostalAddress' | None = None
    postalCode: str | None = None
    longitude: int | float | str | None = None