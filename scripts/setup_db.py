#!/usr/bin/env python3
"""
데이터베이스 초기화 스크립트
"""

import asyncio
import sys
import os

# 프로젝트 루트를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app.core.database import init_db, engine
from backend.app.models.sensor_data import Base as SensorDataBase
from backend.app.models.ai_recommendation import Base as AIRecommendationBase

async def setup_database():
    """데이터베이스 설정"""
    try:
        print("🔧 데이터베이스 초기화 시작...")
        
        # 모든 테이블 생성
        SensorDataBase.metadata.create_all(bind=engine)
        AIRecommendationBase.metadata.create_all(bind=engine)
        
        print("✅ 데이터베이스 초기화 완료")
        
        # 샘플 데이터 삽입 (선택사항)
        print("📊 샘플 데이터 삽입 중...")
        await insert_sample_data()
        
        print("🎉 데이터베이스 설정 완료!")
        
    except Exception as e:
        print(f"❌ 데이터베이스 설정 실패: {str(e)}")
        sys.exit(1)

async def insert_sample_data():
    """샘플 데이터 삽입"""
    try:
        from backend.app.core.database import SessionLocal
        from backend.app.models.sensor_data import SensorData, SensorType
        from backend.app.models.ai_recommendation import AIRecommendation, AgencyType, PriorityLevel, RecommendationStatus
        from datetime import datetime, timedelta
        
        db = SessionLocal()
        
        # 샘플 센서 데이터
        sample_sensor_data = [
            SensorData(
                sensor_id="cctv_001",
                sensor_type=SensorType.CCTV,
                location_lat=37.5665,
                location_lng=127.9780,
                location_name="양평군 용문면",
                fire_detected=True,
                fire_confidence=0.95,
                data_quality=0.9,
                created_at=datetime.now() - timedelta(minutes=30)
            ),
            SensorData(
                sensor_id="iot_001",
                sensor_type=SensorType.TEMPERATURE,
                location_lat=37.5665,
                location_lng=127.9780,
                location_name="양평군 용문면",
                temperature=32.5,
                humidity=25.0,
                data_quality=0.85,
                created_at=datetime.now() - timedelta(minutes=25)
            ),
            SensorData(
                sensor_id="drone_001",
                sensor_type=SensorType.DRONE,
                location_lat=37.5512,
                location_lng=127.9880,
                location_name="양평군 서종면",
                fire_detected=False,
                fire_confidence=0.0,
                data_quality=0.92,
                created_at=datetime.now() - timedelta(minutes=20)
            )
        ]
        
        for sensor in sample_sensor_data:
            db.add(sensor)
        
        # 샘플 AI 권고안
        sample_recommendations = [
            AIRecommendation(
                recommendation_id="REC_001",
                title="🚒 소방청 긴급 대응 권고안 - 양평군 용문면",
                description="화재 위험도 87.3%에 따른 소방청 긴급 대응 방안",
                agency_type=AgencyType.FIRE_DEPARTMENT,
                priority_level=PriorityLevel.HIGH,
                ai_confidence=0.979,
                status=RecommendationStatus.PENDING,
                location_lat=37.5665,
                location_lng=127.9780,
                location_name="양평군 용문면",
                affected_radius=2.0,
                created_at=datetime.now() - timedelta(minutes=15)
            ),
            AIRecommendation(
                recommendation_id="REC_002",
                title="🌲 산림청 산불방지 권고안 - 양평군 용문면",
                description="산림 보호를 위한 산불방지 및 진화업무 권고안",
                agency_type=AgencyType.FOREST_SERVICE,
                priority_level=PriorityLevel.HIGH,
                ai_confidence=0.968,
                status=RecommendationStatus.PENDING,
                location_lat=37.5665,
                location_lng=127.9780,
                location_name="양평군 용문면",
                affected_radius=3.0,
                created_at=datetime.now() - timedelta(minutes=10)
            ),
            AIRecommendation(
                recommendation_id="REC_003",
                title="🏛️ 지자체 재난대응 권고안 - 양평군 용문면",
                description="주민 안전을 위한 지자체 재난대응 방안",
                agency_type=AgencyType.LOCAL_GOVERNMENT,
                priority_level=PriorityLevel.HIGH,
                ai_confidence=0.981,
                status=RecommendationStatus.APPROVED,
                location_lat=37.5665,
                location_lng=127.9780,
                location_name="양평군 용문면",
                affected_radius=1.0,
                created_at=datetime.now() - timedelta(minutes=5),
                approved_by="관리자",
                approved_at=datetime.now() - timedelta(minutes=2)
            )
        ]
        
        for rec in sample_recommendations:
            db.add(rec)
        
        db.commit()
        print("✅ 샘플 데이터 삽입 완료")
        
    except Exception as e:
        print(f"❌ 샘플 데이터 삽입 실패: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(setup_database())
