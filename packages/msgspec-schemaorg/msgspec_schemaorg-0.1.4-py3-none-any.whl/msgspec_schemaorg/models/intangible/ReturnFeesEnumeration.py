from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Enumeration import Enumeration
from typing import Optional, Union, Dict, List, Any


class ReturnFeesEnumeration(Enumeration):
    """Enumerates several kinds of policies for product return fees."""
    type: str = field(default_factory=lambda: "ReturnFeesEnumeration", name="@type")