"""
데이터 수집 서비스 모듈
Vision AI, IoT 센서, 기상 데이터 수집
"""

import asyncio
import logging
import httpx
import json
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import cv2
import numpy as np
from PIL import Image
import io
import base64

from app.core.config import settings
from app.models.sensor_data import SensorData, SensorDataCreate, SensorType
from app.services.vision_ai_service import VisionAIService
from app.services.weather_service import WeatherService

logger = logging.getLogger(__name__)

class DataCollectionService:
    """데이터 수집 서비스 클래스"""
    
    def __init__(self):
        self.vision_ai_service = VisionAIService()
        self.weather_service = WeatherService()
        self.sensor_endpoints = {
            "kt_gigai": settings.VISION_AI_ENDPOINT,
            "iot_sensors": settings.IOT_SENSOR_ENDPOINT,
            "weather": settings.WEATHER_API_ENDPOINT
        }
    
    async def collect_all_data(
        self, 
        location: Dict[str, float],
        radius_km: float = 5.0
    ) -> List[SensorDataCreate]:
        """
        모든 데이터 소스에서 데이터 수집
        
        Args:
            location: {"lat": float, "lng": float} 위치 정보
            radius_km: 수집 반경 (km)
            
        Returns:
            수집된 센서 데이터 리스트
        """
        try:
            logger.info(f"📡 데이터 수집 시작 - 위치: {location}, 반경: {radius_km}km")
            
            all_sensor_data = []
            
            # 1. Vision AI 데이터 수집 (CCTV, 드론, 위성)
            vision_data = await self._collect_vision_data(location, radius_km)
            all_sensor_data.extend(vision_data)
            
            # 2. IoT 센서 데이터 수집
            iot_data = await self._collect_iot_sensor_data(location, radius_km)
            all_sensor_data.extend(iot_data)
            
            # 3. 기상 데이터 수집
            weather_data = await self._collect_weather_data(location)
            all_sensor_data.extend(weather_data)
            
            logger.info(f"✅ 데이터 수집 완료 - 총 {len(all_sensor_data)}개 데이터 수집")
            return all_sensor_data
            
        except Exception as e:
            logger.error(f"❌ 데이터 수집 실패: {str(e)}")
            raise
    
    async def _collect_vision_data(
        self, 
        location: Dict[str, float], 
        radius_km: float
    ) -> List[SensorDataCreate]:
        """Vision AI 데이터 수집 (CCTV, 드론, 위성)"""
        vision_data = []
        
        try:
            # KT 기가아이즈 CCTV 데이터 수집
            cctv_data = await self._collect_cctv_data(location, radius_km)
            vision_data.extend(cctv_data)
            
            # 드론 데이터 수집
            drone_data = await self._collect_drone_data(location, radius_km)
            vision_data.extend(drone_data)
            
            # 위성 데이터 수집
            satellite_data = await self._collect_satellite_data(location, radius_km)
            vision_data.extend(satellite_data)
            
        except Exception as e:
            logger.error(f"Vision AI 데이터 수집 실패: {str(e)}")
        
        return vision_data
    
    async def _collect_cctv_data(
        self, 
        location: Dict[str, float], 
        radius_km: float
    ) -> List[SensorDataCreate]:
        """CCTV 데이터 수집"""
        cctv_data = []
        
        try:
            async with httpx.AsyncClient() as client:
                # KT 기가아이즈 API 호출
                response = await client.get(
                    f"{self.sensor_endpoints['kt_gigai']}/cctv/nearby",
                    params={
                        "lat": location["lat"],
                        "lng": location["lng"],
                        "radius": radius_km,
                        "api_key": settings.VISION_AI_API_KEY
                    },
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    cctv_list = response.json().get("data", [])
                    
                    for cctv in cctv_list:
                        # 이미지 분석
                        image_analysis = await self.vision_ai_service.analyze_image(
                            cctv.get("image_url"),
                            cctv.get("image_data")
                        )
                        
                        sensor_data = SensorDataCreate(
                            sensor_id=f"cctv_{cctv['id']}",
                            sensor_type=SensorType.CCTV,
                            location_lat=cctv["lat"],
                            location_lng=cctv["lng"],
                            location_name=cctv.get("name"),
                            image_url=cctv.get("image_url"),
                            image_analysis=image_analysis,
                            fire_detected=image_analysis.get("fire_detected", False),
                            fire_confidence=image_analysis.get("fire_confidence", 0.0),
                            raw_data=cctv,
                            data_quality=image_analysis.get("data_quality", 0.8)
                        )
                        cctv_data.append(sensor_data)
                        
        except Exception as e:
            logger.error(f"CCTV 데이터 수집 실패: {str(e)}")
        
        return cctv_data
    
    async def _collect_drone_data(
        self, 
        location: Dict[str, float], 
        radius_km: float
    ) -> List[SensorDataCreate]:
        """드론 데이터 수집"""
        drone_data = []
        
        try:
            async with httpx.AsyncClient() as client:
                # 드론 API 호출
                response = await client.get(
                    f"{self.sensor_endpoints['kt_gigai']}/drone/nearby",
                    params={
                        "lat": location["lat"],
                        "lng": location["lng"],
                        "radius": radius_km,
                        "api_key": settings.VISION_AI_API_KEY
                    },
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    drone_list = response.json().get("data", [])
                    
                    for drone in drone_list:
                        # 드론 이미지 분석
                        image_analysis = await self.vision_ai_service.analyze_image(
                            drone.get("image_url"),
                            drone.get("image_data")
                        )
                        
                        sensor_data = SensorDataCreate(
                            sensor_id=f"drone_{drone['id']}",
                            sensor_type=SensorType.DRONE,
                            location_lat=drone["lat"],
                            location_lng=drone["lng"],
                            location_name=drone.get("name"),
                            image_url=drone.get("image_url"),
                            image_analysis=image_analysis,
                            fire_detected=image_analysis.get("fire_detected", False),
                            fire_confidence=image_analysis.get("fire_confidence", 0.0),
                            raw_data=drone,
                            data_quality=image_analysis.get("data_quality", 0.9)
                        )
                        drone_data.append(sensor_data)
                        
        except Exception as e:
            logger.error(f"드론 데이터 수집 실패: {str(e)}")
        
        return drone_data
    
    async def _collect_satellite_data(
        self, 
        location: Dict[str, float], 
        radius_km: float
    ) -> List[SensorDataCreate]:
        """위성 데이터 수집"""
        satellite_data = []
        
        try:
            async with httpx.AsyncClient() as client:
                # 위성 API 호출
                response = await client.get(
                    f"{self.sensor_endpoints['kt_gigai']}/satellite/nearby",
                    params={
                        "lat": location["lat"],
                        "lng": location["lng"],
                        "radius": radius_km,
                        "api_key": settings.VISION_AI_API_KEY
                    },
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    satellite_list = response.json().get("data", [])
                    
                    for satellite in satellite_list:
                        # 위성 이미지 분석
                        image_analysis = await self.vision_ai_service.analyze_image(
                            satellite.get("image_url"),
                            satellite.get("image_data")
                        )
                        
                        sensor_data = SensorDataCreate(
                            sensor_id=f"satellite_{satellite['id']}",
                            sensor_type=SensorType.SATELLITE,
                            location_lat=satellite["lat"],
                            location_lng=satellite["lng"],
                            location_name=satellite.get("name"),
                            image_url=satellite.get("image_url"),
                            image_analysis=image_analysis,
                            fire_detected=image_analysis.get("fire_detected", False),
                            fire_confidence=image_analysis.get("fire_confidence", 0.0),
                            raw_data=satellite,
                            data_quality=image_analysis.get("data_quality", 0.85)
                        )
                        satellite_data.append(sensor_data)
                        
        except Exception as e:
            logger.error(f"위성 데이터 수집 실패: {str(e)}")
        
        return satellite_data
    
    async def _collect_iot_sensor_data(
        self, 
        location: Dict[str, float], 
        radius_km: float
    ) -> List[SensorDataCreate]:
        """IoT 센서 데이터 수집"""
        iot_data = []
        
        try:
            async with httpx.AsyncClient() as client:
                # IoT 센서 API 호출
                response = await client.get(
                    f"{self.sensor_endpoints['iot_sensors']}/sensors/nearby",
                    params={
                        "lat": location["lat"],
                        "lng": location["lng"],
                        "radius": radius_km,
                        "api_key": settings.IOT_SENSOR_API_KEY
                    },
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    sensor_list = response.json().get("data", [])
                    
                    for sensor in sensor_list:
                        sensor_data = SensorDataCreate(
                            sensor_id=f"iot_{sensor['id']}",
                            sensor_type=SensorType(sensor["type"]),
                            location_lat=sensor["lat"],
                            location_lng=sensor["lng"],
                            location_name=sensor.get("name"),
                            temperature=sensor.get("temperature"),
                            humidity=sensor.get("humidity"),
                            smoke_density=sensor.get("smoke_density"),
                            wind_speed=sensor.get("wind_speed"),
                            wind_direction=sensor.get("wind_direction"),
                            air_pressure=sensor.get("air_pressure"),
                            visibility=sensor.get("visibility"),
                            raw_data=sensor,
                            data_quality=sensor.get("data_quality", 0.9)
                        )
                        iot_data.append(sensor_data)
                        
        except Exception as e:
            logger.error(f"IoT 센서 데이터 수집 실패: {str(e)}")
        
        return iot_data
    
    async def _collect_weather_data(
        self, 
        location: Dict[str, float]
    ) -> List[SensorDataCreate]:
        """기상 데이터 수집"""
        weather_data = []
        
        try:
            # 기상청 API에서 현재 날씨 데이터 수집
            weather_info = await self.weather_service.get_current_weather(
                location["lat"], location["lng"]
            )
            
            if weather_info:
                # 온도 센서 데이터
                temp_sensor = SensorDataCreate(
                    sensor_id="weather_temp",
                    sensor_type=SensorType.TEMPERATURE,
                    location_lat=location["lat"],
                    location_lng=location["lng"],
                    location_name="기상청",
                    temperature=weather_info.get("temperature"),
                    raw_data=weather_info,
                    data_quality=0.95
                )
                weather_data.append(temp_sensor)
                
                # 습도 센서 데이터
                humidity_sensor = SensorDataCreate(
                    sensor_id="weather_humidity",
                    sensor_type=SensorType.HUMIDITY,
                    location_lat=location["lat"],
                    location_lng=location["lng"],
                    location_name="기상청",
                    humidity=weather_info.get("humidity"),
                    raw_data=weather_info,
                    data_quality=0.95
                )
                weather_data.append(humidity_sensor)
                
                # 풍속 센서 데이터
                wind_sensor = SensorDataCreate(
                    sensor_id="weather_wind",
                    sensor_type=SensorType.WIND_SPEED,
                    location_lat=location["lat"],
                    location_lng=location["lng"],
                    location_name="기상청",
                    wind_speed=weather_info.get("wind_speed"),
                    wind_direction=weather_info.get("wind_direction"),
                    raw_data=weather_info,
                    data_quality=0.95
                )
                weather_data.append(wind_sensor)
                
                # 기압 센서 데이터
                pressure_sensor = SensorDataCreate(
                    sensor_id="weather_pressure",
                    sensor_type=SensorType.AIR_PRESSURE,
                    location_lat=location["lat"],
                    location_lng=location["lng"],
                    location_name="기상청",
                    air_pressure=weather_info.get("air_pressure"),
                    raw_data=weather_info,
                    data_quality=0.95
                )
                weather_data.append(pressure_sensor)
                
        except Exception as e:
            logger.error(f"기상 데이터 수집 실패: {str(e)}")
        
        return weather_data
    
    async def start_continuous_collection(
        self, 
        location: Dict[str, float],
        interval_seconds: int = 30
    ):
        """지속적인 데이터 수집 시작"""
        logger.info(f"🔄 지속적 데이터 수집 시작 - 간격: {interval_seconds}초")
        
        while True:
            try:
                # 데이터 수집
                sensor_data = await self.collect_all_data(location)
                
                # 데이터베이스에 저장 (여기서는 로그만 출력)
                logger.info(f"📊 수집된 데이터: {len(sensor_data)}개")
                
                # 다음 수집까지 대기
                await asyncio.sleep(interval_seconds)
                
            except Exception as e:
                logger.error(f"지속적 데이터 수집 오류: {str(e)}")
                await asyncio.sleep(interval_seconds)
