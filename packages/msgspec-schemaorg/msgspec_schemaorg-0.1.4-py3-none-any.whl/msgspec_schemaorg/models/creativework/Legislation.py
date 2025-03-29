from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
from msgspec_schemaorg.utils import parse_iso8601
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.Legislation import Legislation
    from msgspec_schemaorg.models.intangible.CategoryCode import CategoryCode
    from msgspec_schemaorg.models.intangible.LegalForceStatus import LegalForceStatus
    from msgspec_schemaorg.models.organization.Organization import Organization
    from msgspec_schemaorg.models.person.Person import Person
    from msgspec_schemaorg.models.place.AdministrativeArea import AdministrativeArea
from datetime import date
from typing import Optional, Union, Dict, List, Any


class Legislation(CreativeWork):
    """A legal document such as an act, decree, bill, etc. (enforceable or not) or a component of a legal act (like an article)."""
    type: str = field(default_factory=lambda: "Legislation", name="@type")
    legislationIdentifier: 'URL' | str | None = None
    legislationJurisdiction: str | 'AdministrativeArea' | None = None
    legislationEnsuresImplementationOf: 'Legislation' | None = None
    jurisdiction: str | 'AdministrativeArea' | None = None
    legislationRepeals: 'Legislation' | None = None
    legislationConsolidates: 'Legislation' | None = None
    legislationChanges: 'Legislation' | None = None
    legislationCommences: 'Legislation' | None = None
    legislationTransposes: 'Legislation' | None = None
    legislationResponsible: 'Organization' | 'Person' | None = None
    legislationCorrects: 'Legislation' | None = None
    legislationDate: date | None = None
    legislationApplies: 'Legislation' | None = None
    legislationDateOfApplicability: date | None = None
    legislationType: str | 'CategoryCode' | None = None
    legislationAmends: 'Legislation' | None = None
    legislationCountersignedBy: 'Organization' | 'Person' | None = None
    legislationLegalForce: 'LegalForceStatus' | None = None
    legislationPassedBy: 'Organization' | 'Person' | None = None
    legislationDateVersion: date | None = None