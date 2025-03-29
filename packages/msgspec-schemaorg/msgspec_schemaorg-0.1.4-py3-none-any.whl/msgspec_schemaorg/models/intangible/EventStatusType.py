from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.StatusEnumeration import StatusEnumeration
from typing import Optional, Union, Dict, List, Any


class EventStatusType(StatusEnumeration):
    """EventStatusType is an enumeration type whose instances represent several states that an Event may be in."""
    type: str = field(default_factory=lambda: "EventStatusType", name="@type")