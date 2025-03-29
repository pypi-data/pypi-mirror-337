from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Intangible import Intangible
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.GeospatialGeometry import GeospatialGeometry
    from msgspec_schemaorg.models.place.Place import Place
from typing import Optional, Union, Dict, List, Any


class GeospatialGeometry(Intangible):
    """(Eventually to be defined as) a supertype of GeoShape designed to accommodate definitions from Geo-Spatial best practices."""
    type: str = field(default_factory=lambda: "GeospatialGeometry", name="@type")
    geoIntersects: Union[List[Union['GeospatialGeometry', 'Place']], Union['GeospatialGeometry', 'Place'], None] = None
    geoOverlaps: Union[List[Union['Place', 'GeospatialGeometry']], Union['Place', 'GeospatialGeometry'], None] = None
    geoCrosses: Union[List[Union['GeospatialGeometry', 'Place']], Union['GeospatialGeometry', 'Place'], None] = None
    geoCoveredBy: Union[List[Union['Place', 'GeospatialGeometry']], Union['Place', 'GeospatialGeometry'], None] = None
    geoContains: Union[List[Union['Place', 'GeospatialGeometry']], Union['Place', 'GeospatialGeometry'], None] = None
    geoTouches: Union[List[Union['GeospatialGeometry', 'Place']], Union['GeospatialGeometry', 'Place'], None] = None
    geoWithin: Union[List[Union['GeospatialGeometry', 'Place']], Union['GeospatialGeometry', 'Place'], None] = None
    geoDisjoint: Union[List[Union['Place', 'GeospatialGeometry']], Union['Place', 'GeospatialGeometry'], None] = None
    geoCovers: Union[List[Union['Place', 'GeospatialGeometry']], Union['Place', 'GeospatialGeometry'], None] = None
    geoEquals: Union[List[Union['GeospatialGeometry', 'Place']], Union['GeospatialGeometry', 'Place'], None] = None