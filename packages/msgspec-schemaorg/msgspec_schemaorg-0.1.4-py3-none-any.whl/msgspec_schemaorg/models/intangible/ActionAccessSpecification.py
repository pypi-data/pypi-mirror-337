from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Intangible import Intangible
from msgspec_schemaorg.utils import parse_iso8601
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.CategoryCode import CategoryCode
    from msgspec_schemaorg.models.intangible.GeoShape import GeoShape
    from msgspec_schemaorg.models.intangible.MediaSubscription import MediaSubscription
    from msgspec_schemaorg.models.intangible.Offer import Offer
    from msgspec_schemaorg.models.intangible.PhysicalActivityCategory import PhysicalActivityCategory
    from msgspec_schemaorg.models.place.Place import Place
    from msgspec_schemaorg.models.thing.Thing import Thing
from datetime import date, datetime, time
from typing import Optional, Union, Dict, List, Any


class ActionAccessSpecification(Intangible):
    """A set of requirements that must be fulfilled in order to perform an Action."""
    type: str = field(default_factory=lambda: "ActionAccessSpecification", name="@type")
    expectsAcceptanceOf: 'Offer' | None = None
    eligibleRegion: str | 'GeoShape' | 'Place' | None = None
    availabilityStarts: datetime | time | date | None = None
    requiresSubscription: bool | 'MediaSubscription' | None = None
    category: 'URL' | str | 'CategoryCode' | 'Thing' | 'PhysicalActivityCategory' | None = None
    ineligibleRegion: str | 'GeoShape' | 'Place' | None = None
    availabilityEnds: datetime | date | time | None = None