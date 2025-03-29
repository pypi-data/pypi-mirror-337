from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.StructuredValue import StructuredValue
from msgspec_schemaorg.utils import parse_iso8601
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.MonetaryAmount import MonetaryAmount
from datetime import date, datetime
from typing import Optional, Union, Dict, List, Any


class DatedMoneySpecification(StructuredValue):
    """A DatedMoneySpecification represents monetary values with optional start and end dates. For example, this could represent an employee's salary over a specific period of time. __Note:__ This type has been superseded by [[MonetaryAmount]], use of that type is recommended."""
    type: str = field(default_factory=lambda: "DatedMoneySpecification", name="@type")
    endDate: datetime | date | None = None
    amount: int | float | 'MonetaryAmount' | None = None
    startDate: datetime | date | None = None
    currency: str | None = None