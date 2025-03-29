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
    drugClass: Union[List['DrugClass'], 'DrugClass', None] = None
    relatedDrug: Union[List['Drug'], 'Drug', None] = None
    alcoholWarning: Union[List[str], str, None] = None
    breastfeedingWarning: Union[List[str], str, None] = None
    dosageForm: Union[List[str], str, None] = None
    isAvailableGenerically: Union[List[bool], bool, None] = None
    includedInHealthInsurancePlan: Union[List['HealthInsurancePlan'], 'HealthInsurancePlan', None] = None
    legalStatus: Union[List[Union[str, 'DrugLegalStatus', 'MedicalEnumeration']], Union[str, 'DrugLegalStatus', 'MedicalEnumeration'], None] = None
    drugUnit: Union[List[str], str, None] = None
    overdosage: Union[List[str], str, None] = None
    prescriptionStatus: Union[List[Union[str, 'DrugPrescriptionStatus']], Union[str, 'DrugPrescriptionStatus'], None] = None
    nonProprietaryName: Union[List[str], str, None] = None
    isProprietary: Union[List[bool], bool, None] = None
    labelDetails: Union[List['URL'], 'URL', None] = None
    mechanismOfAction: Union[List[str], str, None] = None
    rxcui: Union[List[str], str, None] = None
    activeIngredient: Union[List[str], str, None] = None
    doseSchedule: Union[List['DoseSchedule'], 'DoseSchedule', None] = None
    pregnancyWarning: Union[List[str], str, None] = None
    warning: Union[List[Union['URL', str]], Union['URL', str], None] = None
    proprietaryName: Union[List[str], str, None] = None
    maximumIntake: Union[List['MaximumDoseSchedule'], 'MaximumDoseSchedule', None] = None
    administrationRoute: Union[List[str], str, None] = None
    pregnancyCategory: Union[List['DrugPregnancyCategory'], 'DrugPregnancyCategory', None] = None
    availableStrength: Union[List['DrugStrength'], 'DrugStrength', None] = None
    clincalPharmacology: Union[List[str], str, None] = None
    foodWarning: Union[List[str], str, None] = None
    prescribingInfo: Union[List['URL'], 'URL', None] = None
    clinicalPharmacology: Union[List[str], str, None] = None
    interactingDrug: Union[List['Drug'], 'Drug', None] = None