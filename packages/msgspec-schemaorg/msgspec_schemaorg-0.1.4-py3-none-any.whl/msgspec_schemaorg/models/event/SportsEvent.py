from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.event.Event import Event
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.organization.SportsTeam import SportsTeam
    from msgspec_schemaorg.models.person.Person import Person
from typing import Optional, Union, Dict, List, Any


class SportsEvent(Event):
    """Event type: Sports event."""
    type: str = field(default_factory=lambda: "SportsEvent", name="@type")
    competitor: 'Person' | 'SportsTeam' | None = None
    sport: 'URL' | str | None = None
    homeTeam: 'Person' | 'SportsTeam' | None = None
    awayTeam: 'Person' | 'SportsTeam' | None = None