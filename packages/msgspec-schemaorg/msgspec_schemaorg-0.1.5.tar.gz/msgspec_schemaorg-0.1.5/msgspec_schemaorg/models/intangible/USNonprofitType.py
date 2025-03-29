from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.NonprofitType import NonprofitType
from typing import Optional, Union, Dict, List, Any


class USNonprofitType(NonprofitType):
    """USNonprofitType: Non-profit organization type originating from the United States."""
    type: str = field(default_factory=lambda: "USNonprofitType", name="@type")