from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Enumeration import Enumeration
from typing import Optional, Union, Dict, List, Any


class IncentiveQualifiedExpenseType(Enumeration):
    """The types of expenses that are covered by the incentive. For example some incentives are only for the goods (tangible items) but the services (labor) are excluded."""
    type: str = field(default_factory=lambda: "IncentiveQualifiedExpenseType", name="@type")