"""
AI 권고안 모델
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, JSON, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum as PyEnum

Base = declarative_base()

class AgencyType(str, PyEnum):
    """기관 타입 열거형"""
    FIRE_DEPARTMENT = "fire_department"  # 소방청
    FOREST_SERVICE = "forest_service"    # 산림청
    LOCAL_GOVERNMENT = "local_government"  # 지자체
    EMERGENCY_MANAGEMENT = "emergency_management"  # 행정안전부

class RecommendationStatus(str, PyEnum):
    """권고안 상태 열거형"""
    PENDING = "pending"          # 대기 중
    APPROVED = "approved"        # 승인됨
    REJECTED = "rejected"        # 거부됨
    AUTO_APPROVED = "auto_approved"  # 자동 승인됨  
    EXPIRED = "expired"          # 만료됨

class PriorityLevel(str, PyEnum):
    """우선순위 레벨"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class AIRecommendation(Base):
    """AI 권고안 테이블"""
    __tablename__ = "ai_recommendations"
    
    id = Column(Integer, primary_key=True, index=True)
    recommendation_id = Column(String(100), unique=True, nullable=False, index=True)
    
    # 기본 정보
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    agency_type = Column(Enum(AgencyType), nullable=False)
    priority_level = Column(Enum(PriorityLevel), nullable=False)
    
    # AI 생성 정보
    ai_model_name = Column(String(100), nullable=False, default="믿:음-2.0")
    ai_confidence = Column(Float, nullable=False)
    ai_reasoning = Column(Text, nullable=True)
    
    # 권고안 내용
    immediate_actions = Column(JSON, nullable=True)  # 즉시 조치사항
    legal_basis = Column(JSON, nullable=True)        # 법적 근거
    expected_cost = Column(Float, nullable=True)     # 예상 비용
    expected_effect = Column(JSON, nullable=True)    # 예상 효과
    required_resources = Column(JSON, nullable=True) # 필요 자원
    
    # 상태 및 승인
    status = Column(Enum(RecommendationStatus), default=RecommendationStatus.PENDING)
    approved_by = Column(String(100), nullable=True)
    approved_at = Column(DateTime(timezone=True), nullable=True)
    rejection_reason = Column(Text, nullable=True)
    
    # 위치 정보
    location_lat = Column(Float, nullable=False)
    location_lng = Column(Float, nullable=False)
    location_name = Column(String(200), nullable=True)
    affected_radius = Column(Float, nullable=True)  # 영향 반경 (km)
    
    # 메타데이터
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=True)

class AIRecommendationCreate(BaseModel):
    """AI 권고안 생성 스키마"""
    title: str = Field(..., description="권고안 제목")
    description: Optional[str] = Field(None, description="권고안 설명")
    agency_type: AgencyType = Field(..., description="대상 기관")
    priority_level: PriorityLevel = Field(..., description="우선순위")
    
    # AI 생성 정보
    ai_confidence: float = Field(..., ge=0, le=1, description="AI 신뢰도")
    ai_reasoning: Optional[str] = Field(None, description="AI 추론 과정")
    
    # 권고안 내용
    immediate_actions: Optional[List[Dict[str, Any]]] = Field(None, description="즉시 조치사항")
    legal_basis: Optional[List[Dict[str, Any]]] = Field(None, description="법적 근거")
    expected_cost: Optional[float] = Field(None, ge=0, description="예상 비용")
    expected_effect: Optional[Dict[str, Any]] = Field(None, description="예상 효과")
    required_resources: Optional[List[Dict[str, Any]]] = Field(None, description="필요 자원")
    
    # 위치 정보
    location_lat: float = Field(..., ge=-90, le=90, description="위도")
    location_lng: float = Field(..., ge=-180, le=180, description="경도")
    location_name: Optional[str] = Field(None, description="위치명")
    affected_radius: Optional[float] = Field(None, ge=0, description="영향 반경 (km)")
    
    # 만료 시간
    expires_at: Optional[datetime] = Field(None, description="만료 시간")

class AIRecommendationResponse(BaseModel):
    """AI 권고안 응답 스키마"""
    id: int
    recommendation_id: str
    title: str
    description: Optional[str]
    agency_type: AgencyType
    priority_level: PriorityLevel
    
    ai_model_name: str
    ai_confidence: float
    ai_reasoning: Optional[str]
    
    immediate_actions: Optional[List[Dict[str, Any]]]
    legal_basis: Optional[List[Dict[str, Any]]]
    expected_cost: Optional[float]
    expected_effect: Optional[Dict[str, Any]]
    required_resources: Optional[List[Dict[str, Any]]]
    
    status: RecommendationStatus
    approved_by: Optional[str]
    approved_at: Optional[datetime]
    rejection_reason: Optional[str]
    
    location_lat: float
    location_lng: float
    location_name: Optional[str]
    affected_radius: Optional[float]
    
    created_at: datetime
    updated_at: Optional[datetime]
    expires_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class RecommendationApproval(BaseModel):
    """권고안 승인 스키마"""
    recommendation_id: str = Field(..., description="권고안 ID")
    approved: bool = Field(..., description="승인 여부")
    approved_by: str = Field(..., description="승인자")
    rejection_reason: Optional[str] = Field(None, description="거부 사유")

class RecommendationFilter(BaseModel):
    """권고안 필터 스키마"""
    agency_type: Optional[AgencyType] = None
    status: Optional[RecommendationStatus] = None
    priority_level: Optional[PriorityLevel] = None
    ai_confidence_min: Optional[float] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    location_lat_min: Optional[float] = None
    location_lat_max: Optional[float] = None
    location_lng_min: Optional[float] = None
    location_lng_max: Optional[float] = None
