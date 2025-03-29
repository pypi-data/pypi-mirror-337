from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.MediaObject import MediaObject
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.DefinedTerm import DefinedTerm
    from msgspec_schemaorg.models.intangible.MeasurementMethodEnum import MeasurementMethodEnum
from typing import Optional, Union, Dict, List, Any


class DataDownload(MediaObject):
    """All or part of a [[Dataset]] in downloadable form. """
    type: str = field(default_factory=lambda: "DataDownload", name="@type")
    measurementTechnique: 'URL' | str | 'DefinedTerm' | 'MeasurementMethodEnum' | None = None
    measurementMethod: 'URL' | str | 'DefinedTerm' | 'MeasurementMethodEnum' | None = None