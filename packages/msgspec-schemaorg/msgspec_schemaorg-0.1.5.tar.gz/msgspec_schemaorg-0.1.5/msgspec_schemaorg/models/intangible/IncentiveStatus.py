from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Enumeration import Enumeration
from typing import Optional, Union, Dict, List, Any


class IncentiveStatus(Enumeration):
    """Enumerates a status for an incentive, such as whether it is active."""
    type: str = field(default_factory=lambda: "IncentiveStatus", name="@type")