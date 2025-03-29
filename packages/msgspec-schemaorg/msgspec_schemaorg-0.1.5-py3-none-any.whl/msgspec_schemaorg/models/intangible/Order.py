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
    paymentMethod: Union[List[Union[str, 'PaymentMethod']], Union[str, 'PaymentMethod'], None] = None
    billingAddress: Union[List['PostalAddress'], 'PostalAddress', None] = None
    broker: Union[List[Union['Person', 'Organization']], Union['Person', 'Organization'], None] = None
    merchant: Union[List[Union['Person', 'Organization']], Union['Person', 'Organization'], None] = None
    paymentDueDate: Union[List[Union[datetime, date]], Union[datetime, date], None] = None
    seller: Union[List[Union['Person', 'Organization']], Union['Person', 'Organization'], None] = None
    isGift: Union[List[bool], bool, None] = None
    orderStatus: Union[List['OrderStatus'], 'OrderStatus', None] = None
    acceptedOffer: Union[List['Offer'], 'Offer', None] = None
    orderNumber: Union[List[str], str, None] = None
    orderDate: Union[List[Union[datetime, date]], Union[datetime, date], None] = None
    customer: Union[List[Union['Person', 'Organization']], Union['Person', 'Organization'], None] = None
    paymentMethodId: Union[List[str], str, None] = None
    orderDelivery: Union[List['ParcelDelivery'], 'ParcelDelivery', None] = None
    discountCode: Union[List[str], str, None] = None
    discountCurrency: Union[List[str], str, None] = None
    partOfInvoice: Union[List['Invoice'], 'Invoice', None] = None
    orderedItem: Union[List[Union['Product', 'OrderItem', 'Service']], Union['Product', 'OrderItem', 'Service'], None] = None
    paymentDue: Union[List[datetime], datetime, None] = None
    discount: Union[List[Union[int | float, str]], Union[int | float, str], None] = None
    confirmationNumber: Union[List[str], str, None] = None
    paymentUrl: Union[List['URL'], 'URL', None] = None