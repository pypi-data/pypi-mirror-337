from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.thing.Vessel import Vessel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.thing.AnatomicalStructure import AnatomicalStructure
    from msgspec_schemaorg.models.thing.AnatomicalSystem import AnatomicalSystem
    from msgspec_schemaorg.models.thing.Vessel import Vessel
from typing import Optional, Union, Dict, List, Any


class Vein(Vessel):
    """A type of blood vessel that specifically carries blood to the heart."""
    type: str = field(default_factory=lambda: "Vein", name="@type")
    regionDrained: 'AnatomicalStructure' | 'AnatomicalSystem' | None = None
    drainsTo: 'Vessel' | None = None
    tributary: 'AnatomicalStructure' | None = None