from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Enumeration import Enumeration
from typing import Optional, Union, Dict, List, Any


class PaymentMethodType(Enumeration):
    """The type of payment method, only for generic payment types, specific forms of payments, like card payment should be expressed using subclasses of PaymentMethod."""
    type: str = field(default_factory=lambda: "PaymentMethodType", name="@type")