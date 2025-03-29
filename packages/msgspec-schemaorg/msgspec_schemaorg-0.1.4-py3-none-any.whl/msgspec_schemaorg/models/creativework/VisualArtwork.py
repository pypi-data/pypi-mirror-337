from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.Distance import Distance
    from msgspec_schemaorg.models.intangible.Mass import Mass
    from msgspec_schemaorg.models.intangible.QuantitativeValue import QuantitativeValue
    from msgspec_schemaorg.models.person.Person import Person
from typing import Optional, Union, Dict, List, Any


class VisualArtwork(CreativeWork):
    """A work of art that is primarily visual in character."""
    type: str = field(default_factory=lambda: "VisualArtwork", name="@type")
    inker: 'Person' | None = None
    artist: 'Person' | None = None
    letterer: 'Person' | None = None
    colorist: 'Person' | None = None
    weight: 'QuantitativeValue' | 'Mass' | None = None
    artMedium: 'URL' | str | None = None
    artworkSurface: 'URL' | str | None = None
    penciler: 'Person' | None = None
    surface: 'URL' | str | None = None
    artEdition: int | str | None = None
    artform: 'URL' | str | None = None
    width: 'Distance' | 'QuantitativeValue' | None = None
    depth: 'QuantitativeValue' | 'Distance' | None = None
    height: 'Distance' | 'QuantitativeValue' | None = None