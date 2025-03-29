from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.PublicationIssue import PublicationIssue
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.person.Person import Person
from typing import Optional, Union, Dict, List, Any


class ComicIssue(PublicationIssue):
    """Individual comic issues are serially published as
    	part of a larger series. For the sake of consistency, even one-shot issues
    	belong to a series comprised of a single issue. All comic issues can be
    	uniquely identified by: the combination of the name and volume number of the
    	series to which the issue belongs; the issue number; and the variant
    	description of the issue (if any)."""
    type: str = field(default_factory=lambda: "ComicIssue", name="@type")
    inker: 'Person' | None = None
    artist: 'Person' | None = None
    letterer: 'Person' | None = None
    colorist: 'Person' | None = None
    penciler: 'Person' | None = None
    variantCover: str | None = None