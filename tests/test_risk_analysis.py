"""
위험도 분석 서비스 테스트
"""

import pytest
import asyncio
from unittest.mock import Mock, patch
from backend.app.services.risk_analysis_service import RiskAnalysisService
from backend.app.models.sensor_data import SensorData, SensorType

class TestRiskAnalysisService:
    """위험도 분석 서비스 테스트 클래스"""
    
    @pytest.fixture
    def risk_service(self):
        """위험도 분석 서비스 인스턴스"""
        return RiskAnalysisService()
    
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
            ),
            SensorData(
                id=3,
                sensor_id="iot_002",
                sensor_type=SensorType.SMOKE_DENSITY,
                location_lat=37.5665,
                location_lng=127.9780,
                location_name="양평군 용문면",
                smoke_density=75.0,
                data_quality=0.88
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
    async def test_analyze_fire_risk(self, risk_service, sample_sensor_data, sample_location):
        """화재 위험도 분석 테스트"""
        with patch.object(risk_service.weather_service, 'get_current_weather') as mock_weather:
            mock_weather.return_value = {
                "temperature": 30.0,
                "humidity": 40.0,
                "wind_speed": 8.0,
                "wind_direction": 180.0
            }
            
            result = await risk_service.analyze_fire_risk(sample_sensor_data, sample_location)
            
            # 결과 구조 확인
            assert "overall_risk" in result
            assert "risk_level" in result
            assert "fire_detection_risk" in result
            assert "environmental_risk" in result
            assert "weather_risk" in result
            assert "historical_risk" in result
            assert "spread_prediction" in result
            assert "analysis_timestamp" in result
            assert "confidence" in result
            
            # 위험도 값 확인
            assert 0 <= result["overall_risk"] <= 1
            assert result["risk_level"] in ["low", "medium", "high", "critical"]
            assert 0 <= result["confidence"] <= 1
    
    def test_analyze_fire_detection(self, risk_service, sample_sensor_data):
        """화재 탐지 분석 테스트"""
        result = risk_service._analyze_fire_detection(sample_sensor_data)
        
        # 결과 구조 확인
        assert "risk_score" in result
        assert "confidence" in result
        assert "detection_count" in result
        assert "max_confidence" in result
        assert "detection_sources" in result
        
        # 화재 탐지 확인
        assert result["fire_detected"] == True
        assert result["detection_count"] > 0
        assert result["max_confidence"] == 0.95
    
    def test_analyze_environmental_conditions(self, risk_service, sample_sensor_data):
        """환경 조건 분석 테스트"""
        result = risk_service._analyze_environmental_conditions(sample_sensor_data)
        
        # 결과 구조 확인
        assert "risk_score" in result
        assert "temperature_risk" in result
        assert "humidity_risk" in result
        assert "smoke_risk" in result
        assert "visibility_risk" in result
        
        # 위험도 값 확인
        assert 0 <= result["risk_score"] <= 1
        assert 0 <= result["temperature_risk"] <= 1
        assert 0 <= result["humidity_risk"] <= 1
        assert 0 <= result["smoke_risk"] <= 1
        assert 0 <= result["visibility_risk"] <= 1
    
    @pytest.mark.asyncio
    async def test_analyze_weather_conditions(self, risk_service, sample_location):
        """날씨 조건 분석 테스트"""
        with patch.object(risk_service.weather_service, 'get_current_weather') as mock_weather:
            mock_weather.return_value = {
                "temperature": 30.0,
                "humidity": 40.0,
                "wind_speed": 8.0,
                "wind_direction": 180.0
            }
            
            result = await risk_service._analyze_weather_conditions(sample_location)
            
            # 결과 구조 확인
            assert "risk_score" in result
            assert "wind_risk" in result
            assert "temperature_risk" in result
            assert "humidity_risk" in result
            assert "weather_data" in result
            
            # 위험도 값 확인
            assert 0 <= result["risk_score"] <= 1
            assert 0 <= result["wind_risk"] <= 1
            assert 0 <= result["temperature_risk"] <= 1
            assert 0 <= result["humidity_risk"] <= 1
    
    def test_analyze_historical_data(self, risk_service, sample_sensor_data, sample_location):
        """과거 데이터 분석 테스트"""
        result = risk_service._analyze_historical_data(sample_sensor_data, sample_location)
        
        # 결과 구조 확인
        assert "risk_score" in result
        assert "seasonal_risk" in result
        assert "time_risk" in result
        assert "current_month" in result
        assert "current_hour" in result
        
        # 위험도 값 확인
        assert 0 <= result["risk_score"] <= 1
        assert 0 <= result["seasonal_risk"] <= 1
        assert 0 <= result["time_risk"] <= 1
        assert 1 <= result["current_month"] <= 12
        assert 0 <= result["current_hour"] <= 23
    
    def test_calculate_overall_risk(self, risk_service):
        """종합 위험도 계산 테스트"""
        fire_detection_risk = {"risk_score": 0.8}
        environmental_risk = {"risk_score": 0.6}
        weather_risk = {"risk_score": 0.7}
        historical_risk = {"risk_score": 0.4}
        
        overall_risk = risk_service._calculate_overall_risk(
            fire_detection_risk, environmental_risk, weather_risk, historical_risk
        )
        
        assert 0 <= overall_risk <= 1
        # 가중치 적용 확인 (0.4*0.8 + 0.3*0.6 + 0.2*0.7 + 0.1*0.4 = 0.68)
        assert abs(overall_risk - 0.68) < 0.01
    
    def test_determine_risk_level(self, risk_service):
        """위험도 등급 결정 테스트"""
        assert risk_service._determine_risk_level(0.95) == "critical"
        assert risk_service._determine_risk_level(0.85) == "high"
        assert risk_service._determine_risk_level(0.65) == "medium"
        assert risk_service._determine_risk_level(0.25) == "low"
    
    def test_predict_fire_spread(self, risk_service, sample_sensor_data, sample_location):
        """화재 확산 예측 테스트"""
        overall_risk = 0.8
        
        result = risk_service._predict_fire_spread(sample_sensor_data, sample_location, overall_risk)
        
        # 결과 구조 확인
        assert "spread_direction" in result
        assert "spread_speed" in result
        assert "affected_radius" in result
        assert "evacuation_radius" in result
        assert "confidence" in result
        
        # 값 확인
        assert result["spread_speed"] >= 0
        assert result["affected_radius"] >= 0
        assert result["evacuation_radius"] >= result["affected_radius"]
        assert 0 <= result["confidence"] <= 1
    
    def test_calculate_analysis_confidence(self, risk_service, sample_sensor_data):
        """분석 신뢰도 계산 테스트"""
        confidence = risk_service._calculate_analysis_confidence(sample_sensor_data)
        
        assert 0 <= confidence <= 1
        # 센서 데이터가 있으므로 신뢰도가 0보다 커야 함
        assert confidence > 0
