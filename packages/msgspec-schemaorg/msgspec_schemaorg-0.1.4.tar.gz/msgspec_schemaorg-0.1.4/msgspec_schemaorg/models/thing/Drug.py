from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.thing.Substance import Substance
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.DrugPregnancyCategory import DrugPregnancyCategory
    from msgspec_schemaorg.models.intangible.DrugPrescriptionStatus import DrugPrescriptionStatus
    from msgspec_schemaorg.models.intangible.HealthInsurancePlan import HealthInsurancePlan
    from msgspec_schemaorg.models.intangible.MedicalEnumeration import MedicalEnumeration
    from msgspec_schemaorg.models.thing.DoseSchedule import DoseSchedule
    from msgspec_schemaorg.models.thing.Drug import Drug
    from msgspec_schemaorg.models.thing.DrugClass import DrugClass
    from msgspec_schemaorg.models.thing.DrugLegalStatus import DrugLegalStatus
    from msgspec_schemaorg.models.thing.DrugStrength import DrugStrength
    from msgspec_schemaorg.models.thing.MaximumDoseSchedule import MaximumDoseSchedule
from typing import Optional, Union, Dict, List, Any


class Drug(Substance):
    """A chemical or biologic substance, used as a medical therapy, that has a physiological effect on an organism. Here the term drug is used interchangeably with the term medicine although clinical knowledge makes a clear difference between them."""
    type: str = field(default_factory=lambda: "Drug", name="@type")
    drugClass: 'DrugClass' | None = None
    relatedDrug: 'Drug' | None = None
    alcoholWarning: str | None = None
    breastfeedingWarning: str | None = None
    dosageForm: str | None = None
    isAvailableGenerically: bool | None = None
    includedInHealthInsurancePlan: 'HealthInsurancePlan' | None = None
    legalStatus: str | 'DrugLegalStatus' | 'MedicalEnumeration' | None = None
    drugUnit: str | None = None
    overdosage: str | None = None
    prescriptionStatus: str | 'DrugPrescriptionStatus' | None = None
    nonProprietaryName: str | None = None
    isProprietary: bool | None = None
    labelDetails: 'URL' | None = None
    mechanismOfAction: str | None = None
    rxcui: str | None = None
    activeIngredient: str | None = None
    doseSchedule: 'DoseSchedule' | None = None
    pregnancyWarning: str | None = None
    warning: 'URL' | str | None = None
    proprietaryName: str | None = None
    maximumIntake: 'MaximumDoseSchedule' | None = None
    administrationRoute: str | None = None
    pregnancyCategory: 'DrugPregnancyCategory' | None = None
    availableStrength: 'DrugStrength' | None = None
    clincalPharmacology: str | None = None
    foodWarning: str | None = None
    prescribingInfo: 'URL' | None = None
    clinicalPharmacology: str | None = None
    interactingDrug: 'Drug' | None = None