from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.thing.Thing import Thing
from msgspec_schemaorg.utils import parse_iso8601
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.AboutPage import AboutPage
    from msgspec_schemaorg.models.creativework.Article import Article
    from msgspec_schemaorg.models.creativework.Certification import Certification
    from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
    from msgspec_schemaorg.models.creativework.EducationalOccupationalCredential import EducationalOccupationalCredential
    from msgspec_schemaorg.models.creativework.ImageObject import ImageObject
    from msgspec_schemaorg.models.creativework.Review import Review
    from msgspec_schemaorg.models.event.Event import Event
    from msgspec_schemaorg.models.intangible.AggregateRating import AggregateRating
    from msgspec_schemaorg.models.intangible.Brand import Brand
    from msgspec_schemaorg.models.intangible.ContactPoint import ContactPoint
    from msgspec_schemaorg.models.intangible.DefinedTerm import DefinedTerm
    from msgspec_schemaorg.models.intangible.Demand import Demand
    from msgspec_schemaorg.models.intangible.GeoShape import GeoShape
    from msgspec_schemaorg.models.intangible.Grant import Grant
    from msgspec_schemaorg.models.intangible.InteractionCounter import InteractionCounter
    from msgspec_schemaorg.models.intangible.Language import Language
    from msgspec_schemaorg.models.intangible.LoanOrCredit import LoanOrCredit
    from msgspec_schemaorg.models.intangible.MemberProgram import MemberProgram
    from msgspec_schemaorg.models.intangible.MemberProgramTier import MemberProgramTier
    from msgspec_schemaorg.models.intangible.MerchantReturnPolicy import MerchantReturnPolicy
    from msgspec_schemaorg.models.intangible.NonprofitType import NonprofitType
    from msgspec_schemaorg.models.intangible.Offer import Offer
    from msgspec_schemaorg.models.intangible.OfferCatalog import OfferCatalog
    from msgspec_schemaorg.models.intangible.OwnershipInfo import OwnershipInfo
    from msgspec_schemaorg.models.intangible.PaymentMethod import PaymentMethod
    from msgspec_schemaorg.models.intangible.PostalAddress import PostalAddress
    from msgspec_schemaorg.models.intangible.ProgramMembership import ProgramMembership
    from msgspec_schemaorg.models.intangible.QuantitativeValue import QuantitativeValue
    from msgspec_schemaorg.models.intangible.ShippingService import ShippingService
    from msgspec_schemaorg.models.intangible.VirtualLocation import VirtualLocation
    from msgspec_schemaorg.models.organization.Organization import Organization
    from msgspec_schemaorg.models.person.Person import Person
    from msgspec_schemaorg.models.place.AdministrativeArea import AdministrativeArea
    from msgspec_schemaorg.models.place.Place import Place
    from msgspec_schemaorg.models.product.Product import Product
    from msgspec_schemaorg.models.thing.Thing import Thing
from datetime import date
from typing import Optional, Union, Dict, List, Any


class Organization(Thing):
    """An organization such as a school, NGO, corporation, club, etc."""
    type: str = field(default_factory=lambda: "Organization", name="@type")
    event: 'Event' | None = None
    unnamedSourcesPolicy: 'URL' | 'CreativeWork' | None = None
    isicV4: str | None = None
    aggregateRating: 'AggregateRating' | None = None
    hasCertification: 'Certification' | None = None
    skills: str | 'DefinedTerm' | None = None
    publishingPrinciples: 'URL' | 'CreativeWork' | None = None
    hasPOS: 'Place' | None = None
    knowsAbout: 'URL' | str | 'Thing' | None = None
    telephone: str | None = None
    hasMerchantReturnPolicy: 'MerchantReturnPolicy' | None = None
    numberOfEmployees: 'QuantitativeValue' | None = None
    employees: 'Person' | None = None
    hasGS1DigitalLink: 'URL' | None = None
    ownershipFundingInfo: 'URL' | str | 'AboutPage' | 'CreativeWork' | None = None
    foundingLocation: 'Place' | None = None
    serviceArea: 'GeoShape' | 'AdministrativeArea' | 'Place' | None = None
    reviews: 'Review' | None = None
    seeks: 'Demand' | None = None
    nonprofitStatus: 'NonprofitType' | None = None
    parentOrganization: 'Organization' | None = None
    leiCode: str | None = None
    hasCredential: 'EducationalOccupationalCredential' | None = None
    founders: 'Person' | None = None
    keywords: 'URL' | str | 'DefinedTerm' | None = None
    vatID: str | None = None
    taxID: str | None = None
    location: str | 'Place' | 'VirtualLocation' | 'PostalAddress' | None = None
    funding: 'Grant' | None = None
    diversityPolicy: 'URL' | 'CreativeWork' | None = None
    foundingDate: date | None = None
    logo: 'URL' | 'ImageObject' | None = None
    employee: 'Person' | None = None
    contactPoints: 'ContactPoint' | None = None
    legalName: str | None = None
    alumni: 'Person' | None = None
    naics: str | None = None
    owns: 'Product' | 'OwnershipInfo' | None = None
    award: str | None = None
    brand: 'Brand' | 'Organization' | None = None
    knowsLanguage: str | 'Language' | None = None
    awards: str | None = None
    agentInteractionStatistic: 'InteractionCounter' | None = None
    iso6523Code: str | None = None
    funder: 'Person' | 'Organization' | None = None
    address: str | 'PostalAddress' | None = None
    slogan: str | None = None
    hasMemberProgram: 'MemberProgram' | None = None
    correctionsPolicy: 'URL' | 'CreativeWork' | None = None
    review: 'Review' | None = None
    interactionStatistic: 'InteractionCounter' | None = None
    globalLocationNumber: str | None = None
    makesOffer: 'Offer' | None = None
    department: 'Organization' | None = None
    sponsor: 'Organization' | 'Person' | None = None
    memberOf: 'Organization' | 'ProgramMembership' | 'MemberProgramTier' | None = None
    hasOfferCatalog: 'OfferCatalog' | None = None
    diversityStaffingReport: 'URL' | 'Article' | None = None
    duns: str | None = None
    ethicsPolicy: 'URL' | 'CreativeWork' | None = None
    actionableFeedbackPolicy: 'URL' | 'CreativeWork' | None = None
    areaServed: str | 'AdministrativeArea' | 'GeoShape' | 'Place' | None = None
    members: 'Organization' | 'Person' | None = None
    member: 'Person' | 'Organization' | None = None
    dissolutionDate: date | None = None
    acceptedPaymentMethod: str | 'PaymentMethod' | 'LoanOrCredit' | None = None
    founder: 'Person' | 'Organization' | None = None
    faxNumber: str | None = None
    contactPoint: 'ContactPoint' | None = None
    subOrganization: 'Organization' | None = None
    events: 'Event' | None = None
    hasShippingService: 'ShippingService' | None = None
    email: str | None = None