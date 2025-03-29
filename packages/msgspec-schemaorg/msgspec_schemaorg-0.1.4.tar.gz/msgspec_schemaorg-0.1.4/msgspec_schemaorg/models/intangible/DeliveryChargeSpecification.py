from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.PriceSpecification import PriceSpecification
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.DeliveryMethod import DeliveryMethod
    from msgspec_schemaorg.models.intangible.GeoShape import GeoShape
    from msgspec_schemaorg.models.place.AdministrativeArea import AdministrativeArea
    from msgspec_schemaorg.models.place.Place import Place
from typing import Optional, Union, Dict, List, Any


class DeliveryChargeSpecification(PriceSpecification):
    """The price for the delivery of an offer using a particular delivery method."""
    type: str = field(default_factory=lambda: "DeliveryChargeSpecification", name="@type")
    eligibleRegion: str | 'GeoShape' | 'Place' | None = None
    appliesToDeliveryMethod: 'DeliveryMethod' | None = None
    ineligibleRegion: str | 'GeoShape' | 'Place' | None = None
    areaServed: str | 'AdministrativeArea' | 'GeoShape' | 'Place' | None = None