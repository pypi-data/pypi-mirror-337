from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Enumeration import Enumeration
from typing import Optional, Union, Dict, List, Any


class TierBenefitEnumeration(Enumeration):
    """An enumeration of possible benefits as part of a loyalty (members) program."""
    type: str = field(default_factory=lambda: "TierBenefitEnumeration", name="@type")