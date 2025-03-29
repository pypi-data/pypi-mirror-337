from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.event.Event import Event
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.Movie import Movie
    from msgspec_schemaorg.models.intangible.Language import Language
from typing import Optional, Union, Dict, List, Any


class ScreeningEvent(Event):
    """A screening of a movie or other video."""
    type: str = field(default_factory=lambda: "ScreeningEvent", name="@type")
    subtitleLanguage: str | 'Language' | None = None
    workPresented: 'Movie' | None = None
    videoFormat: str | None = None