from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.StructuredValue import StructuredValue
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.DayOfWeek import DayOfWeek
    from msgspec_schemaorg.models.intangible.Duration import Duration
    from msgspec_schemaorg.models.intangible.OpeningHoursSpecification import OpeningHoursSpecification
    from msgspec_schemaorg.models.intangible.QuantitativeValue import QuantitativeValue
from datetime import time
from typing import Optional, Union, Dict, List, Any


class ServicePeriod(StructuredValue):
    """ServicePeriod represents a duration with some constraints about cutoff time and business days. This is used e.g. in shipping for handling times or transit time."""
    type: str = field(default_factory=lambda: "ServicePeriod", name="@type")
    businessDays: 'OpeningHoursSpecification' | 'DayOfWeek' | None = None
    cutoffTime: time | None = None
    duration: 'QuantitativeValue' | 'Duration' | None = None