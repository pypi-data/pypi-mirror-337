from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.MedicalEnumeration import MedicalEnumeration
from typing import Optional, Union, Dict, List, Any


class DrugCostCategory(MedicalEnumeration):
    """Enumerated categories of medical drug costs."""
    type: str = field(default_factory=lambda: "DrugCostCategory", name="@type")