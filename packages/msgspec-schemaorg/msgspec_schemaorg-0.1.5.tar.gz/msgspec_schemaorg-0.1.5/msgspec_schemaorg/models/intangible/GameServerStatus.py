from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.StatusEnumeration import StatusEnumeration
from typing import Optional, Union, Dict, List, Any


class GameServerStatus(StatusEnumeration):
    """Status of a game server."""
    type: str = field(default_factory=lambda: "GameServerStatus", name="@type")