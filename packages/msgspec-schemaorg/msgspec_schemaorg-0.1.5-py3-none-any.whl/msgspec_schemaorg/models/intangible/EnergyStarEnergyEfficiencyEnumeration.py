from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.EnergyEfficiencyEnumeration import EnergyEfficiencyEnumeration
from typing import Optional, Union, Dict, List, Any


class EnergyStarEnergyEfficiencyEnumeration(EnergyEfficiencyEnumeration):
    """Used to indicate whether a product is EnergyStar certified."""
    type: str = field(default_factory=lambda: "EnergyStarEnergyEfficiencyEnumeration", name="@type")