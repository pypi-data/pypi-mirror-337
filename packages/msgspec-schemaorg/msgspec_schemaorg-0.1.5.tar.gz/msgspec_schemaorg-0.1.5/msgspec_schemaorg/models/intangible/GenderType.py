from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Enumeration import Enumeration
from typing import Optional, Union, Dict, List, Any


class GenderType(Enumeration):
    """An enumeration of genders."""
    type: str = field(default_factory=lambda: "GenderType", name="@type")