from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.FinancialProduct import FinancialProduct
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.Duration import Duration
    from msgspec_schemaorg.models.intangible.MonetaryAmount import MonetaryAmount
    from msgspec_schemaorg.models.intangible.QuantitativeValue import QuantitativeValue
    from msgspec_schemaorg.models.intangible.RepaymentSpecification import RepaymentSpecification
    from msgspec_schemaorg.models.thing.Thing import Thing
from typing import Optional, Union, Dict, List, Any


class LoanOrCredit(FinancialProduct):
    """A financial product for the loaning of an amount of money, or line of credit, under agreed terms and charges."""
    type: str = field(default_factory=lambda: "LoanOrCredit", name="@type")
    loanTerm: 'QuantitativeValue' | None = None
    loanRepaymentForm: 'RepaymentSpecification' | None = None
    loanType: 'URL' | str | None = None
    amount: int | float | 'MonetaryAmount' | None = None
    gracePeriod: 'Duration' | None = None
    recourseLoan: bool | None = None
    requiredCollateral: str | 'Thing' | None = None
    currency: str | None = None
    renegotiableLoan: bool | None = None