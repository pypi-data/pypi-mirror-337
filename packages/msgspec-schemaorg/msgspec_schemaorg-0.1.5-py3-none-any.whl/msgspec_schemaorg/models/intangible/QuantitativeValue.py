from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.StructuredValue import StructuredValue
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.DefinedTerm import DefinedTerm
    from msgspec_schemaorg.models.intangible.Enumeration import Enumeration
    from msgspec_schemaorg.models.intangible.MeasurementTypeEnumeration import MeasurementTypeEnumeration
    from msgspec_schemaorg.models.intangible.PropertyValue import PropertyValue
    from msgspec_schemaorg.models.intangible.QualitativeValue import QualitativeValue
    from msgspec_schemaorg.models.intangible.QuantitativeValue import QuantitativeValue
    from msgspec_schemaorg.models.intangible.StructuredValue import StructuredValue
from typing import Optional, Union, Dict, List, Any


class QuantitativeValue(StructuredValue):
    """ A point value or interval for product characteristics and other purposes."""
    type: str = field(default_factory=lambda: "QuantitativeValue", name="@type")
    maxValue: Union[List[int | float], int | float, None] = None
    valueReference: Union[List[Union[str, 'PropertyValue', 'MeasurementTypeEnumeration', 'DefinedTerm', 'QuantitativeValue', 'Enumeration', 'StructuredValue', 'QualitativeValue']], Union[str, 'PropertyValue', 'MeasurementTypeEnumeration', 'DefinedTerm', 'QuantitativeValue', 'Enumeration', 'StructuredValue', 'QualitativeValue'], None] = None
    unitText: Union[List[str], str, None] = None
    value: Union[List[Union[int | float, bool, str, 'StructuredValue']], Union[int | float, bool, str, 'StructuredValue'], None] = None
    additionalProperty: Union[List['PropertyValue'], 'PropertyValue', None] = None
    unitCode: Union[List[Union['URL', str]], Union['URL', str], None] = None
    minValue: Union[List[int | float], int | float, None] = None