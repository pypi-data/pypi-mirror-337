from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Intangible import Intangible
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.thing.Thing import Thing
from typing import Optional, Union, Dict, List, Any


class PropertyValueSpecification(Intangible):
    """A Property value specification."""
    type: str = field(default_factory=lambda: "PropertyValueSpecification", name="@type")
    maxValue: int | float | None = None
    valueMinLength: int | float | None = None
    stepValue: int | float | None = None
    valueName: str | None = None
    valuePattern: str | None = None
    multipleValues: bool | None = None
    defaultValue: str | 'Thing' | None = None
    valueMaxLength: int | float | None = None
    valueRequired: bool | None = None
    readonlyValue: bool | None = None
    minValue: int | float | None = None