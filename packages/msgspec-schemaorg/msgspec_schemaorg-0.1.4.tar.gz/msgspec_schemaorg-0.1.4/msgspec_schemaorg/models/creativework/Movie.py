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
    countryOfOrigin: 'Country' | None = None
    subtitleLanguage: str | 'Language' | None = None
    actors: 'Person' | None = None
    trailer: 'VideoObject' | None = None
    musicBy: 'Person' | 'MusicGroup' | None = None
    duration: 'QuantitativeValue' | 'Duration' | None = None
    actor: 'Person' | 'PerformingGroup' | None = None
    directors: 'Person' | None = None
    productionCompany: 'Organization' | None = None
    titleEIDR: 'URL' | str | None = None
    director: 'Person' | None = None