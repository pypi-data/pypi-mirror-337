from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Intangible import Intangible
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.ListItem import ListItem
    from msgspec_schemaorg.models.thing.Thing import Thing
from typing import Optional, Union, Dict, List, Any


class ListItem(Intangible):
    """An list item, e.g. a step in a checklist or how-to description."""
    type: str = field(default_factory=lambda: "ListItem", name="@type")
    nextItem: 'ListItem' | None = None
    item: 'Thing' | None = None
    position: int | str | None = None
    previousItem: 'ListItem' | None = None