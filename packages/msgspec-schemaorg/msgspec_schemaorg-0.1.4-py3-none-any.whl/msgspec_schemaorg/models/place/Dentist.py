from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.place.LocalBusiness import LocalBusiness
from typing import Optional, Union, Dict, List, Any


class Dentist(LocalBusiness):
    """A dentist."""
    type: str = field(default_factory=lambda: "Dentist", name="@type")