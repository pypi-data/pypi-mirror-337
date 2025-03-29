from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.thing.Thing import Thing
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.DefinedTerm import DefinedTerm
    from msgspec_schemaorg.models.intangible.Grant import Grant
    from msgspec_schemaorg.models.intangible.PropertyValue import PropertyValue
    from msgspec_schemaorg.models.thing.BioChemEntity import BioChemEntity
    from msgspec_schemaorg.models.thing.Gene import Gene
    from msgspec_schemaorg.models.thing.MedicalCondition import MedicalCondition
    from msgspec_schemaorg.models.thing.Taxon import Taxon
from typing import Optional, Union, Dict, List, Any


class BioChemEntity(Thing):
    """Any biological, chemical, or biochemical thing. For example: a protein; a gene; a chemical; a synthetic chemical."""
    type: str = field(default_factory=lambda: "BioChemEntity", name="@type")
    bioChemSimilarity: 'BioChemEntity' | None = None
    hasRepresentation: 'URL' | str | 'PropertyValue' | None = None
    hasBioChemEntityPart: 'BioChemEntity' | None = None
    taxonomicRange: 'URL' | str | 'DefinedTerm' | 'Taxon' | None = None
    funding: 'Grant' | None = None
    isEncodedByBioChemEntity: 'Gene' | None = None
    isInvolvedInBiologicalProcess: 'URL' | 'PropertyValue' | 'DefinedTerm' | None = None
    associatedDisease: 'URL' | 'MedicalCondition' | 'PropertyValue' | None = None
    bioChemInteraction: 'BioChemEntity' | None = None
    isLocatedInSubcellularLocation: 'URL' | 'PropertyValue' | 'DefinedTerm' | None = None
    hasMolecularFunction: 'URL' | 'PropertyValue' | 'DefinedTerm' | None = None
    biologicalRole: 'DefinedTerm' | None = None
    isPartOfBioChemEntity: 'BioChemEntity' | None = None