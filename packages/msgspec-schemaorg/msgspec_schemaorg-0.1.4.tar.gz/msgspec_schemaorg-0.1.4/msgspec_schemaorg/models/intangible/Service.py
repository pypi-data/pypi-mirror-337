from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Intangible import Intangible
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.Certification import Certification
    from msgspec_schemaorg.models.creativework.ImageObject import ImageObject
    from msgspec_schemaorg.models.creativework.Review import Review
    from msgspec_schemaorg.models.intangible.AggregateRating import AggregateRating
    from msgspec_schemaorg.models.intangible.Audience import Audience
    from msgspec_schemaorg.models.intangible.Brand import Brand
    from msgspec_schemaorg.models.intangible.CategoryCode import CategoryCode
    from msgspec_schemaorg.models.intangible.Demand import Demand
    from msgspec_schemaorg.models.intangible.GeoShape import GeoShape
    from msgspec_schemaorg.models.intangible.GovernmentBenefitsType import GovernmentBenefitsType
    from msgspec_schemaorg.models.intangible.Offer import Offer
    from msgspec_schemaorg.models.intangible.OfferCatalog import OfferCatalog
    from msgspec_schemaorg.models.intangible.OpeningHoursSpecification import OpeningHoursSpecification
    from msgspec_schemaorg.models.intangible.PhysicalActivityCategory import PhysicalActivityCategory
    from msgspec_schemaorg.models.intangible.Service import Service
    from msgspec_schemaorg.models.intangible.ServiceChannel import ServiceChannel
    from msgspec_schemaorg.models.organization.Organization import Organization
    from msgspec_schemaorg.models.person.Person import Person
    from msgspec_schemaorg.models.place.AdministrativeArea import AdministrativeArea
    from msgspec_schemaorg.models.place.Place import Place
    from msgspec_schemaorg.models.product.Product import Product
    from msgspec_schemaorg.models.thing.Thing import Thing
from typing import Optional, Union, Dict, List, Any


class Service(Intangible):
    """A service provided by an organization, e.g. delivery service, print services, etc."""
    type: str = field(default_factory=lambda: "Service", name="@type")
    provider: 'Person' | 'Organization' | None = None
    aggregateRating: 'AggregateRating' | None = None
    hasCertification: 'Certification' | None = None
    isSimilarTo: 'Product' | 'Service' | None = None
    availableChannel: 'ServiceChannel' | None = None
    hoursAvailable: 'OpeningHoursSpecification' | None = None
    broker: 'Person' | 'Organization' | None = None
    serviceArea: 'GeoShape' | 'AdministrativeArea' | 'Place' | None = None
    isRelatedTo: 'Product' | 'Service' | None = None
    offers: 'Offer' | 'Demand' | None = None
    termsOfService: 'URL' | str | None = None
    category: 'URL' | str | 'CategoryCode' | 'Thing' | 'PhysicalActivityCategory' | None = None
    logo: 'URL' | 'ImageObject' | None = None
    award: str | None = None
    brand: 'Brand' | 'Organization' | None = None
    providerMobility: str | None = None
    audience: 'Audience' | None = None
    slogan: str | None = None
    review: 'Review' | None = None
    hasOfferCatalog: 'OfferCatalog' | None = None
    produces: 'Thing' | None = None
    areaServed: str | 'AdministrativeArea' | 'GeoShape' | 'Place' | None = None
    serviceAudience: 'Audience' | None = None
    serviceType: str | 'GovernmentBenefitsType' | None = None
    serviceOutput: 'Thing' | None = None