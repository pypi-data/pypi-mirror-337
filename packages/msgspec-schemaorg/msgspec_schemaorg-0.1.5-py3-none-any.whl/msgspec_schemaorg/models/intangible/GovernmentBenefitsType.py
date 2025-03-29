from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Enumeration import Enumeration
from typing import Optional, Union, Dict, List, Any


class GovernmentBenefitsType(Enumeration):
    """GovernmentBenefitsType enumerates several kinds of government benefits to support the COVID-19 situation. Note that this structure may not capture all benefits offered."""
    type: str = field(default_factory=lambda: "GovernmentBenefitsType", name="@type")