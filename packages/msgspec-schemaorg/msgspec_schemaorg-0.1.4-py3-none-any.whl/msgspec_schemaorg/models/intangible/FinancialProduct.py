from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Service import Service
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.QuantitativeValue import QuantitativeValue
from typing import Optional, Union, Dict, List, Any


class FinancialProduct(Service):
    """A product provided to consumers and businesses by financial institutions such as banks, insurance companies, brokerage firms, consumer finance companies, and investment companies which comprise the financial services industry."""
    type: str = field(default_factory=lambda: "FinancialProduct", name="@type")
    feesAndCommissionsSpecification: 'URL' | str | None = None
    interestRate: int | float | 'QuantitativeValue' | None = None
    annualPercentageRate: int | float | 'QuantitativeValue' | None = None