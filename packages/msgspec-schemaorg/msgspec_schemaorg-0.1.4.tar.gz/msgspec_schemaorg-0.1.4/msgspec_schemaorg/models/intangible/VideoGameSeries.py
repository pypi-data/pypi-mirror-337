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
    seasons: 'CreativeWorkSeason' | None = None
    season: 'URL' | 'CreativeWorkSeason' | None = None
    gameItem: 'Thing' | None = None
    playMode: 'GamePlayMode' | None = None
    actors: 'Person' | None = None
    trailer: 'VideoObject' | None = None
    musicBy: 'Person' | 'MusicGroup' | None = None
    numberOfPlayers: 'QuantitativeValue' | None = None
    containsSeason: 'CreativeWorkSeason' | None = None
    cheatCode: 'CreativeWork' | None = None
    numberOfSeasons: int | None = None
    gamePlatform: 'URL' | str | 'Thing' | None = None
    actor: 'Person' | 'PerformingGroup' | None = None
    quest: 'Thing' | None = None
    directors: 'Person' | None = None
    numberOfEpisodes: int | None = None
    episodes: 'Episode' | None = None
    gameLocation: 'URL' | 'Place' | 'PostalAddress' | None = None
    productionCompany: 'Organization' | None = None
    characterAttribute: 'Thing' | None = None
    director: 'Person' | None = None
    episode: 'Episode' | None = None