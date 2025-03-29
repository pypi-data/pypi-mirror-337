from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.thing.MedicalEntity import MedicalEntity
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.ImageObject import ImageObject
    from msgspec_schemaorg.models.thing.AnatomicalStructure import AnatomicalStructure
    from msgspec_schemaorg.models.thing.AnatomicalSystem import AnatomicalSystem
    from msgspec_schemaorg.models.thing.MedicalCondition import MedicalCondition
    from msgspec_schemaorg.models.thing.MedicalTherapy import MedicalTherapy
from typing import Optional, Union, Dict, List, Any


class AnatomicalStructure(MedicalEntity):
    """Any part of the human body, typically a component of an anatomical system. Organs, tissues, and cells are all anatomical structures."""
    type: str = field(default_factory=lambda: "AnatomicalStructure", name="@type")
    diagram: 'ImageObject' | None = None
    partOfSystem: 'AnatomicalSystem' | None = None
    connectedTo: 'AnatomicalStructure' | None = None
    associatedPathophysiology: str | None = None
    relatedCondition: 'MedicalCondition' | None = None
    relatedTherapy: 'MedicalTherapy' | None = None
    subStructure: 'AnatomicalStructure' | None = None
    bodyLocation: str | None = None