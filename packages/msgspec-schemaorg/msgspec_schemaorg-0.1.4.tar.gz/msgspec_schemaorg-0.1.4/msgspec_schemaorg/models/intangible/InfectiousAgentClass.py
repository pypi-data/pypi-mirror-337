from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.MedicalEnumeration import MedicalEnumeration
from typing import Optional, Union, Dict, List, Any


class InfectiousAgentClass(MedicalEnumeration):
    """Classes of agents or pathogens that transmit infectious diseases. Enumerated type."""
    type: str = field(default_factory=lambda: "InfectiousAgentClass", name="@type")