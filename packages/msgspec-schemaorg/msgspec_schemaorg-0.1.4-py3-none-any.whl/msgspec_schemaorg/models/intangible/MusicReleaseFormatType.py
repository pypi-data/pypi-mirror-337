from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Enumeration import Enumeration
from typing import Optional, Union, Dict, List, Any


class MusicReleaseFormatType(Enumeration):
    """Format of this release (the type of recording media used, i.e. compact disc, digital media, LP, etc.)."""
    type: str = field(default_factory=lambda: "MusicReleaseFormatType", name="@type")