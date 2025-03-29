from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Intangible import Intangible
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.ContactPoint import ContactPoint
    from msgspec_schemaorg.models.intangible.HealthPlanFormulary import HealthPlanFormulary
    from msgspec_schemaorg.models.intangible.HealthPlanNetwork import HealthPlanNetwork
from typing import Optional, Union, Dict, List, Any


class HealthInsurancePlan(Intangible):
    """A US-style health insurance plan, including PPOs, EPOs, and HMOs."""
    type: str = field(default_factory=lambda: "HealthInsurancePlan", name="@type")
    includesHealthPlanNetwork: 'HealthPlanNetwork' | None = None
    usesHealthPlanIdStandard: 'URL' | str | None = None
    healthPlanDrugOption: str | None = None
    healthPlanId: str | None = None
    benefitsSummaryUrl: 'URL' | None = None
    healthPlanMarketingUrl: 'URL' | None = None
    healthPlanDrugTier: str | None = None
    includesHealthPlanFormulary: 'HealthPlanFormulary' | None = None
    contactPoint: 'ContactPoint' | None = None