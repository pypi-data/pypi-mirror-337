from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
from msgspec_schemaorg.utils import parse_iso8601
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.DataCatalog import DataCatalog
    from msgspec_schemaorg.models.creativework.DataDownload import DataDownload
    from msgspec_schemaorg.models.intangible.DefinedTerm import DefinedTerm
    from msgspec_schemaorg.models.intangible.MeasurementMethodEnum import MeasurementMethodEnum
    from msgspec_schemaorg.models.intangible.Property import Property
    from msgspec_schemaorg.models.intangible.PropertyValue import PropertyValue
    from msgspec_schemaorg.models.intangible.StatisticalVariable import StatisticalVariable
from datetime import datetime
from typing import Optional, Union, Dict, List, Any


class Dataset(CreativeWork):
    """A body of structured information describing some topic(s) of interest."""
    type: str = field(default_factory=lambda: "Dataset", name="@type")
    distribution: 'DataDownload' | None = None
    catalog: 'DataCatalog' | None = None
    includedDataCatalog: 'DataCatalog' | None = None
    includedInDataCatalog: 'DataCatalog' | None = None
    measurementTechnique: 'URL' | str | 'DefinedTerm' | 'MeasurementMethodEnum' | None = None
    measurementMethod: 'URL' | str | 'DefinedTerm' | 'MeasurementMethodEnum' | None = None
    datasetTimeInterval: datetime | None = None
    issn: str | None = None
    variableMeasured: str | 'Property' | 'StatisticalVariable' | 'PropertyValue' | None = None