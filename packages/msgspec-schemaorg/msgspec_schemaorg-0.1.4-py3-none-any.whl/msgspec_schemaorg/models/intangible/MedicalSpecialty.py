from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Specialty import Specialty
from typing import Optional, Union, Dict, List, Any


class MedicalSpecialty(Specialty):
    """Any specific branch of medical science or practice. Medical specialities include clinical specialties that pertain to particular organ systems and their respective disease states, as well as allied health specialties. Enumerated type."""
    type: str = field(default_factory=lambda: "MedicalSpecialty", name="@type")