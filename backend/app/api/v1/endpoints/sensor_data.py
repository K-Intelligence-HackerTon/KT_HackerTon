"""
센서 데이터 API 엔드포인트
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.sensor_data import SensorData, SensorDataCreate, SensorDataResponse, SensorDataFilter

router = APIRouter()

@router.post("/", response_model=SensorDataResponse)
async def create_sensor_data(
    sensor_data: SensorDataCreate,
    db: Session = Depends(get_db)
):
    """센서 데이터 생성"""
    try:
        db_sensor_data = SensorData(**sensor_data.dict())
        db.add(db_sensor_data)
        db.commit()
        db.refresh(db_sensor_data)
        return db_sensor_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"센서 데이터 생성 실패: {str(e)}")

@router.get("/", response_model=List[SensorDataResponse])
async def get_sensor_data(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    sensor_type: Optional[str] = None,
    fire_detected: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """센서 데이터 목록 조회"""
    try:
        query = db.query(SensorData)
        
        if sensor_type:
            query = query.filter(SensorData.sensor_type == sensor_type)
        if fire_detected is not None:
            query = query.filter(SensorData.fire_detected == fire_detected)
        
        sensor_data = query.offset(skip).limit(limit).all()
        return sensor_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"센서 데이터 조회 실패: {str(e)}")

@router.get("/{sensor_data_id}", response_model=SensorDataResponse)
async def get_sensor_data_by_id(
    sensor_data_id: int,
    db: Session = Depends(get_db)
):
    """특정 센서 데이터 조회"""
    try:
        sensor_data = db.query(SensorData).filter(SensorData.id == sensor_data_id).first()
        if not sensor_data:
            raise HTTPException(status_code=404, detail="센서 데이터를 찾을 수 없습니다")
        return sensor_data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"센서 데이터 조회 실패: {str(e)}")
