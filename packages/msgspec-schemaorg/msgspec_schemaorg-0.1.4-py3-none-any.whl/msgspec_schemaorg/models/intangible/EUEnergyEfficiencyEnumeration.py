from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.EnergyEfficiencyEnumeration import EnergyEfficiencyEnumeration
from typing import Optional, Union, Dict, List, Any


class EUEnergyEfficiencyEnumeration(EnergyEfficiencyEnumeration):
    """Enumerates the EU energy efficiency classes A-G as well as A+, A++, and A+++ as defined in EU directive 2017/1369."""
    type: str = field(default_factory=lambda: "EUEnergyEfficiencyEnumeration", name="@type")