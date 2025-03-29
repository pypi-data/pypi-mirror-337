from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Intangible import Intangible
from msgspec_schemaorg.utils import parse_iso8601
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.Demand import Demand
    from msgspec_schemaorg.models.intangible.ItemList import ItemList
    from msgspec_schemaorg.models.intangible.Offer import Offer
    from msgspec_schemaorg.models.intangible.Trip import Trip
    from msgspec_schemaorg.models.organization.Organization import Organization
    from msgspec_schemaorg.models.person.Person import Person
    from msgspec_schemaorg.models.place.Place import Place
from datetime import datetime, time
from typing import Optional, Union, Dict, List, Any


class Trip(Intangible):
    """A trip or journey. An itinerary of visits to one or more places."""
    type: str = field(default_factory=lambda: "Trip", name="@type")
    provider: 'Person' | 'Organization' | None = None
    tripOrigin: 'Place' | None = None
    departureTime: datetime | time | None = None
    partOfTrip: 'Trip' | None = None
    offers: 'Offer' | 'Demand' | None = None
    itinerary: 'ItemList' | 'Place' | None = None
    arrivalTime: datetime | time | None = None
    subTrip: 'Trip' | None = None