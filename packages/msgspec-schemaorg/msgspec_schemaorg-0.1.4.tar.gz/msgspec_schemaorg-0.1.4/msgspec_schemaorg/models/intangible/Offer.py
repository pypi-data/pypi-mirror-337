from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Intangible import Intangible
from msgspec_schemaorg.utils import parse_iso8601
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
    from msgspec_schemaorg.models.creativework.Review import Review
    from msgspec_schemaorg.models.event.Event import Event
    from msgspec_schemaorg.models.intangible.AdultOrientedEnumeration import AdultOrientedEnumeration
    from msgspec_schemaorg.models.intangible.AggregateOffer import AggregateOffer
    from msgspec_schemaorg.models.intangible.AggregateRating import AggregateRating
    from msgspec_schemaorg.models.intangible.BusinessEntityType import BusinessEntityType
    from msgspec_schemaorg.models.intangible.BusinessFunction import BusinessFunction
    from msgspec_schemaorg.models.intangible.CategoryCode import CategoryCode
    from msgspec_schemaorg.models.intangible.DeliveryMethod import DeliveryMethod
    from msgspec_schemaorg.models.intangible.Duration import Duration
    from msgspec_schemaorg.models.intangible.GeoShape import GeoShape
    from msgspec_schemaorg.models.intangible.ItemAvailability import ItemAvailability
    from msgspec_schemaorg.models.intangible.LoanOrCredit import LoanOrCredit
    from msgspec_schemaorg.models.intangible.MemberProgramTier import MemberProgramTier
    from msgspec_schemaorg.models.intangible.MenuItem import MenuItem
    from msgspec_schemaorg.models.intangible.MerchantReturnPolicy import MerchantReturnPolicy
    from msgspec_schemaorg.models.intangible.Offer import Offer
    from msgspec_schemaorg.models.intangible.OfferItemCondition import OfferItemCondition
    from msgspec_schemaorg.models.intangible.OfferShippingDetails import OfferShippingDetails
    from msgspec_schemaorg.models.intangible.PaymentMethod import PaymentMethod
    from msgspec_schemaorg.models.intangible.PhysicalActivityCategory import PhysicalActivityCategory
    from msgspec_schemaorg.models.intangible.PriceSpecification import PriceSpecification
    from msgspec_schemaorg.models.intangible.PropertyValue import PropertyValue
    from msgspec_schemaorg.models.intangible.QuantitativeValue import QuantitativeValue
    from msgspec_schemaorg.models.intangible.Service import Service
    from msgspec_schemaorg.models.intangible.Trip import Trip
    from msgspec_schemaorg.models.intangible.TypeAndQuantityNode import TypeAndQuantityNode
    from msgspec_schemaorg.models.intangible.WarrantyPromise import WarrantyPromise
    from msgspec_schemaorg.models.organization.Organization import Organization
    from msgspec_schemaorg.models.person.Person import Person
    from msgspec_schemaorg.models.place.AdministrativeArea import AdministrativeArea
    from msgspec_schemaorg.models.place.Place import Place
    from msgspec_schemaorg.models.product.Product import Product
    from msgspec_schemaorg.models.thing.Thing import Thing
from datetime import date, datetime, time
from typing import Optional, Union, Dict, List, Any


class Offer(Intangible):
    """An offer to transfer some rights to an item or to provide a service — for example, an offer to sell tickets to an event, to rent the DVD of a movie, to stream a TV show over the internet, to repair a motorcycle, or to loan a book.\\n\\nNote: As the [[businessFunction]] property, which identifies the form of offer (e.g. sell, lease, repair, dispose), defaults to http://purl.org/goodrelations/v1#Sell; an Offer without a defined businessFunction value can be assumed to be an offer to sell.\\n\\nFor [GTIN](http://www.gs1.org/barcodes/technical/idkeys/gtin)-related fields, see [Check Digit calculator](http://www.gs1.org/barcodes/support/check_digit_calculator) and [validation guide](http://www.gs1us.org/resources/standards/gtin-validation-guide) from [GS1](http://www.gs1.org/)."""
    type: str = field(default_factory=lambda: "Offer", name="@type")
    priceValidUntil: date | None = None
    aggregateRating: 'AggregateRating' | None = None
    eligibleQuantity: 'QuantitativeValue' | None = None
    eligibleRegion: str | 'GeoShape' | 'Place' | None = None
    availabilityStarts: datetime | time | date | None = None
    sku: str | None = None
    priceSpecification: 'PriceSpecification' | None = None
    eligibleCustomerType: 'BusinessEntityType' | None = None
    hasMerchantReturnPolicy: 'MerchantReturnPolicy' | None = None
    validForMemberTier: 'MemberProgramTier' | None = None
    availability: 'ItemAvailability' | None = None
    inventoryLevel: 'QuantitativeValue' | None = None
    eligibleDuration: 'QuantitativeValue' | None = None
    shippingDetails: 'OfferShippingDetails' | None = None
    mpn: str | None = None
    hasGS1DigitalLink: 'URL' | None = None
    serialNumber: str | None = None
    reviews: 'Review' | None = None
    gtin12: str | None = None
    leaseLength: 'QuantitativeValue' | 'Duration' | None = None
    gtin13: str | None = None
    hasMeasurement: 'QuantitativeValue' | None = None
    deliveryLeadTime: 'QuantitativeValue' | None = None
    seller: 'Person' | 'Organization' | None = None
    advanceBookingRequirement: 'QuantitativeValue' | None = None
    gtin: 'URL' | str | None = None
    price: int | float | str | None = None
    validFrom: datetime | date | None = None
    mobileUrl: str | None = None
    category: 'URL' | str | 'CategoryCode' | 'Thing' | 'PhysicalActivityCategory' | None = None
    asin: 'URL' | str | None = None
    addOn: 'Offer' | None = None
    availableDeliveryMethod: 'DeliveryMethod' | None = None
    offeredBy: 'Person' | 'Organization' | None = None
    validThrough: datetime | date | None = None
    isFamilyFriendly: bool | None = None
    warranty: 'WarrantyPromise' | None = None
    hasAdultConsideration: 'AdultOrientedEnumeration' | None = None
    businessFunction: 'BusinessFunction' | None = None
    additionalProperty: 'PropertyValue' | None = None
    eligibleTransactionVolume: 'PriceSpecification' | None = None
    review: 'Review' | None = None
    itemCondition: 'OfferItemCondition' | None = None
    includesObject: 'TypeAndQuantityNode' | None = None
    priceCurrency: str | None = None
    ineligibleRegion: str | 'GeoShape' | 'Place' | None = None
    gtin14: str | None = None
    areaServed: str | 'AdministrativeArea' | 'GeoShape' | 'Place' | None = None
    checkoutPageURLTemplate: str | None = None
    acceptedPaymentMethod: str | 'PaymentMethod' | 'LoanOrCredit' | None = None
    gtin8: str | None = None
    availableAtOrFrom: 'Place' | None = None
    itemOffered: 'Trip' | 'Product' | 'AggregateOffer' | 'MenuItem' | 'Service' | 'Event' | 'CreativeWork' | None = None
    availabilityEnds: datetime | date | time | None = None