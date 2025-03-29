from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.StructuredValue import StructuredValue
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.FulfillmentTypeEnumeration import FulfillmentTypeEnumeration
    from msgspec_schemaorg.models.intangible.MemberProgramTier import MemberProgramTier
    from msgspec_schemaorg.models.intangible.QuantitativeValue import QuantitativeValue
    from msgspec_schemaorg.models.intangible.ServicePeriod import ServicePeriod
    from msgspec_schemaorg.models.intangible.ShippingConditions import ShippingConditions
from typing import Optional, Union, Dict, List, Any


class ShippingService(StructuredValue):
    """ShippingService represents the criteria used to determine if and how an offer could be shipped to a customer."""
    type: str = field(default_factory=lambda: "ShippingService", name="@type")
    validForMemberTier: 'MemberProgramTier' | None = None
    shippingConditions: 'ShippingConditions' | None = None
    handlingTime: 'QuantitativeValue' | 'ServicePeriod' | None = None
    fulfillmentType: 'FulfillmentTypeEnumeration' | None = None