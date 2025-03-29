from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.TechArticle import TechArticle
from typing import Optional, Union, Dict, List, Any


class APIReference(TechArticle):
    """Reference documentation for application programming interfaces (APIs)."""
    type: str = field(default_factory=lambda: "APIReference", name="@type")
    executableLibraryName: str | None = None
    programmingModel: str | None = None
    assemblyVersion: str | None = None
    targetPlatform: str | None = None
    assembly: str | None = None