from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.organization.Organization import Organization
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.BoardingPolicyType import BoardingPolicyType
from typing import Optional, Union, Dict, List, Any


class Airline(Organization):
    """An organization that provides flights for passengers."""
    type: str = field(default_factory=lambda: "Airline", name="@type")
    boardingPolicy: 'BoardingPolicyType' | None = None
    iataCode: str | None = None