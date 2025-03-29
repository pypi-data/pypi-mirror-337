from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.ListItem import ListItem
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.MediaObject import MediaObject
    from msgspec_schemaorg.models.intangible.Duration import Duration
    from msgspec_schemaorg.models.intangible.HowToSupply import HowToSupply
    from msgspec_schemaorg.models.intangible.HowToTool import HowToTool
from typing import Optional, Union, Dict, List, Any


class HowToDirection(ListItem):
    """A direction indicating a single action to do in the instructions for how to achieve a result."""
    type: str = field(default_factory=lambda: "HowToDirection", name="@type")
    tool: str | 'HowToTool' | None = None
    duringMedia: 'URL' | 'MediaObject' | None = None
    prepTime: 'Duration' | None = None
    afterMedia: 'URL' | 'MediaObject' | None = None
    performTime: 'Duration' | None = None
    totalTime: 'Duration' | None = None
    supply: str | 'HowToSupply' | None = None
    beforeMedia: 'URL' | 'MediaObject' | None = None