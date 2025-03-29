from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Enumeration import Enumeration
from typing import Optional, Union, Dict, List, Any


class ContactPointOption(Enumeration):
    """Enumerated options related to a ContactPoint."""
    type: str = field(default_factory=lambda: "ContactPointOption", name="@type")