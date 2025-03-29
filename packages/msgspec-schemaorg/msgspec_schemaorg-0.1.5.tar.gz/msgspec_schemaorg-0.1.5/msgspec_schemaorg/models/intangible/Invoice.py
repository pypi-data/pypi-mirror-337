from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Intangible import Intangible
from msgspec_schemaorg.utils import parse_iso8601
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.CategoryCode import CategoryCode
    from msgspec_schemaorg.models.intangible.Duration import Duration
    from msgspec_schemaorg.models.intangible.MonetaryAmount import MonetaryAmount
    from msgspec_schemaorg.models.intangible.Order import Order
    from msgspec_schemaorg.models.intangible.PaymentMethod import PaymentMethod
    from msgspec_schemaorg.models.intangible.PaymentStatusType import PaymentStatusType
    from msgspec_schemaorg.models.intangible.PhysicalActivityCategory import PhysicalActivityCategory
    from msgspec_schemaorg.models.intangible.PriceSpecification import PriceSpecification
    from msgspec_schemaorg.models.organization.Organization import Organization
    from msgspec_schemaorg.models.person.Person import Person
    from msgspec_schemaorg.models.thing.Thing import Thing
from datetime import date, datetime
from typing import Optional, Union, Dict, List, Any


class Invoice(Intangible):
    """A statement of the money due for goods or services; a bill."""
    type: str = field(default_factory=lambda: "Invoice", name="@type")
    provider: Union[List[Union['Person', 'Organization']], Union['Person', 'Organization'], None] = None
    paymentMethod: Union[List[Union[str, 'PaymentMethod']], Union[str, 'PaymentMethod'], None] = None
    scheduledPaymentDate: Union[List[date], date, None] = None
    paymentStatus: Union[List[Union[str, 'PaymentStatusType']], Union[str, 'PaymentStatusType'], None] = None
    broker: Union[List[Union['Person', 'Organization']], Union['Person', 'Organization'], None] = None
    paymentDueDate: Union[List[Union[datetime, date]], Union[datetime, date], None] = None
    billingPeriod: Union[List['Duration'], 'Duration', None] = None
    referencesOrder: Union[List['Order'], 'Order', None] = None
    category: Union[List[Union['URL', str, 'CategoryCode', 'Thing', 'PhysicalActivityCategory']], Union['URL', str, 'CategoryCode', 'Thing', 'PhysicalActivityCategory'], None] = None
    totalPaymentDue: Union[List[Union['MonetaryAmount', 'PriceSpecification']], Union['MonetaryAmount', 'PriceSpecification'], None] = None
    customer: Union[List[Union['Person', 'Organization']], Union['Person', 'Organization'], None] = None
    paymentMethodId: Union[List[str], str, None] = None
    accountId: Union[List[str], str, None] = None
    paymentDue: Union[List[datetime], datetime, None] = None
    minimumPaymentDue: Union[List[Union['PriceSpecification', 'MonetaryAmount']], Union['PriceSpecification', 'MonetaryAmount'], None] = None
    confirmationNumber: Union[List[str], str, None] = None