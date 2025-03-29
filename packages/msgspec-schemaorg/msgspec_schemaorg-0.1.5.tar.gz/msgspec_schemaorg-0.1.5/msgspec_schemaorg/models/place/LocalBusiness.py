from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.place.Place import Place
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.organization.Organization import Organization
from typing import Optional, Union, Dict, List, Any


class LocalBusiness(Place):
    """A particular physical business or branch of an organization. Examples of LocalBusiness include a restaurant, a particular branch of a restaurant chain, a branch of a bank, a medical practice, a club, a bowling alley, etc."""
    type: str = field(default_factory=lambda: "LocalBusiness", name="@type")
    branchOf: Union[List['Organization'], 'Organization', None] = None
    openingHours: Union[List[str], str, None] = None
    paymentAccepted: Union[List[str], str, None] = None
    priceRange: Union[List[str], str, None] = None
    currenciesAccepted: Union[List[str], str, None] = None