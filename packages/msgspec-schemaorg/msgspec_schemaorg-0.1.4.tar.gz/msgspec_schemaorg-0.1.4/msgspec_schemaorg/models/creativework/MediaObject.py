from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
from msgspec_schemaorg.utils import parse_iso8601
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.Claim import Claim
    from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
    from msgspec_schemaorg.models.creativework.NewsArticle import NewsArticle
    from msgspec_schemaorg.models.intangible.Distance import Distance
    from msgspec_schemaorg.models.intangible.Duration import Duration
    from msgspec_schemaorg.models.intangible.GeoShape import GeoShape
    from msgspec_schemaorg.models.intangible.MediaSubscription import MediaSubscription
    from msgspec_schemaorg.models.intangible.QuantitativeValue import QuantitativeValue
    from msgspec_schemaorg.models.organization.Organization import Organization
    from msgspec_schemaorg.models.place.Place import Place
from datetime import date, datetime, time
from typing import Optional, Union, Dict, List, Any


class MediaObject(CreativeWork):
    """A media object, such as an image, video, audio, or text object embedded in a web page or a downloadable dataset i.e. DataDownload. Note that a creative work may have many media objects associated with it on the same web page. For example, a page about a single song (MusicRecording) may have a music video (VideoObject), and a high and low bandwidth audio stream (2 AudioObject's)."""
    type: str = field(default_factory=lambda: "MediaObject", name="@type")
    contentUrl: 'URL' | None = None
    playerType: str | None = None
    startTime: datetime | time | None = None
    uploadDate: datetime | date | None = None
    requiresSubscription: bool | 'MediaSubscription' | None = None
    encodingFormat: 'URL' | str | None = None
    embedUrl: 'URL' | None = None
    sha256: str | None = None
    regionsAllowed: 'Place' | None = None
    duration: 'QuantitativeValue' | 'Duration' | None = None
    width: 'Distance' | 'QuantitativeValue' | None = None
    interpretedAsClaim: 'Claim' | None = None
    encodesCreativeWork: 'CreativeWork' | None = None
    associatedArticle: 'NewsArticle' | None = None
    endTime: datetime | time | None = None
    ineligibleRegion: str | 'GeoShape' | 'Place' | None = None
    productionCompany: 'Organization' | None = None
    height: 'Distance' | 'QuantitativeValue' | None = None
    bitrate: str | None = None
    contentSize: str | None = None