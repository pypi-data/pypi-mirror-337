from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.StatusEnumeration import StatusEnumeration
from typing import Optional, Union, Dict, List, Any


class ReservationStatusType(StatusEnumeration):
    """Enumerated status values for Reservation."""
    type: str = field(default_factory=lambda: "ReservationStatusType", name="@type")