from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.StructuredValue import StructuredValue
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.MonetaryAmount import MonetaryAmount
from typing import Optional, Union, Dict, List, Any


class RepaymentSpecification(StructuredValue):
    """A structured value representing repayment."""
    type: str = field(default_factory=lambda: "RepaymentSpecification", name="@type")
    downPayment: int | float | 'MonetaryAmount' | None = None
    numberOfLoanPayments: int | float | None = None
    loanPaymentFrequency: int | float | None = None
    loanPaymentAmount: 'MonetaryAmount' | None = None
    earlyPrepaymentPenalty: 'MonetaryAmount' | None = None