from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.thing.Thing import Thing
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.DefinedTerm import DefinedTerm
    from msgspec_schemaorg.models.intangible.PropertyValue import PropertyValue
    from msgspec_schemaorg.models.thing.Taxon import Taxon
from typing import Optional, Union, Dict, List, Any


class Taxon(Thing):
    """A set of organisms asserted to represent a natural cohesive biological unit."""
    type: str = field(default_factory=lambda: "Taxon", name="@type")
    parentTaxon: 'URL' | str | 'Taxon' | None = None
    hasDefinedTerm: 'DefinedTerm' | None = None
    childTaxon: 'URL' | str | 'Taxon' | None = None
    taxonRank: 'URL' | str | 'PropertyValue' | None = None