from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.HowTo import HowTo
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
    from msgspec_schemaorg.models.intangible.Duration import Duration
    from msgspec_schemaorg.models.intangible.ItemList import ItemList
    from msgspec_schemaorg.models.intangible.NutritionInformation import NutritionInformation
    from msgspec_schemaorg.models.intangible.QuantitativeValue import QuantitativeValue
    from msgspec_schemaorg.models.intangible.RestrictedDiet import RestrictedDiet
from typing import Optional, Union, Dict, List, Any


class Recipe(HowTo):
    """A recipe. For dietary restrictions covered by the recipe, a few common restrictions are enumerated via [[suitableForDiet]]. The [[keywords]] property can also be used to add more detail."""
    type: str = field(default_factory=lambda: "Recipe", name="@type")
    recipeCuisine: str | None = None
    suitableForDiet: 'RestrictedDiet' | None = None
    cookTime: 'Duration' | None = None
    nutrition: 'NutritionInformation' | None = None
    cookingMethod: str | None = None
    recipeIngredient: str | None = None
    recipeInstructions: str | 'ItemList' | 'CreativeWork' | None = None
    ingredients: str | None = None
    recipeYield: str | 'QuantitativeValue' | None = None
    recipeCategory: str | None = None