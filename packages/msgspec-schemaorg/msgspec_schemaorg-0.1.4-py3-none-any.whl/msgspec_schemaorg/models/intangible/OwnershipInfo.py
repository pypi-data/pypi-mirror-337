from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.StructuredValue import StructuredValue
from msgspec_schemaorg.utils import parse_iso8601
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.Service import Service
    from msgspec_schemaorg.models.organization.Organization import Organization
    from msgspec_schemaorg.models.person.Person import Person
    from msgspec_schemaorg.models.product.Product import Product
from datetime import datetime
from typing import Optional, Union, Dict, List, Any


class OwnershipInfo(StructuredValue):
    """A structured value providing information about when a certain organization or person owned a certain product."""
    type: str = field(default_factory=lambda: "OwnershipInfo", name="@type")
    ownedFrom: datetime | None = None
    acquiredFrom: 'Person' | 'Organization' | None = None
    typeOfGood: 'Product' | 'Service' | None = None
    ownedThrough: datetime | None = None