from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.StructuredValue import StructuredValue
from msgspec_schemaorg.utils import parse_iso8601
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.MemberProgramTier import MemberProgramTier
    from msgspec_schemaorg.models.intangible.PriceSpecification import PriceSpecification
    from msgspec_schemaorg.models.intangible.QuantitativeValue import QuantitativeValue
from datetime import date, datetime
from typing import Optional, Union, Dict, List, Any


class PriceSpecification(StructuredValue):
    """A structured value representing a price or price range. Typically, only the subclasses of this type are used for markup. It is recommended to use [[MonetaryAmount]] to describe independent amounts of money such as a salary, credit card limits, etc."""
    type: str = field(default_factory=lambda: "PriceSpecification", name="@type")
    minPrice: int | float | None = None
    eligibleQuantity: 'QuantitativeValue' | None = None
    maxPrice: int | float | None = None
    validForMemberTier: 'MemberProgramTier' | None = None
    membershipPointsEarned: int | float | 'QuantitativeValue' | None = None
    price: int | float | str | None = None
    validFrom: datetime | date | None = None
    validThrough: datetime | date | None = None
    valueAddedTaxIncluded: bool | None = None
    eligibleTransactionVolume: 'PriceSpecification' | None = None
    priceCurrency: str | None = None