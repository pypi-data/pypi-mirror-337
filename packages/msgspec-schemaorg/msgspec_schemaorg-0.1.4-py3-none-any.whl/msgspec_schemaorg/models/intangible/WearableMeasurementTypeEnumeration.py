from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.MeasurementTypeEnumeration import MeasurementTypeEnumeration
from typing import Optional, Union, Dict, List, Any


class WearableMeasurementTypeEnumeration(MeasurementTypeEnumeration):
    """Enumerates common types of measurement for wearables products."""
    type: str = field(default_factory=lambda: "WearableMeasurementTypeEnumeration", name="@type")