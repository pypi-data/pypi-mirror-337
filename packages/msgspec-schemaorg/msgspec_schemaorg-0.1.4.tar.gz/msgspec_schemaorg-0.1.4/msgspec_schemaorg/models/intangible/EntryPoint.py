from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Intangible import Intangible
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.SoftwareApplication import SoftwareApplication
    from msgspec_schemaorg.models.intangible.DigitalPlatformEnumeration import DigitalPlatformEnumeration
from typing import Optional, Union, Dict, List, Any


class EntryPoint(Intangible):
    """An entry point, within some Web-based protocol."""
    type: str = field(default_factory=lambda: "EntryPoint", name="@type")
    urlTemplate: str | None = None
    application: 'SoftwareApplication' | None = None
    contentType: str | None = None
    encodingType: str | None = None
    actionPlatform: 'URL' | str | 'DigitalPlatformEnumeration' | None = None
    actionApplication: 'SoftwareApplication' | None = None
    httpMethod: str | None = None