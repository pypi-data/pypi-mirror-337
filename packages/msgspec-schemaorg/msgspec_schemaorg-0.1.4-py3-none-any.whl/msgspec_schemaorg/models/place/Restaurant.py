from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.place.FoodEstablishment import FoodEstablishment
from typing import Optional, Union, Dict, List, Any


class Restaurant(FoodEstablishment):
    """A restaurant."""
    type: str = field(default_factory=lambda: "Restaurant", name="@type")