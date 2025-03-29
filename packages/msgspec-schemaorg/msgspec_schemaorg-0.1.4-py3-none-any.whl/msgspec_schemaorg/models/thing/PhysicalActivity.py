from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.thing.LifestyleModification import LifestyleModification
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.CategoryCode import CategoryCode
    from msgspec_schemaorg.models.intangible.PhysicalActivityCategory import PhysicalActivityCategory
    from msgspec_schemaorg.models.thing.AnatomicalStructure import AnatomicalStructure
    from msgspec_schemaorg.models.thing.AnatomicalSystem import AnatomicalSystem
    from msgspec_schemaorg.models.thing.SuperficialAnatomy import SuperficialAnatomy
    from msgspec_schemaorg.models.thing.Thing import Thing
from typing import Optional, Union, Dict, List, Any


class PhysicalActivity(LifestyleModification):
    """Any bodily activity that enhances or maintains physical fitness and overall health and wellness. Includes activity that is part of daily living and routine, structured exercise, and exercise prescribed as part of a medical treatment or recovery plan."""
    type: str = field(default_factory=lambda: "PhysicalActivity", name="@type")
    associatedAnatomy: 'SuperficialAnatomy' | 'AnatomicalStructure' | 'AnatomicalSystem' | None = None
    category: 'URL' | str | 'CategoryCode' | 'Thing' | 'PhysicalActivityCategory' | None = None
    epidemiology: str | None = None
    pathophysiology: str | None = None