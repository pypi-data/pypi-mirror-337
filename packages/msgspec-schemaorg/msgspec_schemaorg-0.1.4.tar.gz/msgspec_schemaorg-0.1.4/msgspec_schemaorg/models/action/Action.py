from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.thing.Thing import Thing
from msgspec_schemaorg.utils import parse_iso8601
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.HowTo import HowTo
    from msgspec_schemaorg.models.intangible.ActionStatusType import ActionStatusType
    from msgspec_schemaorg.models.intangible.EntryPoint import EntryPoint
    from msgspec_schemaorg.models.intangible.PostalAddress import PostalAddress
    from msgspec_schemaorg.models.intangible.VirtualLocation import VirtualLocation
    from msgspec_schemaorg.models.organization.Organization import Organization
    from msgspec_schemaorg.models.person.Person import Person
    from msgspec_schemaorg.models.place.Place import Place
    from msgspec_schemaorg.models.thing.Thing import Thing
from datetime import datetime, time
from typing import Optional, Union, Dict, List, Any


class Action(Thing):
    """An action performed by a direct agent and indirect participants upon a direct object. Optionally happens at a location with the help of an inanimate instrument. The execution of the action may produce a result. Specific action sub-type documentation specifies the exact expectation of each argument/role.\\n\\nSee also [blog post](http://blog.schema.org/2014/04/announcing-schemaorg-actions.html) and [Actions overview document](https://schema.org/docs/actions.html)."""
    type: str = field(default_factory=lambda: "Action", name="@type")
    provider: 'Person' | 'Organization' | None = None
    actionProcess: 'HowTo' | None = None
    startTime: datetime | time | None = None
    actionStatus: 'ActionStatusType' | None = None
    object: 'Thing' | None = None
    error: 'Thing' | None = None
    location: str | 'Place' | 'VirtualLocation' | 'PostalAddress' | None = None
    agent: 'Person' | 'Organization' | None = None
    result: 'Thing' | None = None
    target: 'URL' | 'EntryPoint' | None = None
    endTime: datetime | time | None = None
    instrument: 'Thing' | None = None
    participant: 'Person' | 'Organization' | None = None