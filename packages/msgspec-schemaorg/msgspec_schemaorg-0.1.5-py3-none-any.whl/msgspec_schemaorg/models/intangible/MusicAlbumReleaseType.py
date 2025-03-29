from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Enumeration import Enumeration
from typing import Optional, Union, Dict, List, Any


class MusicAlbumReleaseType(Enumeration):
    """The kind of release which this album is: single, EP or album."""
    type: str = field(default_factory=lambda: "MusicAlbumReleaseType", name="@type")