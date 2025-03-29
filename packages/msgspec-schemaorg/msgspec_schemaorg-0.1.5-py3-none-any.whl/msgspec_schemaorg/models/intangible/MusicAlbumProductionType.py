from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Enumeration import Enumeration
from typing import Optional, Union, Dict, List, Any


class MusicAlbumProductionType(Enumeration):
    """Classification of the album by its type of content: soundtrack, live album, studio album, etc."""
    type: str = field(default_factory=lambda: "MusicAlbumProductionType", name="@type")