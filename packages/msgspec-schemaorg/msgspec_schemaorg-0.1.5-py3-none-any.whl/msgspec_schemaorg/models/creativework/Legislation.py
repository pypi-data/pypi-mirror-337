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
    legislationIdentifier: Union[List[Union['URL', str]], Union['URL', str], None] = None
    legislationJurisdiction: Union[List[Union[str, 'AdministrativeArea']], Union[str, 'AdministrativeArea'], None] = None
    legislationEnsuresImplementationOf: Union[List['Legislation'], 'Legislation', None] = None
    jurisdiction: Union[List[Union[str, 'AdministrativeArea']], Union[str, 'AdministrativeArea'], None] = None
    legislationRepeals: Union[List['Legislation'], 'Legislation', None] = None
    legislationConsolidates: Union[List['Legislation'], 'Legislation', None] = None
    legislationChanges: Union[List['Legislation'], 'Legislation', None] = None
    legislationCommences: Union[List['Legislation'], 'Legislation', None] = None
    legislationTransposes: Union[List['Legislation'], 'Legislation', None] = None
    legislationResponsible: Union[List[Union['Organization', 'Person']], Union['Organization', 'Person'], None] = None
    legislationCorrects: Union[List['Legislation'], 'Legislation', None] = None
    legislationDate: Union[List[date], date, None] = None
    legislationApplies: Union[List['Legislation'], 'Legislation', None] = None
    legislationDateOfApplicability: Union[List[date], date, None] = None
    legislationType: Union[List[Union[str, 'CategoryCode']], Union[str, 'CategoryCode'], None] = None
    legislationAmends: Union[List['Legislation'], 'Legislation', None] = None
    legislationCountersignedBy: Union[List[Union['Organization', 'Person']], Union['Organization', 'Person'], None] = None
    legislationLegalForce: Union[List['LegalForceStatus'], 'LegalForceStatus', None] = None
    legislationPassedBy: Union[List[Union['Organization', 'Person']], Union['Organization', 'Person'], None] = None
    legislationDateVersion: Union[List[date], date, None] = None