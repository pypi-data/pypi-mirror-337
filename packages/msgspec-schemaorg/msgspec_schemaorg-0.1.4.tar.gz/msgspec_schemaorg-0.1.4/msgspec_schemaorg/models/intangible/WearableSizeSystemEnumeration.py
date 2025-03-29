from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.SizeSystemEnumeration import SizeSystemEnumeration
from typing import Optional, Union, Dict, List, Any


class WearableSizeSystemEnumeration(SizeSystemEnumeration):
    """Enumerates common size systems specific for wearable products."""
    type: str = field(default_factory=lambda: "WearableSizeSystemEnumeration", name="@type")