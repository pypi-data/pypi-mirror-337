from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.StructuredValue import StructuredValue
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.Energy import Energy
    from msgspec_schemaorg.models.intangible.Mass import Mass
from typing import Optional, Union, Dict, List, Any


class NutritionInformation(StructuredValue):
    """Nutritional information about the recipe."""
    type: str = field(default_factory=lambda: "NutritionInformation", name="@type")
    servingSize: str | None = None
    unsaturatedFatContent: 'Mass' | None = None
    sodiumContent: 'Mass' | None = None
    cholesterolContent: 'Mass' | None = None
    transFatContent: 'Mass' | None = None
    calories: 'Energy' | None = None
    sugarContent: 'Mass' | None = None
    fiberContent: 'Mass' | None = None
    proteinContent: 'Mass' | None = None
    fatContent: 'Mass' | None = None
    carbohydrateContent: 'Mass' | None = None
    saturatedFatContent: 'Mass' | None = None