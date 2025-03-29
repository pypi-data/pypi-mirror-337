from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Enumeration import Enumeration
from typing import Optional, Union, Dict, List, Any


class GamePlayMode(Enumeration):
    """Indicates whether this game is multi-player, co-op or single-player."""
    type: str = field(default_factory=lambda: "GamePlayMode", name="@type")