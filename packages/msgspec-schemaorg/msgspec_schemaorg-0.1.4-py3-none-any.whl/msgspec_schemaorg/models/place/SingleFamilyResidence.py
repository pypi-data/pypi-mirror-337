from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.place.House import House
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.QuantitativeValue import QuantitativeValue
from typing import Optional, Union, Dict, List, Any


class SingleFamilyResidence(House):
    """Residence type: Single-family home."""
    type: str = field(default_factory=lambda: "SingleFamilyResidence", name="@type")
    numberOfRooms: int | float | 'QuantitativeValue' | None = None
    occupancy: 'QuantitativeValue' | None = None