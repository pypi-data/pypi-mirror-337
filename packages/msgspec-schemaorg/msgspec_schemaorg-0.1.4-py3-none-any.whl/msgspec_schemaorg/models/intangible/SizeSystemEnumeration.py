from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Enumeration import Enumeration
from typing import Optional, Union, Dict, List, Any


class SizeSystemEnumeration(Enumeration):
    """Enumerates common size systems for different categories of products, for example "EN-13402" or "UK" for wearables or "Imperial" for screws."""
    type: str = field(default_factory=lambda: "SizeSystemEnumeration", name="@type")