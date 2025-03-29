from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Intangible import Intangible
from msgspec_schemaorg.utils import parse_iso8601
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.Invoice import Invoice
    from msgspec_schemaorg.models.intangible.Offer import Offer
    from msgspec_schemaorg.models.intangible.OrderItem import OrderItem
    from msgspec_schemaorg.models.intangible.OrderStatus import OrderStatus
    from msgspec_schemaorg.models.intangible.ParcelDelivery import ParcelDelivery
    from msgspec_schemaorg.models.intangible.PaymentMethod import PaymentMethod
    from msgspec_schemaorg.models.intangible.PostalAddress import PostalAddress
    from msgspec_schemaorg.models.intangible.Service import Service
    from msgspec_schemaorg.models.organization.Organization import Organization
    from msgspec_schemaorg.models.person.Person import Person
    from msgspec_schemaorg.models.product.Product import Product
from datetime import date, datetime
from typing import Optional, Union, Dict, List, Any


class Order(Intangible):
    """An order is a confirmation of a transaction (a receipt), which can contain multiple line items, each represented by an Offer that has been accepted by the customer."""
    type: str = field(default_factory=lambda: "Order", name="@type")
    paymentMethod: str | 'PaymentMethod' | None = None
    billingAddress: 'PostalAddress' | None = None
    broker: 'Person' | 'Organization' | None = None
    merchant: 'Person' | 'Organization' | None = None
    paymentDueDate: datetime | date | None = None
    seller: 'Person' | 'Organization' | None = None
    isGift: bool | None = None
    orderStatus: 'OrderStatus' | None = None
    acceptedOffer: 'Offer' | None = None
    orderNumber: str | None = None
    orderDate: datetime | date | None = None
    customer: 'Person' | 'Organization' | None = None
    paymentMethodId: str | None = None
    orderDelivery: 'ParcelDelivery' | None = None
    discountCode: str | None = None
    discountCurrency: str | None = None
    partOfInvoice: 'Invoice' | None = None
    orderedItem: 'Product' | 'OrderItem' | 'Service' | None = None
    paymentDue: datetime | None = None
    discount: int | float | str | None = None
    confirmationNumber: str | None = None
    paymentUrl: 'URL' | None = None