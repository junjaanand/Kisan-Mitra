"""Farmer profile data model for KisanMitra."""
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum


class Season(str, Enum):
    KHARIF = "Kharif (Monsoon / Summer)"
    RABI = "Rabi (Winter / Spring)"
    ZAID = "Zaid (Summer Short Season)"


class IrrigationType(str, Enum):
    CANAL_TUBEWELL = "Canal / Borewell / Tubewell"
    DRIP_SPRINKLER = "Drip / Sprinkler"
    RAIN_FED = "Rain-fed only"


class FarmerProfile(BaseModel):
    """Represents an Indian farmer's operational profile."""
    farmer_name: str = Field(default="Farmer", description="Farmer name")
    state: str = Field(..., description="Indian state or UT")
    district: str = Field(..., description="District within the state")
    crops: List[str] = Field(default_factory=list, description="Primary crops cultivated")
    farm_size_acres: float = Field(default=2.0, ge=0.1, le=500.0, description="Landholding in acres")
    season: Season = Field(default=Season.RABI, description="Current cropping season")
    irrigation: IrrigationType = Field(default=IrrigationType.CANAL_TUBEWELL, description="Irrigation method")

    def to_search_context(self) -> str:
        """Convert profile to human-readable context for AI prompt generation."""
        crops_str = ", ".join(self.crops) if self.crops else "General crops"
        return (
            f"Farmer: {self.farmer_name}\n"
            f"Location: {self.district}, {self.state}\n"
            f"Crops: {crops_str}\n"
            f"Farm Size: {self.farm_size_acres} acres\n"
            f"Season: {self.season.value}\n"
            f"Irrigation: {self.irrigation.value}"
        )
