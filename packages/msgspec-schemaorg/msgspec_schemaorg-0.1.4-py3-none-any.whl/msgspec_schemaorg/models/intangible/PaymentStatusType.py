from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.StatusEnumeration import StatusEnumeration
from typing import Optional, Union, Dict, List, Any


class PaymentStatusType(StatusEnumeration):
    """A specific payment status. For example, PaymentDue, PaymentComplete, etc."""
    type: str = field(default_factory=lambda: "PaymentStatusType", name="@type")