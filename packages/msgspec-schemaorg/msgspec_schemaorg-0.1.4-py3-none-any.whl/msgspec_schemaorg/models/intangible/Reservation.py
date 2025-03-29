from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Intangible import Intangible
from msgspec_schemaorg.utils import parse_iso8601
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.PriceSpecification import PriceSpecification
    from msgspec_schemaorg.models.intangible.ProgramMembership import ProgramMembership
    from msgspec_schemaorg.models.intangible.ReservationStatusType import ReservationStatusType
    from msgspec_schemaorg.models.intangible.Ticket import Ticket
    from msgspec_schemaorg.models.organization.Organization import Organization
    from msgspec_schemaorg.models.person.Person import Person
    from msgspec_schemaorg.models.thing.Thing import Thing
from datetime import datetime
from typing import Optional, Union, Dict, List, Any


class Reservation(Intangible):
    """Describes a reservation for travel, dining or an event. Some reservations require tickets. \\n\\nNote: This type is for information about actual reservations, e.g. in confirmation emails or HTML pages with individual confirmations of reservations. For offers of tickets, restaurant reservations, flights, or rental cars, use [[Offer]]."""
    type: str = field(default_factory=lambda: "Reservation", name="@type")
    provider: 'Person' | 'Organization' | None = None
    programMembershipUsed: 'ProgramMembership' | None = None
    totalPrice: int | float | str | 'PriceSpecification' | None = None
    broker: 'Person' | 'Organization' | None = None
    reservationStatus: 'ReservationStatusType' | None = None
    reservationId: str | None = None
    bookingTime: datetime | None = None
    modifiedTime: datetime | None = None
    priceCurrency: str | None = None
    bookingAgent: 'Person' | 'Organization' | None = None
    reservationFor: 'Thing' | None = None
    underName: 'Person' | 'Organization' | None = None
    reservedTicket: 'Ticket' | None = None