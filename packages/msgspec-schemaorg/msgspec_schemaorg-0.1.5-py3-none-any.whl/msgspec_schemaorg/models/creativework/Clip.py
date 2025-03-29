from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.CreativeWorkSeason import CreativeWorkSeason
    from msgspec_schemaorg.models.creativework.Episode import Episode
    from msgspec_schemaorg.models.creativework.HyperTocEntry import HyperTocEntry
    from msgspec_schemaorg.models.intangible.CreativeWorkSeries import CreativeWorkSeries
    from msgspec_schemaorg.models.organization.MusicGroup import MusicGroup
    from msgspec_schemaorg.models.organization.PerformingGroup import PerformingGroup
    from msgspec_schemaorg.models.person.Person import Person
from typing import Optional, Union, Dict, List, Any


class Clip(CreativeWork):
    """A short TV or radio program or a segment/part of a program."""
    type: str = field(default_factory=lambda: "Clip", name="@type")
    clipNumber: Union[List[Union[int, str]], Union[int, str], None] = None
    actors: Union[List['Person'], 'Person', None] = None
    endOffset: Union[List[Union[int | float, 'HyperTocEntry']], Union[int | float, 'HyperTocEntry'], None] = None
    musicBy: Union[List[Union['Person', 'MusicGroup']], Union['Person', 'MusicGroup'], None] = None
    partOfEpisode: Union[List['Episode'], 'Episode', None] = None
    actor: Union[List[Union['Person', 'PerformingGroup']], Union['Person', 'PerformingGroup'], None] = None
    directors: Union[List['Person'], 'Person', None] = None
    partOfSeason: Union[List['CreativeWorkSeason'], 'CreativeWorkSeason', None] = None
    partOfSeries: Union[List['CreativeWorkSeries'], 'CreativeWorkSeries', None] = None
    startOffset: Union[List[Union[int | float, 'HyperTocEntry']], Union[int | float, 'HyperTocEntry'], None] = None
    director: Union[List['Person'], 'Person', None] = None