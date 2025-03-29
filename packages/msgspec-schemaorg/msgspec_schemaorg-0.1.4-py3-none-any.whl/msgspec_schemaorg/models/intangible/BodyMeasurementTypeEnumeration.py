from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.MeasurementTypeEnumeration import MeasurementTypeEnumeration
from typing import Optional, Union, Dict, List, Any


class BodyMeasurementTypeEnumeration(MeasurementTypeEnumeration):
    """Enumerates types (or dimensions) of a person's body measurements, for example for fitting of clothes."""
    type: str = field(default_factory=lambda: "BodyMeasurementTypeEnumeration", name="@type")