from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.CreativeWorkSeries import CreativeWorkSeries
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.CreativeWorkSeason import CreativeWorkSeason
    from msgspec_schemaorg.models.creativework.Episode import Episode
    from msgspec_schemaorg.models.creativework.VideoObject import VideoObject
    from msgspec_schemaorg.models.organization.MusicGroup import MusicGroup
    from msgspec_schemaorg.models.organization.Organization import Organization
    from msgspec_schemaorg.models.organization.PerformingGroup import PerformingGroup
    from msgspec_schemaorg.models.person.Person import Person
    from msgspec_schemaorg.models.place.Country import Country
from typing import Optional, Union, Dict, List, Any


class TVSeries(CreativeWorkSeries):
    """CreativeWorkSeries dedicated to TV broadcast and associated online delivery."""
    type: str = field(default_factory=lambda: "TVSeries", name="@type")
    seasons: Union[List['CreativeWorkSeason'], 'CreativeWorkSeason', None] = None
    countryOfOrigin: Union[List['Country'], 'Country', None] = None
    season: Union[List[Union['URL', 'CreativeWorkSeason']], Union['URL', 'CreativeWorkSeason'], None] = None
    actors: Union[List['Person'], 'Person', None] = None
    trailer: Union[List['VideoObject'], 'VideoObject', None] = None
    musicBy: Union[List[Union['Person', 'MusicGroup']], Union['Person', 'MusicGroup'], None] = None
    containsSeason: Union[List['CreativeWorkSeason'], 'CreativeWorkSeason', None] = None
    numberOfSeasons: Union[List[int], int, None] = None
    actor: Union[List[Union['Person', 'PerformingGroup']], Union['Person', 'PerformingGroup'], None] = None
    directors: Union[List['Person'], 'Person', None] = None
    numberOfEpisodes: Union[List[int], int, None] = None
    episodes: Union[List['Episode'], 'Episode', None] = None
    productionCompany: Union[List['Organization'], 'Organization', None] = None
    titleEIDR: Union[List[Union['URL', str]], Union['URL', str], None] = None
    director: Union[List['Person'], 'Person', None] = None
    episode: Union[List['Episode'], 'Episode', None] = None