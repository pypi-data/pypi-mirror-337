from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Enumeration import Enumeration
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


class QualitativeValue(Enumeration):
    """A predefined value for a product characteristic, e.g. the power cord plug type 'US' or the garment sizes 'S', 'M', 'L', and 'XL'."""
    type: str = field(default_factory=lambda: "QualitativeValue", name="@type")
    valueReference: str | 'PropertyValue' | 'MeasurementTypeEnumeration' | 'DefinedTerm' | 'QuantitativeValue' | 'Enumeration' | 'StructuredValue' | 'QualitativeValue' | None = None
    lesser: 'QualitativeValue' | None = None
    greater: 'QualitativeValue' | None = None
    equal: 'QualitativeValue' | None = None
    lesserOrEqual: 'QualitativeValue' | None = None
    greaterOrEqual: 'QualitativeValue' | None = None
    additionalProperty: 'PropertyValue' | None = None
    nonEqual: 'QualitativeValue' | None = None