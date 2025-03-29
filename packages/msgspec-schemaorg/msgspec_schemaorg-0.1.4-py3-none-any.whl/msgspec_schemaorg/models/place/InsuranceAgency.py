from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.place.FinancialService import FinancialService
from typing import Optional, Union, Dict, List, Any


class InsuranceAgency(FinancialService):
    """An Insurance agency."""
    type: str = field(default_factory=lambda: "InsuranceAgency", name="@type")