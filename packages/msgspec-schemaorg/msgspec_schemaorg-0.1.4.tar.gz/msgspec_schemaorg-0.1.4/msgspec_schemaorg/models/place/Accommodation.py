from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.place.Place import Place
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.BedDetails import BedDetails
    from msgspec_schemaorg.models.intangible.BedType import BedType
    from msgspec_schemaorg.models.intangible.Duration import Duration
    from msgspec_schemaorg.models.intangible.FloorPlan import FloorPlan
    from msgspec_schemaorg.models.intangible.LocationFeatureSpecification import LocationFeatureSpecification
    from msgspec_schemaorg.models.intangible.QuantitativeValue import QuantitativeValue
from typing import Optional, Union, Dict, List, Any


class Accommodation(Place):
    """An accommodation is a place that can accommodate human beings, e.g. a hotel room, a camping pitch, or a meeting room. Many accommodations are for overnight stays, but this is not a mandatory requirement.
For more specific types of accommodations not defined in schema.org, one can use [[additionalType]] with external vocabularies.
<br /><br />
See also the <a href="/docs/hotels.html">dedicated document on the use of schema.org for marking up hotels and other forms of accommodations</a>.
"""
    type: str = field(default_factory=lambda: "Accommodation", name="@type")
    petsAllowed: bool | str | None = None
    permittedUsage: str | None = None
    tourBookingPage: 'URL' | None = None
    numberOfBathroomsTotal: int | None = None
    floorSize: 'QuantitativeValue' | None = None
    numberOfBedrooms: int | float | 'QuantitativeValue' | None = None
    numberOfFullBathrooms: int | float | None = None
    accommodationFloorPlan: 'FloorPlan' | None = None
    bed: str | 'BedType' | 'BedDetails' | None = None
    leaseLength: 'QuantitativeValue' | 'Duration' | None = None
    numberOfPartialBathrooms: int | float | None = None
    yearBuilt: int | float | None = None
    numberOfRooms: int | float | 'QuantitativeValue' | None = None
    amenityFeature: 'LocationFeatureSpecification' | None = None
    floorLevel: str | None = None
    accommodationCategory: str | None = None
    occupancy: 'QuantitativeValue' | None = None