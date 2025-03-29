from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Enumeration import Enumeration
from typing import Optional, Union, Dict, List, Any


class CarUsageType(Enumeration):
    """A value indicating a special usage of a car, e.g. commercial rental, driving school, or as a taxi."""
    type: str = field(default_factory=lambda: "CarUsageType", name="@type")