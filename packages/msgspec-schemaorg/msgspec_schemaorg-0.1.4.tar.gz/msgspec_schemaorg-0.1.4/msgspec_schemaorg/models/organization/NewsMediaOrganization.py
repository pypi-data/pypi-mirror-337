from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.organization.Organization import Organization
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.AboutPage import AboutPage
    from msgspec_schemaorg.models.creativework.Article import Article
    from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
from typing import Optional, Union, Dict, List, Any


class NewsMediaOrganization(Organization):
    """A News/Media organization such as a newspaper or TV station."""
    type: str = field(default_factory=lambda: "NewsMediaOrganization", name="@type")
    unnamedSourcesPolicy: 'URL' | 'CreativeWork' | None = None
    missionCoveragePrioritiesPolicy: 'URL' | 'CreativeWork' | None = None
    ownershipFundingInfo: 'URL' | str | 'AboutPage' | 'CreativeWork' | None = None
    verificationFactCheckingPolicy: 'URL' | 'CreativeWork' | None = None
    diversityPolicy: 'URL' | 'CreativeWork' | None = None
    correctionsPolicy: 'URL' | 'CreativeWork' | None = None
    noBylinesPolicy: 'URL' | 'CreativeWork' | None = None
    diversityStaffingReport: 'URL' | 'Article' | None = None
    ethicsPolicy: 'URL' | 'CreativeWork' | None = None
    actionableFeedbackPolicy: 'URL' | 'CreativeWork' | None = None
    masthead: 'URL' | 'CreativeWork' | None = None