from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Intangible import Intangible
from msgspec_schemaorg.utils import URL
from typing import Optional, Union, Dict, List, Any


class AlignmentObject(Intangible):
    """An intangible item that describes an alignment between a learning resource and a node in an educational framework.

Should not be used where the nature of the alignment can be described using a simple property, for example to express that a resource [[teaches]] or [[assesses]] a competency."""
    type: str = field(default_factory=lambda: "AlignmentObject", name="@type")
    educationalFramework: str | None = None
    targetName: str | None = None
    targetUrl: 'URL' | None = None
    alignmentType: str | None = None
    targetDescription: str | None = None