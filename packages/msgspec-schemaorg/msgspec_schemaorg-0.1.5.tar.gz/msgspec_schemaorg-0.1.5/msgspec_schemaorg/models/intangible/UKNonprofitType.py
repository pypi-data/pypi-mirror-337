from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.NonprofitType import NonprofitType
from typing import Optional, Union, Dict, List, Any


class UKNonprofitType(NonprofitType):
    """UKNonprofitType: Non-profit organization type originating from the United Kingdom."""
    type: str = field(default_factory=lambda: "UKNonprofitType", name="@type")