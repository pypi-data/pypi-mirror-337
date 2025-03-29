from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Enumeration import Enumeration
from typing import Optional, Union, Dict, List, Any


class BookFormatType(Enumeration):
    """The publication format of the book."""
    type: str = field(default_factory=lambda: "BookFormatType", name="@type")