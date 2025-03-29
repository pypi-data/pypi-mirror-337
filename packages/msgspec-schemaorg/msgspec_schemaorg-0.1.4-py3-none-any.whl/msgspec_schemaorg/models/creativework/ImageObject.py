from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.MediaObject import MediaObject
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.MediaObject import MediaObject
    from msgspec_schemaorg.models.intangible.PropertyValue import PropertyValue
from typing import Optional, Union, Dict, List, Any


class ImageObject(MediaObject):
    """An image file."""
    type: str = field(default_factory=lambda: "ImageObject", name="@type")
    embeddedTextCaption: str | None = None
    caption: str | 'MediaObject' | None = None
    representativeOfPage: bool | None = None
    exifData: str | 'PropertyValue' | None = None