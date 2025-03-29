from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Offer import Offer
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.Demand import Demand
    from msgspec_schemaorg.models.intangible.Offer import Offer
from typing import Optional, Union, Dict, List, Any


class AggregateOffer(Offer):
    """When a single product is associated with multiple offers (for example, the same pair of shoes is offered by different merchants), then AggregateOffer can be used.\\n\\nNote: AggregateOffers are normally expected to associate multiple offers that all share the same defined [[businessFunction]] value, or default to http://purl.org/goodrelations/v1#Sell if businessFunction is not explicitly defined."""
    type: str = field(default_factory=lambda: "AggregateOffer", name="@type")
    highPrice: int | float | str | None = None
    offers: 'Offer' | 'Demand' | None = None
    offerCount: int | None = None
    lowPrice: int | float | str | None = None