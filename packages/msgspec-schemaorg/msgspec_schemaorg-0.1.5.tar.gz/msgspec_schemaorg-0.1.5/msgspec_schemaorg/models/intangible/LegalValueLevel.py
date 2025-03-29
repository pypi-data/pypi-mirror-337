from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Enumeration import Enumeration
from typing import Optional, Union, Dict, List, Any


class LegalValueLevel(Enumeration):
    """A list of possible levels for the legal validity of a legislation."""
    type: str = field(default_factory=lambda: "LegalValueLevel", name="@type")