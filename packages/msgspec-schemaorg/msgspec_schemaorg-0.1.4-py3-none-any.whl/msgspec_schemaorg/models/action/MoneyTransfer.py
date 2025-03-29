from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.TransferAction import TransferAction
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.MonetaryAmount import MonetaryAmount
    from msgspec_schemaorg.models.place.BankOrCreditUnion import BankOrCreditUnion
from typing import Optional, Union, Dict, List, Any


class MoneyTransfer(TransferAction):
    """The act of transferring money from one place to another place. This may occur electronically or physically."""
    type: str = field(default_factory=lambda: "MoneyTransfer", name="@type")
    amount: int | float | 'MonetaryAmount' | None = None
    beneficiaryBank: str | 'BankOrCreditUnion' | None = None