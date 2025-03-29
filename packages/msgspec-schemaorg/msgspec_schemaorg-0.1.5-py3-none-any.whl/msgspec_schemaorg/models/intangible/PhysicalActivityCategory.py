from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Enumeration import Enumeration
from typing import Optional, Union, Dict, List, Any


class PhysicalActivityCategory(Enumeration):
    """Categories of physical activity, organized by physiologic classification."""
    type: str = field(default_factory=lambda: "PhysicalActivityCategory", name="@type")