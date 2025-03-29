from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Enumeration import Enumeration
from typing import Optional, Union, Dict, List, Any


class DigitalDocumentPermissionType(Enumeration):
    """A type of permission which can be granted for accessing a digital document."""
    type: str = field(default_factory=lambda: "DigitalDocumentPermissionType", name="@type")