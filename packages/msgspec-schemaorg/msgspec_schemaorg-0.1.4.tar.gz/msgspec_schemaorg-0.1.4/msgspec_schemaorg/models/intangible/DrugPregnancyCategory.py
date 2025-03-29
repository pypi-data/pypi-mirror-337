from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.MedicalEnumeration import MedicalEnumeration
from typing import Optional, Union, Dict, List, Any


class DrugPregnancyCategory(MedicalEnumeration):
    """Categories that represent an assessment of the risk of fetal injury due to a drug or pharmaceutical used as directed by the mother during pregnancy."""
    type: str = field(default_factory=lambda: "DrugPregnancyCategory", name="@type")