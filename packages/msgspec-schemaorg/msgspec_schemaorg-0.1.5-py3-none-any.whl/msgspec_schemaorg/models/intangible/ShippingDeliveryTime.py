from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.StructuredValue import StructuredValue
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.DayOfWeek import DayOfWeek
    from msgspec_schemaorg.models.intangible.OpeningHoursSpecification import OpeningHoursSpecification
    from msgspec_schemaorg.models.intangible.QuantitativeValue import QuantitativeValue
    from msgspec_schemaorg.models.intangible.ServicePeriod import ServicePeriod
from datetime import time
from typing import Optional, Union, Dict, List, Any


class ShippingDeliveryTime(StructuredValue):
    """ShippingDeliveryTime provides various pieces of information about delivery times for shipping."""
    type: str = field(default_factory=lambda: "ShippingDeliveryTime", name="@type")
    businessDays: Union[List[Union['OpeningHoursSpecification', 'DayOfWeek']], Union['OpeningHoursSpecification', 'DayOfWeek'], None] = None
    cutoffTime: Union[List[time], time, None] = None
    handlingTime: Union[List[Union['QuantitativeValue', 'ServicePeriod']], Union['QuantitativeValue', 'ServicePeriod'], None] = None
    transitTime: Union[List[Union['ServicePeriod', 'QuantitativeValue']], Union['ServicePeriod', 'QuantitativeValue'], None] = None