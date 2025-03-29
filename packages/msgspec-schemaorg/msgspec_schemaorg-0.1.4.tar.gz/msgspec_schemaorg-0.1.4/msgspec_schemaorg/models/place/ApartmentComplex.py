from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.place.Residence import Residence
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.QuantitativeValue import QuantitativeValue
from typing import Optional, Union, Dict, List, Any


class ApartmentComplex(Residence):
    """Residence type: Apartment complex."""
    type: str = field(default_factory=lambda: "ApartmentComplex", name="@type")
    petsAllowed: bool | str | None = None
    tourBookingPage: 'URL' | None = None
    numberOfBedrooms: int | float | 'QuantitativeValue' | None = None
    numberOfAccommodationUnits: 'QuantitativeValue' | None = None
    numberOfAvailableAccommodationUnits: 'QuantitativeValue' | None = None