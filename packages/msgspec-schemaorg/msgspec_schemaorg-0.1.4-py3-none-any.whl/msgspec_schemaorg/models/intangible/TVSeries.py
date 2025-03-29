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
    seasons: 'CreativeWorkSeason' | None = None
    countryOfOrigin: 'Country' | None = None
    season: 'URL' | 'CreativeWorkSeason' | None = None
    actors: 'Person' | None = None
    trailer: 'VideoObject' | None = None
    musicBy: 'Person' | 'MusicGroup' | None = None
    containsSeason: 'CreativeWorkSeason' | None = None
    numberOfSeasons: int | None = None
    actor: 'Person' | 'PerformingGroup' | None = None
    directors: 'Person' | None = None
    numberOfEpisodes: int | None = None
    episodes: 'Episode' | None = None
    productionCompany: 'Organization' | None = None
    titleEIDR: 'URL' | str | None = None
    director: 'Person' | None = None
    episode: 'Episode' | None = None