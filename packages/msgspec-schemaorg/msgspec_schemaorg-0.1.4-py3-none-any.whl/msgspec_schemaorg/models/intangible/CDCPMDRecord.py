from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.StructuredValue import StructuredValue
from msgspec_schemaorg.utils import parse_iso8601
from datetime import date, datetime
from typing import Optional, Union, Dict, List, Any


class CDCPMDRecord(StructuredValue):
    """A CDCPMDRecord is a data structure representing a record in a CDC tabular data format
      used for hospital data reporting. See [documentation](/docs/cdc-covid.html) for details, and the linked CDC materials for authoritative
      definitions used as the source here.
      """
    type: str = field(default_factory=lambda: "CDCPMDRecord", name="@type")
    cvdNumTotBeds: int | float | None = None
    datePosted: datetime | date | None = None
    cvdFacilityCounty: str | None = None
    cvdNumICUBedsOcc: int | float | None = None
    cvdFacilityId: str | None = None
    cvdNumC19HospPats: int | float | None = None
    cvdNumBedsOcc: int | float | None = None
    cvdNumVentUse: int | float | None = None
    cvdNumBeds: int | float | None = None
    cvdNumC19Died: int | float | None = None
    cvdNumICUBeds: int | float | None = None
    cvdNumC19HOPats: int | float | None = None
    cvdNumC19OverflowPats: int | float | None = None
    cvdCollectionDate: datetime | str | None = None
    cvdNumVent: int | float | None = None
    cvdNumC19OFMechVentPats: int | float | None = None
    cvdNumC19MechVentPats: int | float | None = None