from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Enumeration import Enumeration
from typing import Optional, Union, Dict, List, Any


class FulfillmentTypeEnumeration(Enumeration):
    """A type of product fulfillment."""
    type: str = field(default_factory=lambda: "FulfillmentTypeEnumeration", name="@type")