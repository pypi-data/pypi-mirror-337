from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.VideoObject import VideoObject
    from msgspec_schemaorg.models.intangible.Duration import Duration
    from msgspec_schemaorg.models.intangible.Language import Language
    from msgspec_schemaorg.models.intangible.QuantitativeValue import QuantitativeValue
    from msgspec_schemaorg.models.organization.MusicGroup import MusicGroup
    from msgspec_schemaorg.models.organization.Organization import Organization
    from msgspec_schemaorg.models.organization.PerformingGroup import PerformingGroup
    from msgspec_schemaorg.models.person.Person import Person
    from msgspec_schemaorg.models.place.Country import Country
from typing import Optional, Union, Dict, List, Any


class Movie(CreativeWork):
    """A movie."""
    type: str = field(default_factory=lambda: "Movie", name="@type")
    countryOfOrigin: Union[List['Country'], 'Country', None] = None
    subtitleLanguage: Union[List[Union[str, 'Language']], Union[str, 'Language'], None] = None
    actors: Union[List['Person'], 'Person', None] = None
    trailer: Union[List['VideoObject'], 'VideoObject', None] = None
    musicBy: Union[List[Union['Person', 'MusicGroup']], Union['Person', 'MusicGroup'], None] = None
    duration: Union[List[Union['QuantitativeValue', 'Duration']], Union['QuantitativeValue', 'Duration'], None] = None
    actor: Union[List[Union['Person', 'PerformingGroup']], Union['Person', 'PerformingGroup'], None] = None
    directors: Union[List['Person'], 'Person', None] = None
    productionCompany: Union[List['Organization'], 'Organization', None] = None
    titleEIDR: Union[List[Union['URL', str]], Union['URL', str], None] = None
    director: Union[List['Person'], 'Person', None] = None