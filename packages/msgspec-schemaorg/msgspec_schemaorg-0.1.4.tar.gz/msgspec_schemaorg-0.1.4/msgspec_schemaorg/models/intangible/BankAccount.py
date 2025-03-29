from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.FinancialProduct import FinancialProduct
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.MonetaryAmount import MonetaryAmount
from typing import Optional, Union, Dict, List, Any


class BankAccount(FinancialProduct):
    """A product or service offered by a bank whereby one may deposit, withdraw or transfer money and in some cases be paid interest."""
    type: str = field(default_factory=lambda: "BankAccount", name="@type")
    bankAccountType: 'URL' | str | None = None
    accountOverdraftLimit: 'MonetaryAmount' | None = None
    accountMinimumInflow: 'MonetaryAmount' | None = None