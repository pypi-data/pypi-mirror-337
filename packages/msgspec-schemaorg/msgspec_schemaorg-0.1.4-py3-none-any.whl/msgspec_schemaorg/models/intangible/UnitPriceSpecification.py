from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.PriceSpecification import PriceSpecification
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.Duration import Duration
    from msgspec_schemaorg.models.intangible.PriceComponentTypeEnumeration import PriceComponentTypeEnumeration
    from msgspec_schemaorg.models.intangible.PriceTypeEnumeration import PriceTypeEnumeration
    from msgspec_schemaorg.models.intangible.QuantitativeValue import QuantitativeValue
from typing import Optional, Union, Dict, List, Any


class UnitPriceSpecification(PriceSpecification):
    """The price asked for a given offer by the respective organization or person."""
    type: str = field(default_factory=lambda: "UnitPriceSpecification", name="@type")
    billingIncrement: int | float | None = None
    billingDuration: int | float | 'QuantitativeValue' | 'Duration' | None = None
    unitText: str | None = None
    priceType: str | 'PriceTypeEnumeration' | None = None
    referenceQuantity: 'QuantitativeValue' | None = None
    unitCode: 'URL' | str | None = None
    priceComponentType: 'PriceComponentTypeEnumeration' | None = None
    billingStart: int | float | None = None