from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Intangible import Intangible
from msgspec_schemaorg.utils import parse_iso8601
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.PriceSpecification import PriceSpecification
    from msgspec_schemaorg.models.intangible.Seat import Seat
    from msgspec_schemaorg.models.organization.Organization import Organization
    from msgspec_schemaorg.models.person.Person import Person
from datetime import date, datetime
from typing import Optional, Union, Dict, List, Any


class Ticket(Intangible):
    """Used to describe a ticket to an event, a flight, a bus ride, etc."""
    type: str = field(default_factory=lambda: "Ticket", name="@type")
    totalPrice: int | float | str | 'PriceSpecification' | None = None
    ticketToken: 'URL' | str | None = None
    issuedBy: 'Organization' | None = None
    dateIssued: datetime | date | None = None
    ticketedSeat: 'Seat' | None = None
    ticketNumber: str | None = None
    priceCurrency: str | None = None
    underName: 'Person' | 'Organization' | None = None