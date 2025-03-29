from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Intangible import Intangible
from msgspec_schemaorg.utils import parse_iso8601
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.event.DeliveryEvent import DeliveryEvent
    from msgspec_schemaorg.models.intangible.DeliveryMethod import DeliveryMethod
    from msgspec_schemaorg.models.intangible.Order import Order
    from msgspec_schemaorg.models.intangible.PostalAddress import PostalAddress
    from msgspec_schemaorg.models.organization.Organization import Organization
    from msgspec_schemaorg.models.person.Person import Person
    from msgspec_schemaorg.models.product.Product import Product
from datetime import date, datetime
from typing import Optional, Union, Dict, List, Any


class ParcelDelivery(Intangible):
    """The delivery of a parcel either via the postal service or a commercial service."""
    type: str = field(default_factory=lambda: "ParcelDelivery", name="@type")
    provider: 'Person' | 'Organization' | None = None
    hasDeliveryMethod: 'DeliveryMethod' | None = None
    expectedArrivalUntil: datetime | date | None = None
    partOfOrder: 'Order' | None = None
    trackingNumber: str | None = None
    itemShipped: 'Product' | None = None
    deliveryAddress: 'PostalAddress' | None = None
    deliveryStatus: 'DeliveryEvent' | None = None
    originAddress: 'PostalAddress' | None = None
    expectedArrivalFrom: datetime | date | None = None
    carrier: 'Organization' | None = None
    trackingUrl: 'URL' | None = None