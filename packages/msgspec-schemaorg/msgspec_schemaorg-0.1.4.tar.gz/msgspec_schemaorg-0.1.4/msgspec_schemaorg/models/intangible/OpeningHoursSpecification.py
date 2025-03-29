from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.StructuredValue import StructuredValue
from msgspec_schemaorg.utils import parse_iso8601
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.DayOfWeek import DayOfWeek
from datetime import date, datetime, time
from typing import Optional, Union, Dict, List, Any


class OpeningHoursSpecification(StructuredValue):
    """A structured value providing information about the opening hours of a place or a certain service inside a place.\\n\\n
The place is __open__ if the [[opens]] property is specified, and __closed__ otherwise.\\n\\nIf the value for the [[closes]] property is less than the value for the [[opens]] property then the hour range is assumed to span over the next day.
      """
    type: str = field(default_factory=lambda: "OpeningHoursSpecification", name="@type")
    closes: time | None = None
    validFrom: datetime | date | None = None
    opens: time | None = None
    validThrough: datetime | date | None = None
    dayOfWeek: 'DayOfWeek' | None = None