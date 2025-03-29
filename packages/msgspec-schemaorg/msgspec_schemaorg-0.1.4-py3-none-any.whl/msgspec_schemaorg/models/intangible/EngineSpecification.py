from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.StructuredValue import StructuredValue
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.QualitativeValue import QualitativeValue
    from msgspec_schemaorg.models.intangible.QuantitativeValue import QuantitativeValue
from typing import Optional, Union, Dict, List, Any


class EngineSpecification(StructuredValue):
    """Information about the engine of the vehicle. A vehicle can have multiple engines represented by multiple engine specification entities."""
    type: str = field(default_factory=lambda: "EngineSpecification", name="@type")
    engineDisplacement: 'QuantitativeValue' | None = None
    engineType: 'URL' | str | 'QualitativeValue' | None = None
    torque: 'QuantitativeValue' | None = None
    fuelType: 'URL' | str | 'QualitativeValue' | None = None
    enginePower: 'QuantitativeValue' | None = None