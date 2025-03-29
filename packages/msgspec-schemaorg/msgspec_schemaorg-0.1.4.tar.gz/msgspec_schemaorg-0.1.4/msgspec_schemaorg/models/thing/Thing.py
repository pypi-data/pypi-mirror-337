from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.base import SchemaOrgBase
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.action.Action import Action
    from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
    from msgspec_schemaorg.models.creativework.ImageObject import ImageObject
    from msgspec_schemaorg.models.creativework.TextObject import TextObject
    from msgspec_schemaorg.models.event.Event import Event
    from msgspec_schemaorg.models.intangible.PropertyValue import PropertyValue
from typing import Optional, Union, Dict, List, Any


class Thing(SchemaOrgBase):
    """The most generic type of item."""
    type: str = field(default_factory=lambda: "Thing", name="@type")
    name: str | None = None
    mainEntityOfPage: 'URL' | 'CreativeWork' | None = None
    url: 'URL' | None = None
    disambiguatingDescription: str | None = None
    identifier: 'URL' | str | 'PropertyValue' | None = None
    description: str | 'TextObject' | None = None
    subjectOf: 'Event' | 'CreativeWork' | None = None
    alternateName: str | None = None
    additionalType: 'URL' | str | None = None
    potentialAction: 'Action' | None = None
    sameAs: 'URL' | None = None
    image: 'URL' | 'ImageObject' | None = None