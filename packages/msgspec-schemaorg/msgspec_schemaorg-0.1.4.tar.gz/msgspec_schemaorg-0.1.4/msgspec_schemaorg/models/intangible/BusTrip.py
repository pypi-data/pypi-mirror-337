from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Trip import Trip
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.place.BusStation import BusStation
    from msgspec_schemaorg.models.place.BusStop import BusStop
from typing import Optional, Union, Dict, List, Any


class BusTrip(Trip):
    """A trip on a commercial bus line."""
    type: str = field(default_factory=lambda: "BusTrip", name="@type")
    departureBusStop: 'BusStation' | 'BusStop' | None = None
    arrivalBusStop: 'BusStation' | 'BusStop' | None = None
    busNumber: str | None = None
    busName: str | None = None