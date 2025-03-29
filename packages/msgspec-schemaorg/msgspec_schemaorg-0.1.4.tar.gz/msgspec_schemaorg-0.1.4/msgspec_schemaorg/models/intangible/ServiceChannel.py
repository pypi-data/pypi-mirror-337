from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Intangible import Intangible
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.ContactPoint import ContactPoint
    from msgspec_schemaorg.models.intangible.Duration import Duration
    from msgspec_schemaorg.models.intangible.Language import Language
    from msgspec_schemaorg.models.intangible.PostalAddress import PostalAddress
    from msgspec_schemaorg.models.intangible.Service import Service
    from msgspec_schemaorg.models.place.Place import Place
from typing import Optional, Union, Dict, List, Any


class ServiceChannel(Intangible):
    """A means for accessing a service, e.g. a government office location, web site, or phone number."""
    type: str = field(default_factory=lambda: "ServiceChannel", name="@type")
    availableLanguage: str | 'Language' | None = None
    servicePhone: 'ContactPoint' | None = None
    processingTime: 'Duration' | None = None
    serviceLocation: 'Place' | None = None
    servicePostalAddress: 'PostalAddress' | None = None
    serviceUrl: 'URL' | None = None
    serviceSmsNumber: 'ContactPoint' | None = None
    providesService: 'Service' | None = None