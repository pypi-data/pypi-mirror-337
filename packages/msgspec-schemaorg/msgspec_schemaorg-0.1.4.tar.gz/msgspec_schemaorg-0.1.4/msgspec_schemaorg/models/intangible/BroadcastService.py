from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Service import Service
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.BroadcastChannel import BroadcastChannel
    from msgspec_schemaorg.models.intangible.BroadcastFrequencySpecification import BroadcastFrequencySpecification
    from msgspec_schemaorg.models.intangible.BroadcastService import BroadcastService
    from msgspec_schemaorg.models.intangible.Language import Language
    from msgspec_schemaorg.models.organization.Organization import Organization
    from msgspec_schemaorg.models.place.Place import Place
from typing import Optional, Union, Dict, List, Any


class BroadcastService(Service):
    """A delivery service through which content is provided via broadcast over the air or online."""
    type: str = field(default_factory=lambda: "BroadcastService", name="@type")
    parentService: 'BroadcastService' | None = None
    inLanguage: str | 'Language' | None = None
    broadcastFrequency: str | 'BroadcastFrequencySpecification' | None = None
    broadcastTimezone: str | None = None
    hasBroadcastChannel: 'BroadcastChannel' | None = None
    broadcaster: 'Organization' | None = None
    callSign: str | None = None
    broadcastAffiliateOf: 'Organization' | None = None
    area: 'Place' | None = None
    videoFormat: str | None = None
    broadcastDisplayName: str | None = None