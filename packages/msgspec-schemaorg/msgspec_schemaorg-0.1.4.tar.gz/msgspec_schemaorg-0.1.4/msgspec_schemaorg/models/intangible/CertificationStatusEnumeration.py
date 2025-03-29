from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Enumeration import Enumeration
from typing import Optional, Union, Dict, List, Any


class CertificationStatusEnumeration(Enumeration):
    """Enumerates the different statuses of a Certification (Active and Inactive)."""
    type: str = field(default_factory=lambda: "CertificationStatusEnumeration", name="@type")