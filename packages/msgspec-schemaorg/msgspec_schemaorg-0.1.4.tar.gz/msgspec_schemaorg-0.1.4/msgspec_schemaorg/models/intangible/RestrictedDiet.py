from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Enumeration import Enumeration
from typing import Optional, Union, Dict, List, Any


class RestrictedDiet(Enumeration):
    """A diet restricted to certain foods or preparations for cultural, religious, health or lifestyle reasons. """
    type: str = field(default_factory=lambda: "RestrictedDiet", name="@type")