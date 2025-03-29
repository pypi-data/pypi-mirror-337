from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.thing.LifestyleModification import LifestyleModification
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.organization.Organization import Organization
    from msgspec_schemaorg.models.person.Person import Person
from typing import Optional, Union, Dict, List, Any


class Diet(LifestyleModification):
    """A strategy of regulating the intake of food to achieve or maintain a specific health-related goal."""
    type: str = field(default_factory=lambda: "Diet", name="@type")
    endorsers: 'Person' | 'Organization' | None = None
    risks: str | None = None
    dietFeatures: str | None = None
    physiologicalBenefits: str | None = None
    expertConsiderations: str | None = None