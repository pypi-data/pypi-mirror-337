from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.QualitativeValue import QualitativeValue
from typing import Optional, Union, Dict, List, Any


class SteeringPositionValue(QualitativeValue):
    """A value indicating a steering position."""
    type: str = field(default_factory=lambda: "SteeringPositionValue", name="@type")