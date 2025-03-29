from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Enumeration import Enumeration
from typing import Optional, Union, Dict, List, Any


class ReturnMethodEnumeration(Enumeration):
    """Enumerates several types of product return methods."""
    type: str = field(default_factory=lambda: "ReturnMethodEnumeration", name="@type")