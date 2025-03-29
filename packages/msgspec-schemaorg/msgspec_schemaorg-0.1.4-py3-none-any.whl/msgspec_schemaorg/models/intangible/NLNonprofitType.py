from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.NonprofitType import NonprofitType
from typing import Optional, Union, Dict, List, Any


class NLNonprofitType(NonprofitType):
    """NLNonprofitType: Non-profit organization type originating from the Netherlands."""
    type: str = field(default_factory=lambda: "NLNonprofitType", name="@type")