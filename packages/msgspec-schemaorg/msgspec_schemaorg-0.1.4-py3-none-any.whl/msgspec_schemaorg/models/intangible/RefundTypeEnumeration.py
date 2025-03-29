from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Enumeration import Enumeration
from typing import Optional, Union, Dict, List, Any


class RefundTypeEnumeration(Enumeration):
    """Enumerates several kinds of product return refund types."""
    type: str = field(default_factory=lambda: "RefundTypeEnumeration", name="@type")