from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Intangible import Intangible
from typing import Optional, Union, Dict, List, Any


class HealthPlanFormulary(Intangible):
    """For a given health insurance plan, the specification for costs and coverage of prescription drugs."""
    type: str = field(default_factory=lambda: "HealthPlanFormulary", name="@type")
    offersPrescriptionByMail: bool | None = None
    healthPlanCostSharing: bool | None = None
    healthPlanDrugTier: str | None = None