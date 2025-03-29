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
    applicationSubCategory: Union[List[Union['URL', str]], Union['URL', str], None] = None
    countriesNotSupported: Union[List[str], str, None] = None
    downloadUrl: Union[List['URL'], 'URL', None] = None
    permissions: Union[List[str], str, None] = None
    featureList: Union[List[Union['URL', str]], Union['URL', str], None] = None
    softwareVersion: Union[List[str], str, None] = None
    fileSize: Union[List[str], str, None] = None
    operatingSystem: Union[List[str], str, None] = None
    applicationCategory: Union[List[Union['URL', str]], Union['URL', str], None] = None
    applicationSuite: Union[List[str], str, None] = None
    countriesSupported: Union[List[str], str, None] = None
    availableOnDevice: Union[List[str], str, None] = None
    device: Union[List[str], str, None] = None
    screenshot: Union[List[Union['URL', 'ImageObject']], Union['URL', 'ImageObject'], None] = None
    processorRequirements: Union[List[str], str, None] = None
    releaseNotes: Union[List[Union['URL', str]], Union['URL', str], None] = None
    softwareAddOn: Union[List['SoftwareApplication'], 'SoftwareApplication', None] = None
    requirements: Union[List[Union['URL', str]], Union['URL', str], None] = None
    installUrl: Union[List['URL'], 'URL', None] = None
    supportingData: Union[List['DataFeed'], 'DataFeed', None] = None
    memoryRequirements: Union[List[Union['URL', str]], Union['URL', str], None] = None
    softwareHelp: Union[List['CreativeWork'], 'CreativeWork', None] = None
    storageRequirements: Union[List[Union['URL', str]], Union['URL', str], None] = None
    softwareRequirements: Union[List[Union['URL', str]], Union['URL', str], None] = None