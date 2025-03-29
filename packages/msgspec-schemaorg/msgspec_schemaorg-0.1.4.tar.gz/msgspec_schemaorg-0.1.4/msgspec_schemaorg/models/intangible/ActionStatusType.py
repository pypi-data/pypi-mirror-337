from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.StatusEnumeration import StatusEnumeration
from typing import Optional, Union, Dict, List, Any


class ActionStatusType(StatusEnumeration):
    """The status of an Action."""
    type: str = field(default_factory=lambda: "ActionStatusType", name="@type")