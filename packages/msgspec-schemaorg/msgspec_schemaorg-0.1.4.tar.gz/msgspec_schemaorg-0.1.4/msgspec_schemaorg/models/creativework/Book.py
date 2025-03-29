from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.BookFormatType import BookFormatType
    from msgspec_schemaorg.models.person.Person import Person
from typing import Optional, Union, Dict, List, Any


class Book(CreativeWork):
    """A book."""
    type: str = field(default_factory=lambda: "Book", name="@type")
    abridged: bool | None = None
    illustrator: 'Person' | None = None
    isbn: str | None = None
    bookEdition: str | None = None
    bookFormat: 'BookFormatType' | None = None
    numberOfPages: int | None = None