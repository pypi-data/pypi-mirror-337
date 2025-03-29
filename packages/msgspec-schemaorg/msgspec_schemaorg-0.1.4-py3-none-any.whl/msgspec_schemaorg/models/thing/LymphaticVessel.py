from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.thing.Vessel import Vessel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.thing.AnatomicalStructure import AnatomicalStructure
    from msgspec_schemaorg.models.thing.AnatomicalSystem import AnatomicalSystem
    from msgspec_schemaorg.models.thing.Vessel import Vessel
from typing import Optional, Union, Dict, List, Any


class LymphaticVessel(Vessel):
    """A type of blood vessel that specifically carries lymph fluid unidirectionally toward the heart."""
    type: str = field(default_factory=lambda: "LymphaticVessel", name="@type")
    regionDrained: 'AnatomicalStructure' | 'AnatomicalSystem' | None = None
    originatesFrom: 'Vessel' | None = None
    runsTo: 'Vessel' | None = None