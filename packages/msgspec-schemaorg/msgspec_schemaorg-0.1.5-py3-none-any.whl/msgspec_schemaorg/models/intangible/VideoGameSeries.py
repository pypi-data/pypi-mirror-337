from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.CreativeWorkSeries import CreativeWorkSeries
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
    from msgspec_schemaorg.models.creativework.CreativeWorkSeason import CreativeWorkSeason
    from msgspec_schemaorg.models.creativework.Episode import Episode
    from msgspec_schemaorg.models.creativework.VideoObject import VideoObject
    from msgspec_schemaorg.models.intangible.GamePlayMode import GamePlayMode
    from msgspec_schemaorg.models.intangible.PostalAddress import PostalAddress
    from msgspec_schemaorg.models.intangible.QuantitativeValue import QuantitativeValue
    from msgspec_schemaorg.models.organization.MusicGroup import MusicGroup
    from msgspec_schemaorg.models.organization.Organization import Organization
    from msgspec_schemaorg.models.organization.PerformingGroup import PerformingGroup
    from msgspec_schemaorg.models.person.Person import Person
    from msgspec_schemaorg.models.place.Place import Place
    from msgspec_schemaorg.models.thing.Thing import Thing
from typing import Optional, Union, Dict, List, Any


class VideoGameSeries(CreativeWorkSeries):
    """A video game series."""
    type: str = field(default_factory=lambda: "VideoGameSeries", name="@type")
    seasons: Union[List['CreativeWorkSeason'], 'CreativeWorkSeason', None] = None
    season: Union[List[Union['URL', 'CreativeWorkSeason']], Union['URL', 'CreativeWorkSeason'], None] = None
    gameItem: Union[List['Thing'], 'Thing', None] = None
    playMode: Union[List['GamePlayMode'], 'GamePlayMode', None] = None
    actors: Union[List['Person'], 'Person', None] = None
    trailer: Union[List['VideoObject'], 'VideoObject', None] = None
    musicBy: Union[List[Union['Person', 'MusicGroup']], Union['Person', 'MusicGroup'], None] = None
    numberOfPlayers: Union[List['QuantitativeValue'], 'QuantitativeValue', None] = None
    containsSeason: Union[List['CreativeWorkSeason'], 'CreativeWorkSeason', None] = None
    cheatCode: Union[List['CreativeWork'], 'CreativeWork', None] = None
    numberOfSeasons: Union[List[int], int, None] = None
    gamePlatform: Union[List[Union['URL', str, 'Thing']], Union['URL', str, 'Thing'], None] = None
    actor: Union[List[Union['Person', 'PerformingGroup']], Union['Person', 'PerformingGroup'], None] = None
    quest: Union[List['Thing'], 'Thing', None] = None
    directors: Union[List['Person'], 'Person', None] = None
    numberOfEpisodes: Union[List[int], int, None] = None
    episodes: Union[List['Episode'], 'Episode', None] = None
    gameLocation: Union[List[Union['URL', 'Place', 'PostalAddress']], Union['URL', 'Place', 'PostalAddress'], None] = None
    productionCompany: Union[List['Organization'], 'Organization', None] = None
    characterAttribute: Union[List['Thing'], 'Thing', None] = None
    director: Union[List['Person'], 'Person', None] = None
    episode: Union[List['Episode'], 'Episode', None] = None