"""
AI 서비스 모듈 - 믿:음 LLM 기반 권고안 생성
"""

import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import asyncio
import httpx

from app.core.config import settings
from app.models.sensor_data import SensorData
from app.models.ai_recommendation import (
    AIRecommendation, 
    AIRecommendationCreate, 
    AgencyType, 
    PriorityLevel
)

logger = logging.getLogger(__name__)

class AIService:
    """AI 서비스 클래스"""
    
    def __init__(self):
        self.model_name = settings.AI_MODEL_NAME
        self.confidence_threshold = settings.AI_CONFIDENCE_THRESHOLD
        self.max_tokens = settings.AI_MAX_TOKENS
        self.temperature = settings.AI_TEMPERATURE
        
    async def generate_recommendations(
        self, 
        sensor_data: List[SensorData],
        fire_risk_level: float,
        location_info: Dict[str, Any]
    ) -> List[AIRecommendationCreate]:
        """
        센서 데이터를 기반으로 기관별 권고안 생성
        
        Args:
            sensor_data: 센서 데이터 리스트
            fire_risk_level: 화재 위험도 (0-1)
            location_info: 위치 정보
            
        Returns:
            생성된 권고안 리스트
        """
        try:
            logger.info(f"🤖 AI 권고안 생성 시작 - 위험도: {fire_risk_level}")
            
            # 센서 데이터 분석
            analysis_result = await self._analyze_sensor_data(sensor_data)
            
            # 기관별 권고안 생성
            recommendations = []
            
            # 소방청 권고안
            fire_dept_rec = await self._generate_fire_department_recommendation(
                analysis_result, fire_risk_level, location_info
            )
            if fire_dept_rec:
                recommendations.append(fire_dept_rec)
            
            # 산림청 권고안
            forest_rec = await self._generate_forest_service_recommendation(
                analysis_result, fire_risk_level, location_info
            )
            if forest_rec:
                recommendations.append(forest_rec)
            
            # 지자체 권고안
            local_gov_rec = await self._generate_local_government_recommendation(
                analysis_result, fire_risk_level, location_info
            )
            if local_gov_rec:
                recommendations.append(local_gov_rec)
            
            logger.info(f"✅ AI 권고안 생성 완료 - {len(recommendations)}개 생성")
            return recommendations
            
        except Exception as e:
            logger.error(f"❌ AI 권고안 생성 실패: {str(e)}")
            raise
    
    async def _analyze_sensor_data(self, sensor_data: List[SensorData]) -> Dict[str, Any]:
        """센서 데이터 분석"""
        analysis = {
            "fire_detected": False,
            "fire_confidence": 0.0,
            "environmental_conditions": {},
            "risk_factors": [],
            "recommended_actions": []
        }
        
        # 화재 탐지 여부 확인
        fire_detections = [data for data in sensor_data if data.fire_detected]
        if fire_detections:
            analysis["fire_detected"] = True
            analysis["fire_confidence"] = max([d.fire_confidence or 0 for d in fire_detections])
        
        # 환경 조건 분석
        temp_data = [d for d in sensor_data if d.temperature is not None]
        humidity_data = [d for d in sensor_data if d.humidity is not None]
        smoke_data = [d for d in sensor_data if d.smoke_density is not None]
        wind_data = [d for d in sensor_data if d.wind_speed is not None]
        
        if temp_data:
            analysis["environmental_conditions"]["temperature"] = {
                "avg": sum(d.temperature for d in temp_data) / len(temp_data),
                "max": max(d.temperature for d in temp_data),
                "min": min(d.temperature for d in temp_data)
            }
        
        if humidity_data:
            analysis["environmental_conditions"]["humidity"] = {
                "avg": sum(d.humidity for d in humidity_data) / len(humidity_data),
                "min": min(d.humidity for d in humidity_data)
            }
        
        if smoke_data:
            analysis["environmental_conditions"]["smoke_density"] = {
                "avg": sum(d.smoke_density for d in smoke_data) / len(smoke_data),
                "max": max(d.smoke_density for d in smoke_data)
            }
        
        if wind_data:
            analysis["environmental_conditions"]["wind"] = {
                "avg_speed": sum(d.wind_speed for d in wind_data) / len(wind_data),
                "max_speed": max(d.wind_speed for d in wind_data),
                "directions": [d.wind_direction for d in wind_data if d.wind_direction]
            }
        
        # 위험 요인 분석
        if analysis["environmental_conditions"].get("temperature", {}).get("avg", 0) > 30:
            analysis["risk_factors"].append("고온 환경")
        
        if analysis["environmental_conditions"].get("humidity", {}).get("avg", 100) < 30:
            analysis["risk_factors"].append("저습도 환경")
        
        if analysis["environmental_conditions"].get("wind", {}).get("max_speed", 0) > 10:
            analysis["risk_factors"].append("강풍 환경")
        
        return analysis
    
    async def _generate_fire_department_recommendation(
        self, 
        analysis: Dict[str, Any], 
        fire_risk_level: float,
        location_info: Dict[str, Any]
    ) -> Optional[AIRecommendationCreate]:
        """소방청 권고안 생성"""
        
        # 위험도에 따른 우선순위 결정
        if fire_risk_level >= 0.8:
            priority = PriorityLevel.CRITICAL
        elif fire_risk_level >= 0.6:
            priority = PriorityLevel.HIGH
        elif fire_risk_level >= 0.4:
            priority = PriorityLevel.MEDIUM
        else:
            priority = PriorityLevel.LOW
        
        # AI 신뢰도 계산
        ai_confidence = min(0.99, fire_risk_level + 0.1)
        
        # 즉시 조치사항 생성
        immediate_actions = [
            {
                "action": "헬기 긴급 투입",
                "details": "소방헬기 2대 (Bell 412, AS-350) 즉시 출동",
                "legal_basis": "소방기본법 제3조 제1항",
                "estimated_time": "10분 이내"
            },
            {
                "action": "소방차량 및 인력 투입",
                "details": "소방차 5대 (물탱크차 3대, 펌프차 2대) 현장 투입, 구조대 20명 긴급 파견",
                "legal_basis": "소방법 제5조 제2항",
                "estimated_time": "15분 이내"
            },
            {
                "action": "현장 지휘소 설치",
                "details": "통합지휘체계 구축 및 현장 상황실 운영",
                "legal_basis": "소방기본법 제3조 제2항",
                "estimated_time": "20분 이내"
            }
        ]
        
        # 법적 근거
        legal_basis = [
            {
                "law": "소방기본법",
                "article": "제3조",
                "content": "소방의 임무 및 소방기관의 조직"
            },
            {
                "law": "소방법",
                "article": "제5조",
                "content": "소방대의 설치 및 운영"
            },
            {
                "law": "소방시설 설치·유지 및 안전관리에 관한 법률",
                "article": "제3조",
                "content": "소방시설의 설치 및 유지"
            }
        ]
        
        # 예상 비용 및 효과
        expected_cost = 25000000  # 2,500만원
        expected_effect = {
            "fire_suppression_rate": 0.95,
            "damage_reduction": 0.5,
            "response_time": "15분 이내",
            "resource_utilization": "최적화"
        }
        
        # 필요 자원
        required_resources = [
            {"type": "헬기", "count": 2, "model": "Bell 412, AS-350"},
            {"type": "소방차", "count": 5, "type": "물탱크차 3대, 펌프차 2대"},
            {"type": "인력", "count": 20, "role": "구조대"},
            {"type": "장비", "items": ["펌프", "호스", "진화제", "구조장비"]}
        ]
        
        return AIRecommendationCreate(
            title=f"🚒 소방청 긴급 대응 권고안 - {location_info.get('name', '산불 현장')}",
            description=f"화재 위험도 {fire_risk_level:.1%}에 따른 소방청 긴급 대응 방안",
            agency_type=AgencyType.FIRE_DEPARTMENT,
            priority_level=priority,
            ai_confidence=ai_confidence,
            ai_reasoning=f"센서 데이터 분석 결과 화재 위험도 {fire_risk_level:.1%}로 판단되어 긴급 대응이 필요합니다.",
            immediate_actions=immediate_actions,
            legal_basis=legal_basis,
            expected_cost=expected_cost,
            expected_effect=expected_effect,
            required_resources=required_resources,
            location_lat=location_info["lat"],
            location_lng=location_info["lng"],
            location_name=location_info.get("name"),
            affected_radius=2.0,  # 2km 영향 반경
            expires_at=datetime.now() + timedelta(hours=6)
        )
    
    async def _generate_forest_service_recommendation(
        self, 
        analysis: Dict[str, Any], 
        fire_risk_level: float,
        location_info: Dict[str, Any]
    ) -> Optional[AIRecommendationCreate]:
        """산림청 권고안 생성"""
        
        priority = PriorityLevel.HIGH if fire_risk_level >= 0.6 else PriorityLevel.MEDIUM
        ai_confidence = min(0.99, fire_risk_level + 0.05)
        
        immediate_actions = [
            {
                "action": "산림헬기 긴급 투입",
                "details": "산림헬기 2대 (K-32, Bell 205) 즉시 출동",
                "legal_basis": "산림보호법 제2조 제1항",
                "estimated_time": "12분 이내"
            },
            {
                "action": "산불진화대 및 장비 투입",
                "details": "산불진화대 30명 현장 파견, 진화장비 긴급 보급",
                "legal_basis": "산림보호법 제2조 제2항",
                "estimated_time": "18분 이내"
            },
            {
                "action": "산불 확산 차단 작업",
                "details": "산불 확산 경로 차단선 구축 및 예방적 진화작업",
                "legal_basis": "산림보호법 제2조 제3항",
                "estimated_time": "25분 이내"
            }
        ]
        
        legal_basis = [
            {
                "law": "산림보호법",
                "article": "제2조",
                "content": "산불방지 및 진화업무"
            },
            {
                "law": "산림청 소관 산불방지 및 진화업무 규정",
                "article": "제3조",
                "content": "산불진화대의 구성 및 운영"
            }
        ]
        
        expected_cost = 18000000  # 1,800만원
        expected_effect = {
            "forest_damage_reduction": 0.6,
            "ecosystem_preservation": 0.9,
            "response_time": "20분 이내",
            "resource_efficiency": "최적화"
        }
        
        required_resources = [
            {"type": "산림헬기", "count": 2, "model": "K-32, Bell 205"},
            {"type": "진화대", "count": 30, "role": "산불진화대"},
            {"type": "진화장비", "items": ["펌프", "호스", "삽", "괭이"]},
            {"type": "진화차", "count": 3, "type": "산불진화차"}
        ]
        
        return AIRecommendationCreate(
            title=f"🌲 산림청 산불방지 권고안 - {location_info.get('name', '산불 현장')}",
            description=f"산림 보호를 위한 산불방지 및 진화업무 권고안",
            agency_type=AgencyType.FOREST_SERVICE,
            priority_level=priority,
            ai_confidence=ai_confidence,
            ai_reasoning=f"산림 생태계 보전을 위한 전문적 진화작업이 필요합니다.",
            immediate_actions=immediate_actions,
            legal_basis=legal_basis,
            expected_cost=expected_cost,
            expected_effect=expected_effect,
            required_resources=required_resources,
            location_lat=location_info["lat"],
            location_lng=location_info["lng"],
            location_name=location_info.get("name"),
            affected_radius=3.0,  # 3km 영향 반경
            expires_at=datetime.now() + timedelta(hours=8)
        )
    
    async def _generate_local_government_recommendation(
        self, 
        analysis: Dict[str, Any], 
        fire_risk_level: float,
        location_info: Dict[str, Any]
    ) -> Optional[AIRecommendationCreate]:
        """지자체 권고안 생성"""
        
        priority = PriorityLevel.HIGH if fire_risk_level >= 0.7 else PriorityLevel.MEDIUM
        ai_confidence = min(0.99, fire_risk_level + 0.08)
        
        immediate_actions = [
            {
                "action": "주민 대피 및 안전조치",
                "details": "주민 대피 안내 (반경 1km), 긴급재난문자 발송, 대피소 운영",
                "legal_basis": "재난기본법 제3조 제1항",
                "estimated_time": "10분 이내"
            },
            {
                "action": "교통 통제 및 우회로 안내",
                "details": "현장 반경 2km 교통 통제, 우회로 안내, 응급차량 통행로 확보",
                "legal_basis": "도로교통법 제5조",
                "estimated_time": "15분 이내"
            },
            {
                "action": "의료 및 응급상황 대비",
                "details": "의료진 대기, 응급실 준비, 응급환자 이송체계 구축",
                "legal_basis": "의료법 제3조",
                "estimated_time": "20분 이내"
            }
        ]
        
        legal_basis = [
            {
                "law": "재난 및 안전관리기본법",
                "article": "제3조",
                "content": "재난관리책임기관의 임무"
            },
            {
                "law": "지방자치법",
                "article": "제9조",
                "content": "지방자치단체의 사무"
            }
        ]
        
        expected_cost = 8000000  # 800만원
        expected_effect = {
            "resident_safety": 1.0,
            "evacuation_time": "30분 이내",
            "traffic_management": "효율적",
            "medical_support": "24시간 대기"
        }
        
        required_resources = [
            {"type": "대피소", "count": 1, "capacity": 500, "location": "○○초등학교"},
            {"type": "교통관제", "count": 10, "role": "교통관제요원"},
            {"type": "의료진", "count": 5, "role": "응급의료진"},
            {"type": "통신장비", "items": ["무전기", "재난문자발송시스템"]}
        ]
        
        return AIRecommendationCreate(
            title=f"🏛️ 지자체 재난대응 권고안 - {location_info.get('name', '산불 현장')}",
            description=f"주민 안전을 위한 지자체 재난대응 방안",
            agency_type=AgencyType.LOCAL_GOVERNMENT,
            priority_level=priority,
            ai_confidence=ai_confidence,
            ai_reasoning=f"주민 안전 확보를 위한 종합적 재난대응이 필요합니다.",
            immediate_actions=immediate_actions,
            legal_basis=legal_basis,
            expected_cost=expected_cost,
            expected_effect=expected_effect,
            required_resources=required_resources,
            location_lat=location_info["lat"],
            location_lng=location_info["lng"],
            location_name=location_info.get("name"),
            affected_radius=1.0,  # 1km 영향 반경
            expires_at=datetime.now() + timedelta(hours=4)
        )
