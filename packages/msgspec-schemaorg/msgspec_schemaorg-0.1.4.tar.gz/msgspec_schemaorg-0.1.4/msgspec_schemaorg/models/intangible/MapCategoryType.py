from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Enumeration import Enumeration
from typing import Optional, Union, Dict, List, Any


class MapCategoryType(Enumeration):
    """An enumeration of several kinds of Map."""
    type: str = field(default_factory=lambda: "MapCategoryType", name="@type")