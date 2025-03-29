from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.QualitativeValue import QualitativeValue
from typing import Optional, Union, Dict, List, Any


class DriveWheelConfigurationValue(QualitativeValue):
    """A value indicating which roadwheels will receive torque."""
    type: str = field(default_factory=lambda: "DriveWheelConfigurationValue", name="@type")