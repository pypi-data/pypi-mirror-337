from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Intangible import Intangible
from msgspec_schemaorg.utils import parse_iso8601
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.EducationalOccupationalCredential import EducationalOccupationalCredential
    from msgspec_schemaorg.models.intangible.CategoryCode import CategoryCode
    from msgspec_schemaorg.models.intangible.ContactPoint import ContactPoint
    from msgspec_schemaorg.models.intangible.DefinedTerm import DefinedTerm
    from msgspec_schemaorg.models.intangible.MonetaryAmount import MonetaryAmount
    from msgspec_schemaorg.models.intangible.MonetaryAmountDistribution import MonetaryAmountDistribution
    from msgspec_schemaorg.models.intangible.Occupation import Occupation
    from msgspec_schemaorg.models.intangible.OccupationalExperienceRequirements import OccupationalExperienceRequirements
    from msgspec_schemaorg.models.intangible.PriceSpecification import PriceSpecification
    from msgspec_schemaorg.models.organization.Organization import Organization
    from msgspec_schemaorg.models.person.Person import Person
    from msgspec_schemaorg.models.place.AdministrativeArea import AdministrativeArea
    from msgspec_schemaorg.models.place.Place import Place
from datetime import date, datetime
from typing import Optional, Union, Dict, List, Any


class JobPosting(Intangible):
    """A listing that describes a job opening in a certain organization."""
    type: str = field(default_factory=lambda: "JobPosting", name="@type")
    physicalRequirement: 'URL' | str | 'DefinedTerm' | None = None
    applicationContact: 'ContactPoint' | None = None
    responsibilities: str | None = None
    educationRequirements: str | 'EducationalOccupationalCredential' | None = None
    benefits: str | None = None
    skills: str | 'DefinedTerm' | None = None
    employmentType: str | None = None
    experienceInPlaceOfEducation: bool | None = None
    workHours: str | None = None
    datePosted: datetime | date | None = None
    applicantLocationRequirements: 'AdministrativeArea' | None = None
    securityClearanceRequirement: 'URL' | str | None = None
    occupationalCategory: str | 'CategoryCode' | None = None
    employmentUnit: 'Organization' | None = None
    jobImmediateStart: bool | None = None
    directApply: bool | None = None
    jobStartDate: date | str | None = None
    qualifications: str | 'EducationalOccupationalCredential' | None = None
    specialCommitments: str | None = None
    incentiveCompensation: str | None = None
    baseSalary: int | float | 'PriceSpecification' | 'MonetaryAmount' | None = None
    jobBenefits: str | None = None
    validThrough: datetime | date | None = None
    estimatedSalary: int | float | 'MonetaryAmountDistribution' | 'MonetaryAmount' | None = None
    totalJobOpenings: int | None = None
    hiringOrganization: 'Organization' | 'Person' | None = None
    relevantOccupation: 'Occupation' | None = None
    experienceRequirements: str | 'OccupationalExperienceRequirements' | None = None
    jobLocationType: str | None = None
    eligibilityToWorkRequirement: str | None = None
    jobLocation: 'Place' | None = None
    sensoryRequirement: 'URL' | str | 'DefinedTerm' | None = None
    employerOverview: str | None = None
    incentives: str | None = None
    title: str | None = None
    industry: str | 'DefinedTerm' | None = None
    salaryCurrency: str | None = None