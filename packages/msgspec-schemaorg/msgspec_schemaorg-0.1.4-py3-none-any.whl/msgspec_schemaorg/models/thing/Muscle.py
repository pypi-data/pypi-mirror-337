from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.thing.AnatomicalStructure import AnatomicalStructure
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.thing.AnatomicalStructure import AnatomicalStructure
    from msgspec_schemaorg.models.thing.Muscle import Muscle
    from msgspec_schemaorg.models.thing.Nerve import Nerve
    from msgspec_schemaorg.models.thing.Vessel import Vessel
from typing import Optional, Union, Dict, List, Any


class Muscle(AnatomicalStructure):
    """A muscle is an anatomical structure consisting of a contractile form of tissue that animals use to effect movement."""
    type: str = field(default_factory=lambda: "Muscle", name="@type")
    antagonist: 'Muscle' | None = None
    nerve: 'Nerve' | None = None
    bloodSupply: 'Vessel' | None = None
    muscleAction: str | None = None
    insertion: 'AnatomicalStructure' | None = None