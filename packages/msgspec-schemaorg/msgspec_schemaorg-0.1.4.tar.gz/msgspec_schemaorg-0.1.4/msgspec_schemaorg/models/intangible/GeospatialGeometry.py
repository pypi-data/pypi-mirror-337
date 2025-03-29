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
    geoIntersects: 'GeospatialGeometry' | 'Place' | None = None
    geoOverlaps: 'Place' | 'GeospatialGeometry' | None = None
    geoCrosses: 'GeospatialGeometry' | 'Place' | None = None
    geoCoveredBy: 'Place' | 'GeospatialGeometry' | None = None
    geoContains: 'Place' | 'GeospatialGeometry' | None = None
    geoTouches: 'GeospatialGeometry' | 'Place' | None = None
    geoWithin: 'GeospatialGeometry' | 'Place' | None = None
    geoDisjoint: 'Place' | 'GeospatialGeometry' | None = None
    geoCovers: 'Place' | 'GeospatialGeometry' | None = None
    geoEquals: 'GeospatialGeometry' | 'Place' | None = None