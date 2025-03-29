from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.place.CivicStructure import CivicStructure
from typing import Optional, Union, Dict, List, Any


class Airport(CivicStructure):
    """An airport."""
    type: str = field(default_factory=lambda: "Airport", name="@type")
    icaoCode: str | None = None
    iataCode: str | None = None