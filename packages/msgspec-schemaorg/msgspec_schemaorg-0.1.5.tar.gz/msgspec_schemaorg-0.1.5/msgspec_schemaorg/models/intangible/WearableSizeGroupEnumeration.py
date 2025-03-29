from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.SizeGroupEnumeration import SizeGroupEnumeration
from typing import Optional, Union, Dict, List, Any


class WearableSizeGroupEnumeration(SizeGroupEnumeration):
    """Enumerates common size groups (also known as "size types") for wearable products."""
    type: str = field(default_factory=lambda: "WearableSizeGroupEnumeration", name="@type")