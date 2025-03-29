from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.ItemList import ItemList
from typing import Optional, Union, Dict, List, Any


class HowToStep(ItemList):
    """A step in the instructions for how to achieve a result. It is an ordered list with HowToDirection and/or HowToTip items."""
    type: str = field(default_factory=lambda: "HowToStep", name="@type")