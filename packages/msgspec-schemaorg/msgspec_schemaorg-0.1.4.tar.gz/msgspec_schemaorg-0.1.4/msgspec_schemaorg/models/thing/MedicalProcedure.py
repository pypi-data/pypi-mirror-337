from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.thing.MedicalEntity import MedicalEntity
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.EventStatusType import EventStatusType
    from msgspec_schemaorg.models.intangible.MedicalProcedureType import MedicalProcedureType
    from msgspec_schemaorg.models.intangible.MedicalStudyStatus import MedicalStudyStatus
    from msgspec_schemaorg.models.thing.MedicalEntity import MedicalEntity
from typing import Optional, Union, Dict, List, Any


class MedicalProcedure(MedicalEntity):
    """A process of care used in either a diagnostic, therapeutic, preventive or palliative capacity that relies on invasive (surgical), non-invasive, or other techniques."""
    type: str = field(default_factory=lambda: "MedicalProcedure", name="@type")
    howPerformed: str | None = None
    followup: str | None = None
    bodyLocation: str | None = None
    preparation: str | 'MedicalEntity' | None = None
    status: str | 'EventStatusType' | 'MedicalStudyStatus' | None = None
    procedureType: 'MedicalProcedureType' | None = None