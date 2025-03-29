from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
from msgspec_schemaorg.utils import parse_iso8601
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.Episode import Episode
    from msgspec_schemaorg.models.creativework.VideoObject import VideoObject
    from msgspec_schemaorg.models.intangible.CreativeWorkSeries import CreativeWorkSeries
    from msgspec_schemaorg.models.organization.Organization import Organization
    from msgspec_schemaorg.models.organization.PerformingGroup import PerformingGroup
    from msgspec_schemaorg.models.person.Person import Person
from datetime import date, datetime
from typing import Optional, Union, Dict, List, Any


class CreativeWorkSeason(CreativeWork):
    """A media season, e.g. TV, radio, video game etc."""
    type: str = field(default_factory=lambda: "CreativeWorkSeason", name="@type")
    endDate: datetime | date | None = None
    trailer: 'VideoObject' | None = None
    actor: 'Person' | 'PerformingGroup' | None = None
    seasonNumber: int | str | None = None
    startDate: datetime | date | None = None
    numberOfEpisodes: int | None = None
    episodes: 'Episode' | None = None
    partOfSeries: 'CreativeWorkSeries' | None = None
    productionCompany: 'Organization' | None = None
    director: 'Person' | None = None
    episode: 'Episode' | None = None