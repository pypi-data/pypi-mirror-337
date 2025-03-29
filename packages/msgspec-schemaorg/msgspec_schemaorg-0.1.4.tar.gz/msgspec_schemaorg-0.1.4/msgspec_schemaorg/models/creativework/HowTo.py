from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
    from msgspec_schemaorg.models.intangible.Duration import Duration
    from msgspec_schemaorg.models.intangible.HowToSection import HowToSection
    from msgspec_schemaorg.models.intangible.HowToStep import HowToStep
    from msgspec_schemaorg.models.intangible.HowToSupply import HowToSupply
    from msgspec_schemaorg.models.intangible.HowToTool import HowToTool
    from msgspec_schemaorg.models.intangible.ItemList import ItemList
    from msgspec_schemaorg.models.intangible.MonetaryAmount import MonetaryAmount
    from msgspec_schemaorg.models.intangible.QuantitativeValue import QuantitativeValue
from typing import Optional, Union, Dict, List, Any


class HowTo(CreativeWork):
    """Instructions that explain how to achieve a result by performing a sequence of steps."""
    type: str = field(default_factory=lambda: "HowTo", name="@type")
    steps: str | 'ItemList' | 'CreativeWork' | None = None
    yield_: str | 'QuantitativeValue' | None = None
    tool: str | 'HowToTool' | None = None
    step: str | 'CreativeWork' | 'HowToSection' | 'HowToStep' | None = None
    estimatedCost: str | 'MonetaryAmount' | None = None
    prepTime: 'Duration' | None = None
    performTime: 'Duration' | None = None
    totalTime: 'Duration' | None = None
    supply: str | 'HowToSupply' | None = None