from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.thing.Thing import Thing
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.Certification import Certification
    from msgspec_schemaorg.models.creativework.ImageObject import ImageObject
    from msgspec_schemaorg.models.creativework.Map import Map
    from msgspec_schemaorg.models.creativework.Photograph import Photograph
    from msgspec_schemaorg.models.creativework.Review import Review
    from msgspec_schemaorg.models.event.Event import Event
    from msgspec_schemaorg.models.intangible.AggregateRating import AggregateRating
    from msgspec_schemaorg.models.intangible.DefinedTerm import DefinedTerm
    from msgspec_schemaorg.models.intangible.GeoCoordinates import GeoCoordinates
    from msgspec_schemaorg.models.intangible.GeoShape import GeoShape
    from msgspec_schemaorg.models.intangible.GeospatialGeometry import GeospatialGeometry
    from msgspec_schemaorg.models.intangible.LocationFeatureSpecification import LocationFeatureSpecification
    from msgspec_schemaorg.models.intangible.OpeningHoursSpecification import OpeningHoursSpecification
    from msgspec_schemaorg.models.intangible.PostalAddress import PostalAddress
    from msgspec_schemaorg.models.intangible.PropertyValue import PropertyValue
    from msgspec_schemaorg.models.place.Place import Place
from typing import Optional, Union, Dict, List, Any


class Place(Thing):
    """Entities that have a somewhat fixed, physical extension."""
    type: str = field(default_factory=lambda: "Place", name="@type")
    event: 'Event' | None = None
    isicV4: str | None = None
    photos: 'ImageObject' | 'Photograph' | None = None
    aggregateRating: 'AggregateRating' | None = None
    tourBookingPage: 'URL' | None = None
    containedInPlace: 'Place' | None = None
    hasCertification: 'Certification' | None = None
    geoIntersects: 'GeospatialGeometry' | 'Place' | None = None
    containsPlace: 'Place' | None = None
    telephone: str | None = None
    geoOverlaps: 'Place' | 'GeospatialGeometry' | None = None
    hasGS1DigitalLink: 'URL' | None = None
    reviews: 'Review' | None = None
    geoCrosses: 'GeospatialGeometry' | 'Place' | None = None
    keywords: 'URL' | str | 'DefinedTerm' | None = None
    hasDriveThroughService: bool | None = None
    maximumAttendeeCapacity: int | None = None
    specialOpeningHoursSpecification: 'OpeningHoursSpecification' | None = None
    containedIn: 'Place' | None = None
    geoCoveredBy: 'Place' | 'GeospatialGeometry' | None = None
    maps: 'URL' | None = None
    logo: 'URL' | 'ImageObject' | None = None
    geoContains: 'Place' | 'GeospatialGeometry' | None = None
    geo: 'GeoCoordinates' | 'GeoShape' | None = None
    publicAccess: bool | None = None
    latitude: int | float | str | None = None
    map: 'URL' | None = None
    hasMap: 'URL' | 'Map' | None = None
    geoTouches: 'GeospatialGeometry' | 'Place' | None = None
    amenityFeature: 'LocationFeatureSpecification' | None = None
    address: str | 'PostalAddress' | None = None
    additionalProperty: 'PropertyValue' | None = None
    slogan: str | None = None
    review: 'Review' | None = None
    globalLocationNumber: str | None = None
    geoWithin: 'GeospatialGeometry' | 'Place' | None = None
    smokingAllowed: bool | None = None
    longitude: int | float | str | None = None
    geoDisjoint: 'Place' | 'GeospatialGeometry' | None = None
    geoCovers: 'Place' | 'GeospatialGeometry' | None = None
    isAccessibleForFree: bool | None = None
    photo: 'ImageObject' | 'Photograph' | None = None
    faxNumber: str | None = None
    branchCode: str | None = None
    openingHoursSpecification: 'OpeningHoursSpecification' | None = None
    events: 'Event' | None = None
    geoEquals: 'GeospatialGeometry' | 'Place' | None = None