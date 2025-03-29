from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Trip import Trip
from msgspec_schemaorg.utils import parse_iso8601
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.BoardingPolicyType import BoardingPolicyType
    from msgspec_schemaorg.models.intangible.Distance import Distance
    from msgspec_schemaorg.models.intangible.Duration import Duration
    from msgspec_schemaorg.models.organization.Organization import Organization
    from msgspec_schemaorg.models.person.Person import Person
    from msgspec_schemaorg.models.place.Airport import Airport
    from msgspec_schemaorg.models.product.Vehicle import Vehicle
from datetime import datetime
from typing import Optional, Union, Dict, List, Any


class Flight(Trip):
    """An airline flight."""
    type: str = field(default_factory=lambda: "Flight", name="@type")
    departureAirport: 'Airport' | None = None
    flightDistance: str | 'Distance' | None = None
    estimatedFlightDuration: str | 'Duration' | None = None
    mealService: str | None = None
    arrivalGate: str | None = None
    webCheckinTime: datetime | None = None
    seller: 'Person' | 'Organization' | None = None
    departureTerminal: str | None = None
    flightNumber: str | None = None
    departureGate: str | None = None
    arrivalTerminal: str | None = None
    arrivalAirport: 'Airport' | None = None
    carrier: 'Organization' | None = None
    aircraft: str | 'Vehicle' | None = None
    boardingPolicy: 'BoardingPolicyType' | None = None