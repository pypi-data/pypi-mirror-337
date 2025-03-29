from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Intangible import Intangible
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.MenuSection import MenuSection
    from msgspec_schemaorg.models.intangible.Demand import Demand
    from msgspec_schemaorg.models.intangible.MenuItem import MenuItem
    from msgspec_schemaorg.models.intangible.NutritionInformation import NutritionInformation
    from msgspec_schemaorg.models.intangible.Offer import Offer
    from msgspec_schemaorg.models.intangible.RestrictedDiet import RestrictedDiet
from typing import Optional, Union, Dict, List, Any


class MenuItem(Intangible):
    """A food or drink item listed in a menu or menu section."""
    type: str = field(default_factory=lambda: "MenuItem", name="@type")
    offers: Union[List[Union['Offer', 'Demand']], Union['Offer', 'Demand'], None] = None
    suitableForDiet: Union[List['RestrictedDiet'], 'RestrictedDiet', None] = None
    nutrition: Union[List['NutritionInformation'], 'NutritionInformation', None] = None
    menuAddOn: Union[List[Union['MenuSection', 'MenuItem']], Union['MenuSection', 'MenuItem'], None] = None