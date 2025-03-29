from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.Game import Game
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
    from msgspec_schemaorg.models.creativework.VideoObject import VideoObject
    from msgspec_schemaorg.models.intangible.GamePlayMode import GamePlayMode
    from msgspec_schemaorg.models.intangible.GameServer import GameServer
    from msgspec_schemaorg.models.organization.MusicGroup import MusicGroup
    from msgspec_schemaorg.models.organization.PerformingGroup import PerformingGroup
    from msgspec_schemaorg.models.person.Person import Person
    from msgspec_schemaorg.models.thing.Thing import Thing
from typing import Optional, Union, Dict, List, Any


class VideoGame(Game):
    """A video game is an electronic game that involves human interaction with a user interface to generate visual feedback on a video device."""
    type: str = field(default_factory=lambda: "VideoGame", name="@type")
    gameEdition: str | None = None
    playMode: 'GamePlayMode' | None = None
    actors: 'Person' | None = None
    trailer: 'VideoObject' | None = None
    musicBy: 'Person' | 'MusicGroup' | None = None
    gameServer: 'GameServer' | None = None
    cheatCode: 'CreativeWork' | None = None
    gamePlatform: 'URL' | str | 'Thing' | None = None
    actor: 'Person' | 'PerformingGroup' | None = None
    directors: 'Person' | None = None
    gameTip: 'CreativeWork' | None = None
    director: 'Person' | None = None