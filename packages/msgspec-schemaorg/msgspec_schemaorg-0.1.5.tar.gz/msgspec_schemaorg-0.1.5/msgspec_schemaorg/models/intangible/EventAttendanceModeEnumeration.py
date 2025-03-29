from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Enumeration import Enumeration
from typing import Optional, Union, Dict, List, Any


class EventAttendanceModeEnumeration(Enumeration):
    """An EventAttendanceModeEnumeration value is one of potentially several modes of organising an event, relating to whether it is online or offline."""
    type: str = field(default_factory=lambda: "EventAttendanceModeEnumeration", name="@type")