from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.product.Product import Product
from msgspec_schemaorg.utils import parse_iso8601
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.CarUsageType import CarUsageType
    from msgspec_schemaorg.models.intangible.DriveWheelConfigurationValue import DriveWheelConfigurationValue
    from msgspec_schemaorg.models.intangible.EngineSpecification import EngineSpecification
    from msgspec_schemaorg.models.intangible.QualitativeValue import QualitativeValue
    from msgspec_schemaorg.models.intangible.QuantitativeValue import QuantitativeValue
    from msgspec_schemaorg.models.intangible.SteeringPositionValue import SteeringPositionValue
from datetime import date
from typing import Optional, Union, Dict, List, Any


class Vehicle(Product):
    """A vehicle is a device that is designed or used to transport people or cargo over land, water, air, or through space."""
    type: str = field(default_factory=lambda: "Vehicle", name="@type")
    mileageFromOdometer: 'QuantitativeValue' | None = None
    fuelCapacity: 'QuantitativeValue' | None = None
    vehicleTransmission: 'URL' | str | 'QualitativeValue' | None = None
    bodyType: 'URL' | str | 'QualitativeValue' | None = None
    vehicleInteriorColor: str | None = None
    fuelConsumption: 'QuantitativeValue' | None = None
    productionDate: date | None = None
    vehicleSpecialUsage: str | 'CarUsageType' | None = None
    numberOfForwardGears: int | float | 'QuantitativeValue' | None = None
    fuelEfficiency: 'QuantitativeValue' | None = None
    vehicleModelDate: date | None = None
    vehicleEngine: 'EngineSpecification' | None = None
    numberOfDoors: int | float | 'QuantitativeValue' | None = None
    numberOfPreviousOwners: int | float | 'QuantitativeValue' | None = None
    weightTotal: 'QuantitativeValue' | None = None
    numberOfAxles: int | float | 'QuantitativeValue' | None = None
    payload: 'QuantitativeValue' | None = None
    cargoVolume: 'QuantitativeValue' | None = None
    meetsEmissionStandard: 'URL' | str | 'QualitativeValue' | None = None
    wheelbase: 'QuantitativeValue' | None = None
    speed: 'QuantitativeValue' | None = None
    modelDate: date | None = None
    numberOfAirbags: int | float | str | None = None
    accelerationTime: 'QuantitativeValue' | None = None
    callSign: str | None = None
    tongueWeight: 'QuantitativeValue' | None = None
    seatingCapacity: int | float | 'QuantitativeValue' | None = None
    driveWheelConfiguration: str | 'DriveWheelConfigurationValue' | None = None
    fuelType: 'URL' | str | 'QualitativeValue' | None = None
    vehicleInteriorType: str | None = None
    vehicleConfiguration: str | None = None
    dateVehicleFirstRegistered: date | None = None
    vehicleIdentificationNumber: str | None = None
    emissionsCO2: int | float | None = None
    knownVehicleDamages: str | None = None
    vehicleSeatingCapacity: int | float | 'QuantitativeValue' | None = None
    trailerWeight: 'QuantitativeValue' | None = None
    purchaseDate: date | None = None
    steeringPosition: 'SteeringPositionValue' | None = None