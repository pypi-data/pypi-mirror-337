from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Enumeration import Enumeration
from typing import Optional, Union, Dict, List, Any


class MeasurementMethodEnum(Enumeration):
    """Enumeration(s) for use with [[measurementMethod]]."""
    type: str = field(default_factory=lambda: "MeasurementMethodEnum", name="@type")