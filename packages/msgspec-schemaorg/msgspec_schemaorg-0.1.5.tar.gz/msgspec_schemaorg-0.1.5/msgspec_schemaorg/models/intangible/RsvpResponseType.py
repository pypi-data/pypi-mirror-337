from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Enumeration import Enumeration
from typing import Optional, Union, Dict, List, Any


class RsvpResponseType(Enumeration):
    """RsvpResponseType is an enumeration type whose instances represent responding to an RSVP request."""
    type: str = field(default_factory=lambda: "RsvpResponseType", name="@type")