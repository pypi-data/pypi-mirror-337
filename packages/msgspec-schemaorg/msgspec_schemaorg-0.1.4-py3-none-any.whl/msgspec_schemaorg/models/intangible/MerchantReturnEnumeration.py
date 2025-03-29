from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Enumeration import Enumeration
from typing import Optional, Union, Dict, List, Any


class MerchantReturnEnumeration(Enumeration):
    """Enumerates several kinds of product return policies."""
    type: str = field(default_factory=lambda: "MerchantReturnEnumeration", name="@type")