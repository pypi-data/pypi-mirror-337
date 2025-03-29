from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.thing.Thing import Thing
from msgspec_schemaorg.utils import parse_iso8601
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.Certification import Certification
    from msgspec_schemaorg.models.creativework.ImageObject import ImageObject
    from msgspec_schemaorg.models.creativework.Review import Review
    from msgspec_schemaorg.models.creativework.WebContent import WebContent
    from msgspec_schemaorg.models.intangible.AdultOrientedEnumeration import AdultOrientedEnumeration
    from msgspec_schemaorg.models.intangible.AggregateRating import AggregateRating
    from msgspec_schemaorg.models.intangible.Audience import Audience
    from msgspec_schemaorg.models.intangible.Brand import Brand
    from msgspec_schemaorg.models.intangible.CategoryCode import CategoryCode
    from msgspec_schemaorg.models.intangible.DefinedTerm import DefinedTerm
    from msgspec_schemaorg.models.intangible.Demand import Demand
    from msgspec_schemaorg.models.intangible.Distance import Distance
    from msgspec_schemaorg.models.intangible.EnergyConsumptionDetails import EnergyConsumptionDetails
    from msgspec_schemaorg.models.intangible.Grant import Grant
    from msgspec_schemaorg.models.intangible.ItemList import ItemList
    from msgspec_schemaorg.models.intangible.ListItem import ListItem
    from msgspec_schemaorg.models.intangible.Mass import Mass
    from msgspec_schemaorg.models.intangible.MerchantReturnPolicy import MerchantReturnPolicy
    from msgspec_schemaorg.models.intangible.Offer import Offer
    from msgspec_schemaorg.models.intangible.OfferItemCondition import OfferItemCondition
    from msgspec_schemaorg.models.intangible.PhysicalActivityCategory import PhysicalActivityCategory
    from msgspec_schemaorg.models.intangible.PropertyValue import PropertyValue
    from msgspec_schemaorg.models.intangible.QuantitativeValue import QuantitativeValue
    from msgspec_schemaorg.models.intangible.Service import Service
    from msgspec_schemaorg.models.intangible.SizeSpecification import SizeSpecification
    from msgspec_schemaorg.models.organization.Organization import Organization
    from msgspec_schemaorg.models.place.Country import Country
    from msgspec_schemaorg.models.product.Product import Product
    from msgspec_schemaorg.models.product.ProductGroup import ProductGroup
    from msgspec_schemaorg.models.product.ProductModel import ProductModel
    from msgspec_schemaorg.models.thing.Thing import Thing
from datetime import date
from typing import Optional, Union, Dict, List, Any


class Product(Thing):
    """Any offered product or service. For example: a pair of shoes; a concert ticket; the rental of a car; a haircut; or an episode of a TV show streamed online."""
    type: str = field(default_factory=lambda: "Product", name="@type")
    productID: str | None = None
    aggregateRating: 'AggregateRating' | None = None
    hasCertification: 'Certification' | None = None
    isSimilarTo: 'Product' | 'Service' | None = None
    colorSwatch: 'URL' | 'ImageObject' | None = None
    productionDate: date | None = None
    countryOfAssembly: str | None = None
    countryOfOrigin: 'Country' | None = None
    sku: str | None = None
    hasMerchantReturnPolicy: 'MerchantReturnPolicy' | None = None
    weight: 'QuantitativeValue' | 'Mass' | None = None
    mpn: str | None = None
    hasGS1DigitalLink: 'URL' | None = None
    model: str | 'ProductModel' | None = None
    isRelatedTo: 'Product' | 'Service' | None = None
    reviews: 'Review' | None = None
    gtin12: str | None = None
    pattern: str | 'DefinedTerm' | None = None
    offers: 'Offer' | 'Demand' | None = None
    keywords: 'URL' | str | 'DefinedTerm' | None = None
    negativeNotes: str | 'ListItem' | 'ItemList' | 'WebContent' | None = None
    gtin13: str | None = None
    hasMeasurement: 'QuantitativeValue' | None = None
    gtin: 'URL' | str | None = None
    funding: 'Grant' | None = None
    isConsumableFor: 'Product' | None = None
    mobileUrl: str | None = None
    category: 'URL' | str | 'CategoryCode' | 'Thing' | 'PhysicalActivityCategory' | None = None
    asin: 'URL' | str | None = None
    color: str | None = None
    countryOfLastProcessing: str | None = None
    logo: 'URL' | 'ImageObject' | None = None
    award: str | None = None
    isFamilyFriendly: bool | None = None
    releaseDate: date | None = None
    brand: 'Brand' | 'Organization' | None = None
    inProductGroupWithID: str | None = None
    manufacturer: 'Organization' | None = None
    awards: str | None = None
    width: 'Distance' | 'QuantitativeValue' | None = None
    hasAdultConsideration: 'AdultOrientedEnumeration' | None = None
    audience: 'Audience' | None = None
    material: 'URL' | str | 'Product' | None = None
    additionalProperty: 'PropertyValue' | None = None
    slogan: str | None = None
    depth: 'QuantitativeValue' | 'Distance' | None = None
    review: 'Review' | None = None
    itemCondition: 'OfferItemCondition' | None = None
    nsn: str | None = None
    positiveNotes: str | 'WebContent' | 'ItemList' | 'ListItem' | None = None
    size: str | 'QuantitativeValue' | 'DefinedTerm' | 'SizeSpecification' | None = None
    hasEnergyConsumptionDetails: 'EnergyConsumptionDetails' | None = None
    gtin14: str | None = None
    height: 'Distance' | 'QuantitativeValue' | None = None
    purchaseDate: date | None = None
    isVariantOf: 'ProductModel' | 'ProductGroup' | None = None
    gtin8: str | None = None
    isAccessoryOrSparePartFor: 'Product' | None = None