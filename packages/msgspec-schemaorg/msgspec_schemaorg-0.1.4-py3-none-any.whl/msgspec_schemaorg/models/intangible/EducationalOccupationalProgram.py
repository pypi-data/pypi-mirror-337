from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Intangible import Intangible
from msgspec_schemaorg.utils import parse_iso8601
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.Course import Course
    from msgspec_schemaorg.models.creativework.EducationalOccupationalCredential import EducationalOccupationalCredential
    from msgspec_schemaorg.models.intangible.AlignmentObject import AlignmentObject
    from msgspec_schemaorg.models.intangible.CategoryCode import CategoryCode
    from msgspec_schemaorg.models.intangible.DayOfWeek import DayOfWeek
    from msgspec_schemaorg.models.intangible.DefinedTerm import DefinedTerm
    from msgspec_schemaorg.models.intangible.Demand import Demand
    from msgspec_schemaorg.models.intangible.Duration import Duration
    from msgspec_schemaorg.models.intangible.MonetaryAmountDistribution import MonetaryAmountDistribution
    from msgspec_schemaorg.models.intangible.Offer import Offer
    from msgspec_schemaorg.models.intangible.StructuredValue import StructuredValue
    from msgspec_schemaorg.models.organization.Organization import Organization
    from msgspec_schemaorg.models.person.Person import Person
from datetime import date, datetime
from typing import Optional, Union, Dict, List, Any


class EducationalOccupationalProgram(Intangible):
    """A program offered by an institution which determines the learning progress to achieve an outcome, usually a credential like a degree or certificate. This would define a discrete set of opportunities (e.g., job, courses) that together constitute a program with a clear start, end, set of requirements, and transition to a new occupational opportunity (e.g., a job), or sometimes a higher educational opportunity (e.g., an advanced degree)."""
    type: str = field(default_factory=lambda: "EducationalOccupationalProgram", name="@type")
    provider: 'Person' | 'Organization' | None = None
    endDate: datetime | date | None = None
    educationalCredentialAwarded: 'URL' | str | 'EducationalOccupationalCredential' | None = None
    trainingSalary: 'MonetaryAmountDistribution' | None = None
    salaryUponCompletion: 'MonetaryAmountDistribution' | None = None
    programPrerequisites: str | 'EducationalOccupationalCredential' | 'AlignmentObject' | 'Course' | None = None
    offers: 'Offer' | 'Demand' | None = None
    occupationalCategory: str | 'CategoryCode' | None = None
    programType: str | 'DefinedTerm' | None = None
    timeToComplete: 'Duration' | None = None
    numberOfCredits: int | 'StructuredValue' | None = None
    timeOfDay: str | None = None
    termsPerYear: int | float | None = None
    financialAidEligible: str | 'DefinedTerm' | None = None
    startDate: datetime | date | None = None
    dayOfWeek: 'DayOfWeek' | None = None
    occupationalCredentialAwarded: 'URL' | str | 'EducationalOccupationalCredential' | None = None
    educationalProgramMode: 'URL' | str | None = None
    hasCourse: 'Course' | None = None
    typicalCreditsPerTerm: int | 'StructuredValue' | None = None
    applicationStartDate: date | None = None
    maximumEnrollment: int | None = None
    applicationDeadline: date | str | None = None
    termDuration: 'Duration' | None = None