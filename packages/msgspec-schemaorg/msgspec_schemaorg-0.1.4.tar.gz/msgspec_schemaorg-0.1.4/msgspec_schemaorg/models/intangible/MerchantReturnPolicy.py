from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Intangible import Intangible
from msgspec_schemaorg.utils import parse_iso8601
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.MemberProgramTier import MemberProgramTier
    from msgspec_schemaorg.models.intangible.MerchantReturnEnumeration import MerchantReturnEnumeration
    from msgspec_schemaorg.models.intangible.MerchantReturnPolicySeasonalOverride import MerchantReturnPolicySeasonalOverride
    from msgspec_schemaorg.models.intangible.MonetaryAmount import MonetaryAmount
    from msgspec_schemaorg.models.intangible.OfferItemCondition import OfferItemCondition
    from msgspec_schemaorg.models.intangible.PropertyValue import PropertyValue
    from msgspec_schemaorg.models.intangible.RefundTypeEnumeration import RefundTypeEnumeration
    from msgspec_schemaorg.models.intangible.ReturnFeesEnumeration import ReturnFeesEnumeration
    from msgspec_schemaorg.models.intangible.ReturnLabelSourceEnumeration import ReturnLabelSourceEnumeration
    from msgspec_schemaorg.models.intangible.ReturnMethodEnumeration import ReturnMethodEnumeration
    from msgspec_schemaorg.models.place.Country import Country
from datetime import date, datetime
from typing import Optional, Union, Dict, List, Any


class MerchantReturnPolicy(Intangible):
    """A MerchantReturnPolicy provides information about product return policies associated with an [[Organization]], [[Product]], or [[Offer]]."""
    type: str = field(default_factory=lambda: "MerchantReturnPolicy", name="@type")
    itemDefectReturnLabelSource: 'ReturnLabelSourceEnumeration' | None = None
    returnPolicyCountry: str | 'Country' | None = None
    customerRemorseReturnLabelSource: 'ReturnLabelSourceEnumeration' | None = None
    validForMemberTier: 'MemberProgramTier' | None = None
    returnShippingFeesAmount: 'MonetaryAmount' | None = None
    customerRemorseReturnShippingFeesAmount: 'MonetaryAmount' | None = None
    returnFees: 'ReturnFeesEnumeration' | None = None
    inStoreReturnsOffered: bool | None = None
    returnLabelSource: 'ReturnLabelSourceEnumeration' | None = None
    merchantReturnDays: int | datetime | date | None = None
    returnMethod: 'ReturnMethodEnumeration' | None = None
    customerRemorseReturnFees: 'ReturnFeesEnumeration' | None = None
    returnPolicyCategory: 'MerchantReturnEnumeration' | None = None
    merchantReturnLink: 'URL' | None = None
    itemDefectReturnFees: 'ReturnFeesEnumeration' | None = None
    additionalProperty: 'PropertyValue' | None = None
    itemCondition: 'OfferItemCondition' | None = None
    itemDefectReturnShippingFeesAmount: 'MonetaryAmount' | None = None
    returnPolicySeasonalOverride: 'MerchantReturnPolicySeasonalOverride' | None = None
    refundType: 'RefundTypeEnumeration' | None = None
    applicableCountry: str | 'Country' | None = None
    restockingFee: int | float | 'MonetaryAmount' | None = None