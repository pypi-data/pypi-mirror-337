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
    provider: 'Person' | 'Organization' | None = None
    paymentMethod: str | 'PaymentMethod' | None = None
    scheduledPaymentDate: date | None = None
    paymentStatus: str | 'PaymentStatusType' | None = None
    broker: 'Person' | 'Organization' | None = None
    paymentDueDate: datetime | date | None = None
    billingPeriod: 'Duration' | None = None
    referencesOrder: 'Order' | None = None
    category: 'URL' | str | 'CategoryCode' | 'Thing' | 'PhysicalActivityCategory' | None = None
    totalPaymentDue: 'MonetaryAmount' | 'PriceSpecification' | None = None
    customer: 'Person' | 'Organization' | None = None
    paymentMethodId: str | None = None
    accountId: str | None = None
    paymentDue: datetime | None = None
    minimumPaymentDue: 'PriceSpecification' | 'MonetaryAmount' | None = None
    confirmationNumber: str | None = None