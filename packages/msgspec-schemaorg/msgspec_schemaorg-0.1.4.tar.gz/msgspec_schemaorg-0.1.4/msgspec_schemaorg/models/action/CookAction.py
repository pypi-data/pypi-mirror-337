from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.CreateAction import CreateAction
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.Recipe import Recipe
    from msgspec_schemaorg.models.event.FoodEvent import FoodEvent
    from msgspec_schemaorg.models.place.FoodEstablishment import FoodEstablishment
    from msgspec_schemaorg.models.place.Place import Place
from typing import Optional, Union, Dict, List, Any


class CookAction(CreateAction):
    """The act of producing/preparing food."""
    type: str = field(default_factory=lambda: "CookAction", name="@type")
    recipe: 'Recipe' | None = None
    foodEstablishment: 'FoodEstablishment' | 'Place' | None = None
    foodEvent: 'FoodEvent' | None = None