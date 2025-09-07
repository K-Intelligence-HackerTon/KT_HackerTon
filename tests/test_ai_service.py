"""
AI 서비스 테스트
"""

import pytest
import asyncio
from unittest.mock import Mock, patch
from backend.app.services.ai_service import AIService
from backend.app.models.sensor_data import SensorData, SensorType
from backend.app.models.ai_recommendation import AgencyType, PriorityLevel

class TestAIService:
    """AI 서비스 테스트 클래스"""
    
    @pytest.fixture
    def ai_service(self):
        """AI 서비스 인스턴스"""
        return AIService()
    
    @pytest.fixture
    def sample_sensor_data(self):
        """샘플 센서 데이터"""
        return [
            SensorData(
                id=1,
                sensor_id="cctv_001",
                sensor_type=SensorType.CCTV,
                location_lat=37.5665,
                location_lng=127.9780,
                location_name="양평군 용문면",
                fire_detected=True,
                fire_confidence=0.95,
                data_quality=0.9
            ),
            SensorData(
                id=2,
                sensor_id="iot_001",
                sensor_type=SensorType.TEMPERATURE,
                location_lat=37.5665,
                location_lng=127.9780,
                location_name="양평군 용문면",
                temperature=32.5,
                humidity=25.0,
                data_quality=0.85
            )
        ]
    
    @pytest.fixture
    def sample_location(self):
        """샘플 위치 정보"""
        return {
            "lat": 37.5665,
            "lng": 127.9780,
            "name": "양평군 용문면"
        }
    
    @pytest.mark.asyncio
    async def test_generate_recommendations(self, ai_service, sample_sensor_data, sample_location):
        """권고안 생성 테스트"""
        fire_risk_level = 0.87
        
        recommendations = await ai_service.generate_recommendations(
            sample_sensor_data, fire_risk_level, sample_location
        )
        
        # 권고안이 생성되었는지 확인
        assert len(recommendations) == 3  # 소방청, 산림청, 지자체
        
        # 각 권고안의 기본 정보 확인
        for rec in recommendations:
            assert rec.title is not None
            assert rec.agency_type in [AgencyType.FIRE_DEPARTMENT, AgencyType.FOREST_SERVICE, AgencyType.LOCAL_GOVERNMENT]
            assert rec.priority_level in [PriorityLevel.LOW, PriorityLevel.MEDIUM, PriorityLevel.HIGH, PriorityLevel.CRITICAL]
            assert 0 <= rec.ai_confidence <= 1
            assert rec.location_lat == sample_location["lat"]
            assert rec.location_lng == sample_location["lng"]
    
    @pytest.mark.asyncio
    async def test_analyze_sensor_data(self, ai_service, sample_sensor_data):
        """센서 데이터 분석 테스트"""
        analysis = await ai_service._analyze_sensor_data(sample_sensor_data)
        
        # 분석 결과 확인
        assert "fire_detected" in analysis
        assert "fire_confidence" in analysis
        assert "environmental_conditions" in analysis
        assert "risk_factors" in analysis
        assert "recommended_actions" in analysis
        
        # 화재 탐지 확인
        assert analysis["fire_detected"] == True
        assert analysis["fire_confidence"] == 0.95
    
    @pytest.mark.asyncio
    async def test_generate_fire_department_recommendation(self, ai_service, sample_sensor_data, sample_location):
        """소방청 권고안 생성 테스트"""
        analysis = await ai_service._analyze_sensor_data(sample_sensor_data)
        fire_risk_level = 0.87
        
        rec = await ai_service._generate_fire_department_recommendation(
            analysis, fire_risk_level, sample_location
        )
        
        assert rec is not None
        assert rec.agency_type == AgencyType.FIRE_DEPARTMENT
        assert rec.title.startswith("🚒 소방청")
        assert rec.immediate_actions is not None
        assert len(rec.immediate_actions) > 0
        assert rec.legal_basis is not None
        assert rec.expected_cost > 0
    
    @pytest.mark.asyncio
    async def test_generate_forest_service_recommendation(self, ai_service, sample_sensor_data, sample_location):
        """산림청 권고안 생성 테스트"""
        analysis = await ai_service._analyze_sensor_data(sample_sensor_data)
        fire_risk_level = 0.87
        
        rec = await ai_service._generate_forest_service_recommendation(
            analysis, fire_risk_level, sample_location
        )
        
        assert rec is not None
        assert rec.agency_type == AgencyType.FOREST_SERVICE
        assert rec.title.startswith("🌲 산림청")
        assert rec.immediate_actions is not None
        assert len(rec.immediate_actions) > 0
        assert rec.legal_basis is not None
        assert rec.expected_cost > 0
    
    @pytest.mark.asyncio
    async def test_generate_local_government_recommendation(self, ai_service, sample_sensor_data, sample_location):
        """지자체 권고안 생성 테스트"""
        analysis = await ai_service._analyze_sensor_data(sample_sensor_data)
        fire_risk_level = 0.87
        
        rec = await ai_service._generate_local_government_recommendation(
            analysis, fire_risk_level, sample_location
        )
        
        assert rec is not None
        assert rec.agency_type == AgencyType.LOCAL_GOVERNMENT
        assert rec.title.startswith("🏛️ 지자체")
        assert rec.immediate_actions is not None
        assert len(rec.immediate_actions) > 0
        assert rec.legal_basis is not None
        assert rec.expected_cost > 0
