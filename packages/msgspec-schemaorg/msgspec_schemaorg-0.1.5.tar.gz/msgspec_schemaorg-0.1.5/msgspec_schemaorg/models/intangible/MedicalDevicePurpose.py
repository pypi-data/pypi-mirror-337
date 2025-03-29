from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.MedicalEnumeration import MedicalEnumeration
from typing import Optional, Union, Dict, List, Any


class MedicalDevicePurpose(MedicalEnumeration):
    """Categories of medical devices, organized by the purpose or intended use of the device."""
    type: str = field(default_factory=lambda: "MedicalDevicePurpose", name="@type")