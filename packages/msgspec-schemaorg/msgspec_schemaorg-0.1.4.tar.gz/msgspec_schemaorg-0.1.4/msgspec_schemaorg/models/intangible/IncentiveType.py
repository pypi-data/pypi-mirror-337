from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Enumeration import Enumeration
from typing import Optional, Union, Dict, List, Any


class IncentiveType(Enumeration):
    """Enumerates common financial incentives for products, including tax credits, tax deductions, rebates and subsidies, etc."""
    type: str = field(default_factory=lambda: "IncentiveType", name="@type")