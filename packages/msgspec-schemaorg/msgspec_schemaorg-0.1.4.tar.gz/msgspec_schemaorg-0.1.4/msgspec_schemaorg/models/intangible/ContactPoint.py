from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.StructuredValue import StructuredValue
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.ContactPointOption import ContactPointOption
    from msgspec_schemaorg.models.intangible.GeoShape import GeoShape
    from msgspec_schemaorg.models.intangible.Language import Language
    from msgspec_schemaorg.models.intangible.OpeningHoursSpecification import OpeningHoursSpecification
    from msgspec_schemaorg.models.place.AdministrativeArea import AdministrativeArea
    from msgspec_schemaorg.models.place.Place import Place
    from msgspec_schemaorg.models.product.Product import Product
from typing import Optional, Union, Dict, List, Any


class ContactPoint(StructuredValue):
    """A contact point&#x2014;for example, a Customer Complaints department."""
    type: str = field(default_factory=lambda: "ContactPoint", name="@type")
    telephone: str | None = None
    availableLanguage: str | 'Language' | None = None
    hoursAvailable: 'OpeningHoursSpecification' | None = None
    contactType: str | None = None
    serviceArea: 'GeoShape' | 'AdministrativeArea' | 'Place' | None = None
    contactOption: 'ContactPointOption' | None = None
    productSupported: str | 'Product' | None = None
    areaServed: str | 'AdministrativeArea' | 'GeoShape' | 'Place' | None = None
    faxNumber: str | None = None
    email: str | None = None