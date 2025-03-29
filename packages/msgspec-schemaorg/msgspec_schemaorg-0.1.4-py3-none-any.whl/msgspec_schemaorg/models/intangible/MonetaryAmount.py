from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.StructuredValue import StructuredValue
from msgspec_schemaorg.utils import parse_iso8601
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.StructuredValue import StructuredValue
from datetime import date, datetime
from typing import Optional, Union, Dict, List, Any


class MonetaryAmount(StructuredValue):
    """A monetary value or range. This type can be used to describe an amount of money such as $50 USD, or a range as in describing a bank account being suitable for a balance between £1,000 and £1,000,000 GBP, or the value of a salary, etc. It is recommended to use [[PriceSpecification]] Types to describe the price of an Offer, Invoice, etc."""
    type: str = field(default_factory=lambda: "MonetaryAmount", name="@type")
    maxValue: int | float | None = None
    validFrom: datetime | date | None = None
    validThrough: datetime | date | None = None
    value: int | float | bool | str | 'StructuredValue' | None = None
    minValue: int | float | None = None
    currency: str | None = None