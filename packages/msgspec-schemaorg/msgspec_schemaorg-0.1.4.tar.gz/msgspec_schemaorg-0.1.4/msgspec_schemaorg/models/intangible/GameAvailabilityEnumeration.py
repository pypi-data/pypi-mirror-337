from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Enumeration import Enumeration
from typing import Optional, Union, Dict, List, Any


class GameAvailabilityEnumeration(Enumeration):
    """For a [[VideoGame]], such as used with a [[PlayGameAction]], an enumeration of the kind of game availability offered. """
    type: str = field(default_factory=lambda: "GameAvailabilityEnumeration", name="@type")