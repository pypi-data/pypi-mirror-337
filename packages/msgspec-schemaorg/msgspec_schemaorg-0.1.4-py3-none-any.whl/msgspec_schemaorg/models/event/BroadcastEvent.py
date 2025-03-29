from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.event.PublicationEvent import PublicationEvent
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.event.Event import Event
    from msgspec_schemaorg.models.intangible.Language import Language
from typing import Optional, Union, Dict, List, Any


class BroadcastEvent(PublicationEvent):
    """An over the air or online broadcast event."""
    type: str = field(default_factory=lambda: "BroadcastEvent", name="@type")
    subtitleLanguage: str | 'Language' | None = None
    isLiveBroadcast: bool | None = None
    broadcastOfEvent: 'Event' | None = None
    videoFormat: str | None = None