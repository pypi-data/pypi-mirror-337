from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
from msgspec_schemaorg.utils import parse_iso8601
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
    from msgspec_schemaorg.models.intangible.Audience import Audience
    from msgspec_schemaorg.models.intangible.ContactPoint import ContactPoint
    from msgspec_schemaorg.models.organization.Organization import Organization
    from msgspec_schemaorg.models.person.Person import Person
from datetime import date, datetime
from typing import Optional, Union, Dict, List, Any


class Message(CreativeWork):
    """A single message from a sender to one or more organizations or people."""
    type: str = field(default_factory=lambda: "Message", name="@type")
    ccRecipient: 'Organization' | 'ContactPoint' | 'Person' | None = None
    bccRecipient: 'ContactPoint' | 'Person' | 'Organization' | None = None
    recipient: 'Organization' | 'Audience' | 'ContactPoint' | 'Person' | None = None
    toRecipient: 'Organization' | 'Audience' | 'ContactPoint' | 'Person' | None = None
    dateRead: datetime | date | None = None
    sender: 'Audience' | 'Person' | 'Organization' | None = None
    dateReceived: datetime | None = None
    dateSent: datetime | None = None
    messageAttachment: 'CreativeWork' | None = None