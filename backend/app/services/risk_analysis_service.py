"""
위험도 분석 서비스 모듈
센서 데이터 융합 및 화재 위험도 산출
"""

import asyncio
import logging
import numpy as np
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
import math

from app.models.sensor_data import SensorData, SensorType
from app.services.weather_service import WeatherService

logger = logging.getLogger(__name__)

class RiskAnalysisService:
    """위험도 분석 서비스 클래스"""
    
    def __init__(self):
        self.weather_service = WeatherService()
        
        # 위험도 계산 가중치
        self.weights = {
            "fire_detection": 0.4,      # 화재 탐지 가중치
            "environmental": 0.3,       # 환경 조건 가중치
            "weather": 0.2,             # 날씨 조건 가중치
            "historical": 0.1           # 과거 데이터 가중치
        }
        
        # 위험도 임계값
        self.thresholds = {
            "low": 0.3,
            "medium": 0.6,
            "high": 0.8,
            "critical": 0.9
        }
    
    async def analyze_fire_risk(
        self, 
        sensor_data: List[SensorData],
        location: Dict[str, float]
    ) -> Dict[str, Any]:
        """
        화재 위험도 종합 분석
        
        Args:
            sensor_data: 센서 데이터 리스트
            location: 위치 정보 {"lat": float, "lng": float}
            
        Returns:
            위험도 분석 결과
        """
        try:
            logger.info(f"🔍 화재 위험도 분석 시작 - 센서 데이터: {len(sensor_data)}개")
            
            # 1. 화재 탐지 분석
            fire_detection_risk = self._analyze_fire_detection(sensor_data)
            
            # 2. 환경 조건 분석
            environmental_risk = self._analyze_environmental_conditions(sensor_data)
            
            # 3. 날씨 조건 분석
            weather_risk = await self._analyze_weather_conditions(location)
            
            # 4. 과거 데이터 분석
            historical_risk = self._analyze_historical_data(sensor_data, location)
            
            # 5. 종합 위험도 계산
            overall_risk = self._calculate_overall_risk(
                fire_detection_risk,
                environmental_risk,
                weather_risk,
                historical_risk
            )
            
            # 6. 위험도 등급 결정
            risk_level = self._determine_risk_level(overall_risk)
            
            # 7. 확산 예측
            spread_prediction = self._predict_fire_spread(
                sensor_data, location, overall_risk
            )
            
            analysis_result = {
                "overall_risk": overall_risk,
                "risk_level": risk_level,
                "fire_detection_risk": fire_detection_risk,
                "environmental_risk": environmental_risk,
                "weather_risk": weather_risk,
                "historical_risk": historical_risk,
                "spread_prediction": spread_prediction,
                "analysis_timestamp": datetime.now().isoformat(),
                "confidence": self._calculate_analysis_confidence(sensor_data)
            }
            
            logger.info(f"✅ 화재 위험도 분석 완료 - 위험도: {overall_risk:.2f}, 등급: {risk_level}")
            return analysis_result
            
        except Exception as e:
            logger.error(f"❌ 화재 위험도 분석 실패: {str(e)}")
            raise
    
    def _analyze_fire_detection(self, sensor_data: List[SensorData]) -> Dict[str, Any]:
        """화재 탐지 분석"""
        try:
            # 화재 탐지된 센서들
            fire_detected_sensors = [s for s in sensor_data if s.fire_detected]
            
            if not fire_detected_sensors:
                return {
                    "risk_score": 0.0,
                    "confidence": 0.0,
                    "detection_count": 0,
                    "max_confidence": 0.0,
                    "detection_sources": []
                }
            
            # 탐지 신뢰도 분석
            confidences = [s.fire_confidence or 0 for s in fire_detected_sensors]
            max_confidence = max(confidences)
            avg_confidence = sum(confidences) / len(confidences)
            
            # 탐지 소스 분석
            detection_sources = []
            for sensor in fire_detected_sensors:
                detection_sources.append({
                    "sensor_type": sensor.sensor_type,
                    "sensor_id": sensor.sensor_id,
                    "confidence": sensor.fire_confidence or 0,
                    "location": (sensor.location_lat, sensor.location_lng)
                })
            
            # 위험도 점수 계산
            risk_score = min(0.99, max_confidence * (len(fire_detected_sensors) / 3))
            
            return {
                "risk_score": risk_score,
                "confidence": avg_confidence,
                "detection_count": len(fire_detected_sensors),
                "max_confidence": max_confidence,
                "detection_sources": detection_sources
            }
            
        except Exception as e:
            logger.error(f"화재 탐지 분석 실패: {str(e)}")
            return {
                "risk_score": 0.0,
                "confidence": 0.0,
                "detection_count": 0,
                "max_confidence": 0.0,
                "detection_sources": []
            }
    
    def _analyze_environmental_conditions(self, sensor_data: List[SensorData]) -> Dict[str, Any]:
        """환경 조건 분석"""
        try:
            # 온도 데이터 분석
            temp_data = [s for s in sensor_data if s.temperature is not None]
            temp_risk = 0.0
            if temp_data:
                avg_temp = sum(s.temperature for s in temp_data) / len(temp_data)
                max_temp = max(s.temperature for s in temp_data)
                # 30도 이상이면 위험도 증가
                temp_risk = min(0.8, max(0, (max_temp - 25) / 20))
            
            # 습도 데이터 분석
            humidity_data = [s for s in sensor_data if s.humidity is not None]
            humidity_risk = 0.0
            if humidity_data:
                avg_humidity = sum(s.humidity for s in humidity_data) / len(humidity_data)
                min_humidity = min(s.humidity for s in humidity_data)
                # 30% 이하면 위험도 증가
                humidity_risk = min(0.8, max(0, (30 - min_humidity) / 30))
            
            # 연기 농도 분석
            smoke_data = [s for s in sensor_data if s.smoke_density is not None]
            smoke_risk = 0.0
            if smoke_data:
                avg_smoke = sum(s.smoke_density for s in smoke_data) / len(smoke_data)
                max_smoke = max(s.smoke_density for s in smoke_data)
                # 연기 농도가 높을수록 위험도 증가
                smoke_risk = min(0.9, max_smoke / 100)
            
            # 가시거리 분석
            visibility_data = [s for s in sensor_data if s.visibility is not None]
            visibility_risk = 0.0
            if visibility_data:
                min_visibility = min(s.visibility for s in visibility_data)
                # 가시거리가 짧을수록 위험도 증가
                visibility_risk = min(0.7, max(0, (5 - min_visibility) / 5))
            
            # 종합 환경 위험도
            environmental_risk = (temp_risk + humidity_risk + smoke_risk + visibility_risk) / 4
            
            return {
                "risk_score": environmental_risk,
                "temperature_risk": temp_risk,
                "humidity_risk": humidity_risk,
                "smoke_risk": smoke_risk,
                "visibility_risk": visibility_risk,
                "avg_temperature": sum(s.temperature for s in temp_data) / len(temp_data) if temp_data else None,
                "min_humidity": min(s.humidity for s in humidity_data) if humidity_data else None,
                "max_smoke_density": max(s.smoke_density for s in smoke_data) if smoke_data else None,
                "min_visibility": min(s.visibility for s in visibility_data) if visibility_data else None
            }
            
        except Exception as e:
            logger.error(f"환경 조건 분석 실패: {str(e)}")
            return {
                "risk_score": 0.0,
                "temperature_risk": 0.0,
                "humidity_risk": 0.0,
                "smoke_risk": 0.0,
                "visibility_risk": 0.0,
                "avg_temperature": None,
                "min_humidity": None,
                "max_smoke_density": None,
                "min_visibility": None
            }
    
    async def _analyze_weather_conditions(self, location: Dict[str, float]) -> Dict[str, Any]:
        """날씨 조건 분석"""
        try:
            # 현재 날씨 정보 조회
            weather_info = await self.weather_service.get_current_weather(
                location["lat"], location["lng"]
            )
            
            if not weather_info:
                return {
                    "risk_score": 0.0,
                    "wind_risk": 0.0,
                    "temperature_risk": 0.0,
                    "humidity_risk": 0.0,
                    "weather_data": None
                }
            
            # 풍속 위험도
            wind_speed = weather_info.get("wind_speed", 0)
            wind_risk = min(0.9, max(0, (wind_speed - 5) / 15))  # 5m/s 이상부터 위험도 증가
            
            # 온도 위험도
            temperature = weather_info.get("temperature", 20)
            temp_risk = min(0.8, max(0, (temperature - 25) / 20))  # 25도 이상부터 위험도 증가
            
            # 습도 위험도
            humidity = weather_info.get("humidity", 50)
            humidity_risk = min(0.8, max(0, (30 - humidity) / 30))  # 30% 이하면 위험도 증가
            
            # 종합 날씨 위험도
            weather_risk = (wind_risk + temp_risk + humidity_risk) / 3
            
            return {
                "risk_score": weather_risk,
                "wind_risk": wind_risk,
                "temperature_risk": temp_risk,
                "humidity_risk": humidity_risk,
                "wind_speed": wind_speed,
                "temperature": temperature,
                "humidity": humidity,
                "weather_data": weather_info
            }
            
        except Exception as e:
            logger.error(f"날씨 조건 분석 실패: {str(e)}")
            return {
                "risk_score": 0.0,
                "wind_risk": 0.0,
                "temperature_risk": 0.0,
                "humidity_risk": 0.0,
                "weather_data": None
            }
    
    def _analyze_historical_data(
        self, 
        sensor_data: List[SensorData], 
        location: Dict[str, float]
    ) -> Dict[str, Any]:
        """과거 데이터 분석"""
        try:
            # 현재는 간단한 구현 (실제로는 과거 데이터베이스 조회)
            # 과거 화재 발생 이력, 계절적 패턴 등을 고려
            
            # 계절적 위험도 (예시)
            current_month = datetime.now().month
            seasonal_risk = 0.0
            
            if current_month in [3, 4, 5]:  # 봄
                seasonal_risk = 0.3
            elif current_month in [6, 7, 8]:  # 여름
                seasonal_risk = 0.1
            elif current_month in [9, 10, 11]:  # 가을
                seasonal_risk = 0.4
            elif current_month in [12, 1, 2]:  # 겨울
                seasonal_risk = 0.2
            
            # 시간대별 위험도 (예시)
            current_hour = datetime.now().hour
            time_risk = 0.0
            
            if 10 <= current_hour <= 16:  # 낮 시간대
                time_risk = 0.3
            elif 16 <= current_hour <= 20:  # 저녁 시간대
                time_risk = 0.2
            else:  # 밤/새벽 시간대
                time_risk = 0.1
            
            # 종합 과거 데이터 위험도
            historical_risk = (seasonal_risk + time_risk) / 2
            
            return {
                "risk_score": historical_risk,
                "seasonal_risk": seasonal_risk,
                "time_risk": time_risk,
                "current_month": current_month,
                "current_hour": current_hour
            }
            
        except Exception as e:
            logger.error(f"과거 데이터 분석 실패: {str(e)}")
            return {
                "risk_score": 0.0,
                "seasonal_risk": 0.0,
                "time_risk": 0.0,
                "current_month": datetime.now().month,
                "current_hour": datetime.now().hour
            }
    
    def _calculate_overall_risk(
        self,
        fire_detection_risk: Dict[str, Any],
        environmental_risk: Dict[str, Any],
        weather_risk: Dict[str, Any],
        historical_risk: Dict[str, Any]
    ) -> float:
        """종합 위험도 계산"""
        try:
            # 가중치 적용
            overall_risk = (
                fire_detection_risk["risk_score"] * self.weights["fire_detection"] +
                environmental_risk["risk_score"] * self.weights["environmental"] +
                weather_risk["risk_score"] * self.weights["weather"] +
                historical_risk["risk_score"] * self.weights["historical"]
            )
            
            return min(0.99, max(0.0, overall_risk))
            
        except Exception as e:
            logger.error(f"종합 위험도 계산 실패: {str(e)}")
            return 0.0
    
    def _determine_risk_level(self, overall_risk: float) -> str:
        """위험도 등급 결정"""
        if overall_risk >= self.thresholds["critical"]:
            return "critical"
        elif overall_risk >= self.thresholds["high"]:
            return "high"
        elif overall_risk >= self.thresholds["medium"]:
            return "medium"
        else:
            return "low"
    
    def _predict_fire_spread(
        self, 
        sensor_data: List[SensorData], 
        location: Dict[str, float], 
        overall_risk: float
    ) -> Dict[str, Any]:
        """화재 확산 예측"""
        try:
            # 풍속 데이터 수집
            wind_data = [s for s in sensor_data if s.wind_speed is not None and s.wind_direction is not None]
            
            if not wind_data:
                return {
                    "spread_direction": None,
                    "spread_speed": 0.0,
                    "affected_radius": 0.0,
                    "evacuation_radius": 0.0,
                    "confidence": 0.0
                }
            
            # 평균 풍속과 풍향 계산
            avg_wind_speed = sum(s.wind_speed for s in wind_data) / len(wind_data)
            avg_wind_direction = sum(s.wind_direction for s in wind_data) / len(wind_data)
            
            # 확산 방향 (풍향 기준)
            spread_direction = avg_wind_direction
            
            # 확산 속도 계산 (풍속과 위험도 기반)
            base_spread_speed = avg_wind_speed * 0.1  # km/h
            risk_multiplier = 1 + overall_risk * 2
            spread_speed = base_spread_speed * risk_multiplier
            
            # 영향 반경 계산
            affected_radius = min(10.0, spread_speed * 2)  # 최대 10km
            
            # 대피 권고 반경
            evacuation_radius = affected_radius * 1.5  # 영향 반경의 1.5배
            
            # 신뢰도 계산
            confidence = min(0.9, len(wind_data) / 5)  # 센서 수에 따른 신뢰도
            
            return {
                "spread_direction": spread_direction,
                "spread_speed": spread_speed,
                "affected_radius": affected_radius,
                "evacuation_radius": evacuation_radius,
                "confidence": confidence,
                "wind_speed": avg_wind_speed,
                "wind_direction": avg_wind_direction
            }
            
        except Exception as e:
            logger.error(f"화재 확산 예측 실패: {str(e)}")
            return {
                "spread_direction": None,
                "spread_speed": 0.0,
                "affected_radius": 0.0,
                "evacuation_radius": 0.0,
                "confidence": 0.0
            }
    
    def _calculate_analysis_confidence(self, sensor_data: List[SensorData]) -> float:
        """분석 신뢰도 계산"""
        try:
            if not sensor_data:
                return 0.0
            
            # 센서 데이터 품질 평균
            quality_scores = [s.data_quality or 0.5 for s in sensor_data]
            avg_quality = sum(quality_scores) / len(quality_scores)
            
            # 센서 수에 따른 신뢰도
            sensor_count_factor = min(1.0, len(sensor_data) / 10)
            
            # 센서 타입 다양성
            sensor_types = set(s.sensor_type for s in sensor_data)
            diversity_factor = min(1.0, len(sensor_types) / 5)
            
            # 종합 신뢰도
            confidence = (avg_quality + sensor_count_factor + diversity_factor) / 3
            
            return min(0.99, max(0.0, confidence))
            
        except Exception as e:
            logger.error(f"분석 신뢰도 계산 실패: {str(e)}")
            return 0.0
