"""Market intelligence and agricultural data models for KisanMitra."""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum


class PriceRecommendation(str, Enum):
    SELL_NOW = "SELL NOW"
    HOLD = "HOLD"
    WATCH = "WATCH MARKET"


class AlertSeverity(str, Enum):
    URGENT = "URGENT"
    IMPORTANT = "IMPORTANT"
    INFO = "INFO"


class CropPrice(BaseModel):
    """Live APMC Mandi price data for a crop."""
    crop_name: str
    price_per_quintal: Optional[float] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    mandi_name: Optional[str] = "Regional APMC"
    price_trend: str = "Stable"
    recommendation: PriceRecommendation = PriceRecommendation.WATCH
    confidence: str = "Medium"
    arrival_quantity: Optional[str] = None
    notes: Optional[str] = None
    source_urls: List[str] = Field(default_factory=list)
    last_updated: Optional[str] = None


class NewsAlert(BaseModel):
    """Agriculture advisory, weather update, or policy news alert."""
    headline: str
    summary: str
    severity: AlertSeverity = AlertSeverity.INFO
    category: str = "General"
    source: Optional[str] = None
    date: Optional[str] = None
    url: Optional[str] = None


class TrendData(BaseModel):
    """Google Trends search interest and seasonal cycles."""
    crop_name: str
    trend_direction: str = "Stable"
    peak_months: List[str] = Field(default_factory=list)
    insight: str = ""
    relative_demand_index: Optional[int] = 50
    related_queries: List[str] = Field(default_factory=list)


class InputDeal(BaseModel):
    """Farming input deal from Google Shopping (fertilizers, seeds, tools)."""
    product_name: str
    category: str = "Agri Inputs"
    price: Optional[str] = None
    seller: Optional[str] = None
    rating: Optional[float] = None
    url: Optional[str] = None
    thumbnail: Optional[str] = None
    savings_hint: Optional[str] = None


class MandiInfo(BaseModel):
    """Nearby APMC Mandi, cold storage, or agricultural warehouse."""
    name: str
    address: Optional[str] = None
    rating: Optional[float] = None
    reviews_count: Optional[int] = None
    phone: Optional[str] = None
    open_status: Optional[str] = None
    link: Optional[str] = None
    mandi_type: str = "APMC Mandi"


class FarmerIntelligenceReport(BaseModel):
    """Comprehensive intelligence report synthesized for the farmer."""
    farmer_name: str
    location: str
    crops: List[str]
    prices: List[CropPrice] = Field(default_factory=list)
    news_alerts: List[NewsAlert] = Field(default_factory=list)
    trends: List[TrendData] = Field(default_factory=list)
    deals: List[InputDeal] = Field(default_factory=list)
    mandis: List[MandiInfo] = Field(default_factory=list)
    weather_summary: Optional[str] = None
    advisory_recommendations: List[str] = Field(default_factory=list)
    generated_at: Optional[str] = None
