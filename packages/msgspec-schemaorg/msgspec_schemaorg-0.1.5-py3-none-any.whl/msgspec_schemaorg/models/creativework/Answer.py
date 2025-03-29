from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.Comment import Comment
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.Comment import Comment
    from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
    from msgspec_schemaorg.models.creativework.WebContent import WebContent
from typing import Optional, Union, Dict, List, Any


class Answer(Comment):
    """An answer offered to a question; perhaps correct, perhaps opinionated or wrong."""
    type: str = field(default_factory=lambda: "Answer", name="@type")
    answerExplanation: Union[List[Union['Comment', 'WebContent']], Union['Comment', 'WebContent'], None] = None
    parentItem: Union[List[Union['CreativeWork', 'Comment']], Union['CreativeWork', 'Comment'], None] = None