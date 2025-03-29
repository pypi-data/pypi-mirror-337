from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.MapCategoryType import MapCategoryType
from typing import Optional, Union, Dict, List, Any


class Map(CreativeWork):
    """A map."""
    type: str = field(default_factory=lambda: "Map", name="@type")
    mapType: 'MapCategoryType' | None = None