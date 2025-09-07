"""
센서 데이터 모델
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum

Base = declarative_base()

class SensorType(str, Enum):
    """센서 타입 열거형"""
    TEMPERATURE = "temperature"
    HUMIDITY = "humidity"
    SMOKE_DENSITY = "smoke_density"
    WIND_SPEED = "wind_speed"
    WIND_DIRECTION = "wind_direction"
    AIR_PRESSURE = "air_pressure"
    VISIBILITY = "visibility"
    CCTV = "cctv"
    DRONE = "drone"
    SATELLITE = "satellite"

class SensorData(Base):
    """센서 데이터 테이블"""
    __tablename__ = "sensor_data"
    
    id = Column(Integer, primary_key=True, index=True)
    sensor_id = Column(String(100), nullable=False, index=True)
    sensor_type = Column(String(50), nullable=False)
    location_lat = Column(Float, nullable=False)
    location_lng = Column(Float, nullable=False)
    location_name = Column(String(200), nullable=True)
    
    # 센서 값들
    temperature = Column(Float, nullable=True)
    humidity = Column(Float, nullable=True)
    smoke_density = Column(Float, nullable=True)
    wind_speed = Column(Float, nullable=True)
    wind_direction = Column(Float, nullable=True)
    air_pressure = Column(Float, nullable=True)
    visibility = Column(Float, nullable=True)
    
    # Vision AI 데이터
    image_url = Column(String(500), nullable=True)
    image_analysis = Column(JSON, nullable=True)
    fire_detected = Column(Boolean, default=False)
    fire_confidence = Column(Float, nullable=True)
    
    # 메타데이터
    raw_data = Column(JSON, nullable=True)
    data_quality = Column(Float, nullable=True)  # 0-1 사이의 데이터 품질 점수
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class SensorDataCreate(BaseModel):
    """센서 데이터 생성 스키마"""
    sensor_id: str = Field(..., description="센서 고유 ID")
    sensor_type: SensorType = Field(..., description="센서 타입")
    location_lat: float = Field(..., ge=-90, le=90, description="위도")
    location_lng: float = Field(..., ge=-180, le=180, description="경도")
    location_name: Optional[str] = Field(None, description="위치명")
    
    # 센서 값들
    temperature: Optional[float] = Field(None, description="온도 (°C)")
    humidity: Optional[float] = Field(None, ge=0, le=100, description="습도 (%)")
    smoke_density: Optional[float] = Field(None, ge=0, description="연기 농도")
    wind_speed: Optional[float] = Field(None, ge=0, description="풍속 (m/s)")
    wind_direction: Optional[float] = Field(None, ge=0, le=360, description="풍향 (도)")
    air_pressure: Optional[float] = Field(None, description="기압 (hPa)")
    visibility: Optional[float] = Field(None, ge=0, description="가시거리 (km)")
    
    # Vision AI 데이터
    image_url: Optional[str] = Field(None, description="이미지 URL")
    image_analysis: Optional[Dict[str, Any]] = Field(None, description="이미지 분석 결과")
    fire_detected: bool = Field(False, description="화재 탐지 여부")
    fire_confidence: Optional[float] = Field(None, ge=0, le=1, description="화재 탐지 신뢰도")
    
    # 메타데이터
    raw_data: Optional[Dict[str, Any]] = Field(None, description="원본 데이터")
    data_quality: Optional[float] = Field(None, ge=0, le=1, description="데이터 품질")

class SensorDataResponse(BaseModel):
    """센서 데이터 응답 스키마"""
    id: int
    sensor_id: str
    sensor_type: SensorType
    location_lat: float
    location_lng: float
    location_name: Optional[str]
    
    temperature: Optional[float]
    humidity: Optional[float]
    smoke_density: Optional[float]
    wind_speed: Optional[float]
    wind_direction: Optional[float]
    air_pressure: Optional[float]
    visibility: Optional[float]
    
    image_url: Optional[str]
    image_analysis: Optional[Dict[str, Any]]
    fire_detected: bool
    fire_confidence: Optional[float]
    
    raw_data: Optional[Dict[str, Any]]
    data_quality: Optional[float]
    timestamp: datetime
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class SensorDataFilter(BaseModel):
    """센서 데이터 필터 스키마"""
    sensor_type: Optional[SensorType] = None
    location_lat_min: Optional[float] = None
    location_lat_max: Optional[float] = None
    location_lng_min: Optional[float] = None
    location_lng_max: Optional[float] = None
    fire_detected: Optional[bool] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    data_quality_min: Optional[float] = None
