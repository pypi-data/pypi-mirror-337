from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Enumeration import Enumeration
from typing import Optional, Union, Dict, List, Any


class HealthAspectEnumeration(Enumeration):
    """HealthAspectEnumeration enumerates several aspects of health content online, each of which might be described using [[hasHealthAspect]] and [[HealthTopicContent]]."""
    type: str = field(default_factory=lambda: "HealthAspectEnumeration", name="@type")