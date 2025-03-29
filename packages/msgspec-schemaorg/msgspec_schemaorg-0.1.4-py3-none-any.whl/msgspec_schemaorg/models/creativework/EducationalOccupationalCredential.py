from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.DefinedTerm import DefinedTerm
    from msgspec_schemaorg.models.intangible.Duration import Duration
    from msgspec_schemaorg.models.organization.Organization import Organization
    from msgspec_schemaorg.models.place.AdministrativeArea import AdministrativeArea
from typing import Optional, Union, Dict, List, Any


class EducationalOccupationalCredential(CreativeWork):
    """An educational or occupational credential. A diploma, academic degree, certification, qualification, badge, etc., that may be awarded to a person or other entity that meets the requirements defined by the credentialer."""
    type: str = field(default_factory=lambda: "EducationalOccupationalCredential", name="@type")
    credentialCategory: 'URL' | str | 'DefinedTerm' | None = None
    recognizedBy: 'Organization' | None = None
    validFor: 'Duration' | None = None
    educationalLevel: 'URL' | str | 'DefinedTerm' | None = None
    validIn: 'AdministrativeArea' | None = None
    competencyRequired: 'URL' | str | 'DefinedTerm' | None = None