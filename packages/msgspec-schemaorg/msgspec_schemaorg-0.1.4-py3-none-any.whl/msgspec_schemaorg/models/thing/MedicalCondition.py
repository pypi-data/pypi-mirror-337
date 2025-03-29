from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.thing.MedicalEntity import MedicalEntity
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.EventStatusType import EventStatusType
    from msgspec_schemaorg.models.intangible.MedicalStudyStatus import MedicalStudyStatus
    from msgspec_schemaorg.models.thing.AnatomicalStructure import AnatomicalStructure
    from msgspec_schemaorg.models.thing.AnatomicalSystem import AnatomicalSystem
    from msgspec_schemaorg.models.thing.DDxElement import DDxElement
    from msgspec_schemaorg.models.thing.Drug import Drug
    from msgspec_schemaorg.models.thing.MedicalConditionStage import MedicalConditionStage
    from msgspec_schemaorg.models.thing.MedicalRiskFactor import MedicalRiskFactor
    from msgspec_schemaorg.models.thing.MedicalSignOrSymptom import MedicalSignOrSymptom
    from msgspec_schemaorg.models.thing.MedicalTest import MedicalTest
    from msgspec_schemaorg.models.thing.MedicalTherapy import MedicalTherapy
    from msgspec_schemaorg.models.thing.SuperficialAnatomy import SuperficialAnatomy
from typing import Optional, Union, Dict, List, Any


class MedicalCondition(MedicalEntity):
    """Any condition of the human body that affects the normal functioning of a person, whether physically or mentally. Includes diseases, injuries, disabilities, disorders, syndromes, etc."""
    type: str = field(default_factory=lambda: "MedicalCondition", name="@type")
    expectedPrognosis: str | None = None
    associatedAnatomy: 'SuperficialAnatomy' | 'AnatomicalStructure' | 'AnatomicalSystem' | None = None
    possibleComplication: str | None = None
    signOrSymptom: 'MedicalSignOrSymptom' | None = None
    primaryPrevention: 'MedicalTherapy' | None = None
    riskFactor: 'MedicalRiskFactor' | None = None
    secondaryPrevention: 'MedicalTherapy' | None = None
    possibleTreatment: 'MedicalTherapy' | None = None
    drug: 'Drug' | None = None
    naturalProgression: str | None = None
    status: str | 'EventStatusType' | 'MedicalStudyStatus' | None = None
    differentialDiagnosis: 'DDxElement' | None = None
    epidemiology: str | None = None
    stage: 'MedicalConditionStage' | None = None
    typicalTest: 'MedicalTest' | None = None
    pathophysiology: str | None = None