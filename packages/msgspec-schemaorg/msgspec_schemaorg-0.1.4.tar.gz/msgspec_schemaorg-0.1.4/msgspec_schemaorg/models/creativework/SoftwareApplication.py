from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
    from msgspec_schemaorg.models.creativework.DataFeed import DataFeed
    from msgspec_schemaorg.models.creativework.ImageObject import ImageObject
    from msgspec_schemaorg.models.creativework.SoftwareApplication import SoftwareApplication
from typing import Optional, Union, Dict, List, Any


class SoftwareApplication(CreativeWork):
    """A software application."""
    type: str = field(default_factory=lambda: "SoftwareApplication", name="@type")
    applicationSubCategory: 'URL' | str | None = None
    countriesNotSupported: str | None = None
    downloadUrl: 'URL' | None = None
    permissions: str | None = None
    featureList: 'URL' | str | None = None
    softwareVersion: str | None = None
    fileSize: str | None = None
    operatingSystem: str | None = None
    applicationCategory: 'URL' | str | None = None
    applicationSuite: str | None = None
    countriesSupported: str | None = None
    availableOnDevice: str | None = None
    device: str | None = None
    screenshot: 'URL' | 'ImageObject' | None = None
    processorRequirements: str | None = None
    releaseNotes: 'URL' | str | None = None
    softwareAddOn: 'SoftwareApplication' | None = None
    requirements: 'URL' | str | None = None
    installUrl: 'URL' | None = None
    supportingData: 'DataFeed' | None = None
    memoryRequirements: 'URL' | str | None = None
    softwareHelp: 'CreativeWork' | None = None
    storageRequirements: 'URL' | str | None = None
    softwareRequirements: 'URL' | str | None = None