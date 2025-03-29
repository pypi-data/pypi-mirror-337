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
    inker: Union[List['Person'], 'Person', None] = None
    artist: Union[List['Person'], 'Person', None] = None
    letterer: Union[List['Person'], 'Person', None] = None
    colorist: Union[List['Person'], 'Person', None] = None
    weight: Union[List[Union['QuantitativeValue', 'Mass']], Union['QuantitativeValue', 'Mass'], None] = None
    artMedium: Union[List[Union['URL', str]], Union['URL', str], None] = None
    artworkSurface: Union[List[Union['URL', str]], Union['URL', str], None] = None
    penciler: Union[List['Person'], 'Person', None] = None
    surface: Union[List[Union['URL', str]], Union['URL', str], None] = None
    artEdition: Union[List[Union[int, str]], Union[int, str], None] = None
    artform: Union[List[Union['URL', str]], Union['URL', str], None] = None
    width: Union[List[Union['Distance', 'QuantitativeValue']], Union['Distance', 'QuantitativeValue'], None] = None
    depth: Union[List[Union['QuantitativeValue', 'Distance']], Union['QuantitativeValue', 'Distance'], None] = None
    height: Union[List[Union['Distance', 'QuantitativeValue']], Union['Distance', 'QuantitativeValue'], None] = None