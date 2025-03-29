from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Intangible import Intangible
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.ImageObject import ImageObject
    from msgspec_schemaorg.models.intangible.LocationFeatureSpecification import LocationFeatureSpecification
    from msgspec_schemaorg.models.intangible.QuantitativeValue import QuantitativeValue
    from msgspec_schemaorg.models.place.Accommodation import Accommodation
from typing import Optional, Union, Dict, List, Any


class FloorPlan(Intangible):
    """A FloorPlan is an explicit representation of a collection of similar accommodations, allowing the provision of common information (room counts, sizes, layout diagrams) and offers for rental or sale. In typical use, some [[ApartmentComplex]] has an [[accommodationFloorPlan]] which is a [[FloorPlan]].  A FloorPlan is always in the context of a particular place, either a larger [[ApartmentComplex]] or a single [[Apartment]]. The visual/spatial aspects of a floor plan (i.e. room layout, [see wikipedia](https://en.wikipedia.org/wiki/Floor_plan)) can be indicated using [[image]]. """
    type: str = field(default_factory=lambda: "FloorPlan", name="@type")
    petsAllowed: bool | str | None = None
    numberOfBathroomsTotal: int | None = None
    floorSize: 'QuantitativeValue' | None = None
    numberOfBedrooms: int | float | 'QuantitativeValue' | None = None
    numberOfFullBathrooms: int | float | None = None
    numberOfAccommodationUnits: 'QuantitativeValue' | None = None
    numberOfAvailableAccommodationUnits: 'QuantitativeValue' | None = None
    numberOfPartialBathrooms: int | float | None = None
    isPlanForApartment: 'Accommodation' | None = None
    numberOfRooms: int | float | 'QuantitativeValue' | None = None
    amenityFeature: 'LocationFeatureSpecification' | None = None
    layoutImage: 'URL' | 'ImageObject' | None = None