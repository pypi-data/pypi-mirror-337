from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Intangible import Intangible
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.OrderItem import OrderItem
    from msgspec_schemaorg.models.intangible.OrderStatus import OrderStatus
    from msgspec_schemaorg.models.intangible.ParcelDelivery import ParcelDelivery
    from msgspec_schemaorg.models.intangible.QuantitativeValue import QuantitativeValue
    from msgspec_schemaorg.models.intangible.Service import Service
    from msgspec_schemaorg.models.product.Product import Product
from typing import Optional, Union, Dict, List, Any


class OrderItem(Intangible):
    """An order item is a line of an order. It includes the quantity and shipping details of a bought offer."""
    type: str = field(default_factory=lambda: "OrderItem", name="@type")
    orderQuantity: int | float | 'QuantitativeValue' | None = None
    orderItemNumber: str | None = None
    orderDelivery: 'ParcelDelivery' | None = None
    orderItemStatus: 'OrderStatus' | None = None
    orderedItem: 'Product' | 'OrderItem' | 'Service' | None = None