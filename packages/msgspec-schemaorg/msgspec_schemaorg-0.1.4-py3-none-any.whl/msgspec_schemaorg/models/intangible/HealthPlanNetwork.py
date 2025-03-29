from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Intangible import Intangible
from typing import Optional, Union, Dict, List, Any


class HealthPlanNetwork(Intangible):
    """A US-style health insurance plan network."""
    type: str = field(default_factory=lambda: "HealthPlanNetwork", name="@type")
    healthPlanCostSharing: bool | None = None
    healthPlanNetworkId: str | None = None
    healthPlanNetworkTier: str | None = None