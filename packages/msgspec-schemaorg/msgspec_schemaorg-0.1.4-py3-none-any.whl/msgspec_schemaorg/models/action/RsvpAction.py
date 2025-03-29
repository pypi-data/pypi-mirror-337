from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.InformAction import InformAction
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.Comment import Comment
    from msgspec_schemaorg.models.intangible.RsvpResponseType import RsvpResponseType
from typing import Optional, Union, Dict, List, Any


class RsvpAction(InformAction):
    """The act of notifying an event organizer as to whether you expect to attend the event."""
    type: str = field(default_factory=lambda: "RsvpAction", name="@type")
    additionalNumberOfGuests: int | float | None = None
    rsvpResponse: 'RsvpResponseType' | None = None
    comment: 'Comment' | None = None