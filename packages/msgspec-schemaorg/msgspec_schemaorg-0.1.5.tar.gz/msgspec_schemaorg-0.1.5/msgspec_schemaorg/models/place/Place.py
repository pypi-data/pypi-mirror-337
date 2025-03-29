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
    event: Union[List['Event'], 'Event', None] = None
    isicV4: Union[List[str], str, None] = None
    photos: Union[List[Union['ImageObject', 'Photograph']], Union['ImageObject', 'Photograph'], None] = None
    aggregateRating: Union[List['AggregateRating'], 'AggregateRating', None] = None
    tourBookingPage: Union[List['URL'], 'URL', None] = None
    containedInPlace: Union[List['Place'], 'Place', None] = None
    hasCertification: Union[List['Certification'], 'Certification', None] = None
    geoIntersects: Union[List[Union['GeospatialGeometry', 'Place']], Union['GeospatialGeometry', 'Place'], None] = None
    containsPlace: Union[List['Place'], 'Place', None] = None
    telephone: Union[List[str], str, None] = None
    geoOverlaps: Union[List[Union['Place', 'GeospatialGeometry']], Union['Place', 'GeospatialGeometry'], None] = None
    hasGS1DigitalLink: Union[List['URL'], 'URL', None] = None
    reviews: Union[List['Review'], 'Review', None] = None
    geoCrosses: Union[List[Union['GeospatialGeometry', 'Place']], Union['GeospatialGeometry', 'Place'], None] = None
    keywords: Union[List[Union['URL', str, 'DefinedTerm']], Union['URL', str, 'DefinedTerm'], None] = None
    hasDriveThroughService: Union[List[bool], bool, None] = None
    maximumAttendeeCapacity: Union[List[int], int, None] = None
    specialOpeningHoursSpecification: Union[List['OpeningHoursSpecification'], 'OpeningHoursSpecification', None] = None
    containedIn: Union[List['Place'], 'Place', None] = None
    geoCoveredBy: Union[List[Union['Place', 'GeospatialGeometry']], Union['Place', 'GeospatialGeometry'], None] = None
    maps: Union[List['URL'], 'URL', None] = None
    logo: Union[List[Union['URL', 'ImageObject']], Union['URL', 'ImageObject'], None] = None
    geoContains: Union[List[Union['Place', 'GeospatialGeometry']], Union['Place', 'GeospatialGeometry'], None] = None
    geo: Union[List[Union['GeoCoordinates', 'GeoShape']], Union['GeoCoordinates', 'GeoShape'], None] = None
    publicAccess: Union[List[bool], bool, None] = None
    latitude: Union[List[Union[int | float, str]], Union[int | float, str], None] = None
    map: Union[List['URL'], 'URL', None] = None
    hasMap: Union[List[Union['URL', 'Map']], Union['URL', 'Map'], None] = None
    geoTouches: Union[List[Union['GeospatialGeometry', 'Place']], Union['GeospatialGeometry', 'Place'], None] = None
    amenityFeature: Union[List['LocationFeatureSpecification'], 'LocationFeatureSpecification', None] = None
    address: Union[List[Union[str, 'PostalAddress']], Union[str, 'PostalAddress'], None] = None
    additionalProperty: Union[List['PropertyValue'], 'PropertyValue', None] = None
    slogan: Union[List[str], str, None] = None
    review: Union[List['Review'], 'Review', None] = None
    globalLocationNumber: Union[List[str], str, None] = None
    geoWithin: Union[List[Union['GeospatialGeometry', 'Place']], Union['GeospatialGeometry', 'Place'], None] = None
    smokingAllowed: Union[List[bool], bool, None] = None
    longitude: Union[List[Union[int | float, str]], Union[int | float, str], None] = None
    geoDisjoint: Union[List[Union['Place', 'GeospatialGeometry']], Union['Place', 'GeospatialGeometry'], None] = None
    geoCovers: Union[List[Union['Place', 'GeospatialGeometry']], Union['Place', 'GeospatialGeometry'], None] = None
    isAccessibleForFree: Union[List[bool], bool, None] = None
    photo: Union[List[Union['ImageObject', 'Photograph']], Union['ImageObject', 'Photograph'], None] = None
    faxNumber: Union[List[str], str, None] = None
    branchCode: Union[List[str], str, None] = None
    openingHoursSpecification: Union[List['OpeningHoursSpecification'], 'OpeningHoursSpecification', None] = None
    events: Union[List['Event'], 'Event', None] = None
    geoEquals: Union[List[Union['GeospatialGeometry', 'Place']], Union['GeospatialGeometry', 'Place'], None] = None