from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.ContactPoint import ContactPoint
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.place.Country import Country
from typing import Optional, Union, Dict, List, Any


class PostalAddress(ContactPoint):
    """The mailing address."""
    type: str = field(default_factory=lambda: "PostalAddress", name="@type")
    addressRegion: str | None = None
    streetAddress: str | None = None
    addressCountry: str | 'Country' | None = None
    addressLocality: str | None = None
    postOfficeBoxNumber: str | None = None
    postalCode: str | None = None