from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.thing.BioChemEntity import BioChemEntity
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.DefinedTerm import DefinedTerm
    from msgspec_schemaorg.models.intangible.QuantitativeValue import QuantitativeValue
from typing import Optional, Union, Dict, List, Any


class MolecularEntity(BioChemEntity):
    """Any constitutionally or isotopically distinct atom, molecule, ion, ion pair, radical, radical ion, complex, conformer etc., identifiable as a separately distinguishable entity."""
    type: str = field(default_factory=lambda: "MolecularEntity", name="@type")
    molecularWeight: str | 'QuantitativeValue' | None = None
    monoisotopicMolecularWeight: str | 'QuantitativeValue' | None = None
    potentialUse: 'DefinedTerm' | None = None
    inChI: str | None = None
    iupacName: str | None = None
    molecularFormula: str | None = None
    inChIKey: str | None = None
    smiles: str | None = None
    chemicalRole: 'DefinedTerm' | None = None