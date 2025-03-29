from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.CreativeWorkSeries import CreativeWorkSeries
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.VideoObject import VideoObject
    from msgspec_schemaorg.models.organization.MusicGroup import MusicGroup
    from msgspec_schemaorg.models.organization.Organization import Organization
    from msgspec_schemaorg.models.organization.PerformingGroup import PerformingGroup
    from msgspec_schemaorg.models.person.Person import Person
from typing import Optional, Union, Dict, List, Any


class MovieSeries(CreativeWorkSeries):
    """A series of movies. Included movies can be indicated with the hasPart property."""
    type: str = field(default_factory=lambda: "MovieSeries", name="@type")
    actors: Union[List['Person'], 'Person', None] = None
    trailer: Union[List['VideoObject'], 'VideoObject', None] = None
    musicBy: Union[List[Union['Person', 'MusicGroup']], Union['Person', 'MusicGroup'], None] = None
    actor: Union[List[Union['Person', 'PerformingGroup']], Union['Person', 'PerformingGroup'], None] = None
    directors: Union[List['Person'], 'Person', None] = None
    productionCompany: Union[List['Organization'], 'Organization', None] = None
    director: Union[List['Person'], 'Person', None] = None