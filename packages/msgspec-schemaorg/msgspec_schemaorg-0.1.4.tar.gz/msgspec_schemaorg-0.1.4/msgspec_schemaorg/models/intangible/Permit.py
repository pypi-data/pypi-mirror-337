from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Intangible import Intangible
from msgspec_schemaorg.utils import parse_iso8601
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.Audience import Audience
    from msgspec_schemaorg.models.intangible.Duration import Duration
    from msgspec_schemaorg.models.intangible.Service import Service
    from msgspec_schemaorg.models.organization.Organization import Organization
    from msgspec_schemaorg.models.place.AdministrativeArea import AdministrativeArea
from datetime import date, datetime
from typing import Optional, Union, Dict, List, Any


class Permit(Intangible):
    """A permit issued by an organization, e.g. a parking pass."""
    type: str = field(default_factory=lambda: "Permit", name="@type")
    issuedThrough: 'Service' | None = None
    validFor: 'Duration' | None = None
    validFrom: datetime | date | None = None
    validIn: 'AdministrativeArea' | None = None
    validUntil: date | None = None
    issuedBy: 'Organization' | None = None
    permitAudience: 'Audience' | None = None