from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.MedicalEnumeration import MedicalEnumeration
from typing import Optional, Union, Dict, List, Any


class MedicalImagingTechnique(MedicalEnumeration):
    """Any medical imaging modality typically used for diagnostic purposes. Enumerated type."""
    type: str = field(default_factory=lambda: "MedicalImagingTechnique", name="@type")