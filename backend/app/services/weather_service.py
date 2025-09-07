"""
기상 서비스 모듈
기상청 API를 통한 실시간 기상 데이터 수집
"""

import asyncio
import logging
import httpx
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET

from app.core.config import settings

logger = logging.getLogger(__name__)

class WeatherService:
    """기상 서비스 클래스"""
    
    def __init__(self):
        self.api_endpoint = settings.WEATHER_API_ENDPOINT
        self.api_key = settings.WEATHER_API_KEY
    
    async def get_current_weather(
        self, 
        lat: float, 
        lng: float
    ) -> Optional[Dict[str, Any]]:
        """
        현재 날씨 정보 조회
        
        Args:
            lat: 위도
            lng: 경도
            
        Returns:
            날씨 정보 딕셔너리
        """
        try:
            # 기상청 격자 좌표로 변환
            grid_coords = self._convert_to_grid_coordinates(lat, lng)
            
            # 현재 시간 기준으로 조회
            now = datetime.now()
            base_date = now.strftime("%Y%m%d")
            base_time = self._get_base_time(now)
            
            # 기상청 API 호출
            weather_data = await self._call_weather_api(
                grid_coords["nx"], 
                grid_coords["ny"], 
                base_date, 
                base_time
            )
            
            if weather_data:
                # 현재 날씨 정보 추출
                current_weather = self._extract_current_weather(weather_data)
                logger.info(f"🌤️ 날씨 데이터 수집 완료 - 위치: ({lat}, {lng})")
                return current_weather
            
            return None
            
        except Exception as e:
            logger.error(f"❌ 날씨 데이터 수집 실패: {str(e)}")
            return None
    
    async def get_weather_forecast(
        self, 
        lat: float, 
        lng: float, 
        hours: int = 24
    ) -> Optional[Dict[str, Any]]:
        """
        날씨 예보 조회
        
        Args:
            lat: 위도
            lng: 경도
            hours: 예보 시간 (시간)
            
        Returns:
            날씨 예보 딕셔너리
        """
        try:
            # 기상청 격자 좌표로 변환
            grid_coords = self._convert_to_grid_coordinates(lat, lng)
            
            # 현재 시간 기준으로 조회
            now = datetime.now()
            base_date = now.strftime("%Y%m%d")
            base_time = self._get_base_time(now)
            
            # 기상청 API 호출
            weather_data = await self._call_weather_api(
                grid_coords["nx"], 
                grid_coords["ny"], 
                base_date, 
                base_time
            )
            
            if weather_data:
                # 날씨 예보 추출
                forecast = self._extract_weather_forecast(weather_data, hours)
                logger.info(f"📊 날씨 예보 수집 완료 - {hours}시간 예보")
                return forecast
            
            return None
            
        except Exception as e:
            logger.error(f"❌ 날씨 예보 수집 실패: {str(e)}")
            return None
    
    def _convert_to_grid_coordinates(self, lat: float, lng: float) -> Dict[str, int]:
        """위경도를 기상청 격자 좌표로 변환"""
        try:
            # 기상청 격자 좌표 변환 공식
            RE = 6371.00877  # 지구 반경(km)
            GRID = 5.0       # 격자 간격(km)
            SLAT1 = 30.0     # 투영 위도1(degree)
            SLAT2 = 60.0     # 투영 위도2(degree)
            OLON = 126.0     # 기준점 경도(degree)
            OLAT = 38.0      # 기준점 위도(degree)
            XO = 43          # 기준점 X좌표(GRID)
            YO = 136         # 기준점 Y좌표(GRID)
            
            DEGRAD = 3.14159265359 / 180.0
            RADDEG = 180.0 / 3.14159265359
            
            re = RE / GRID
            slat1 = SLAT1 * DEGRAD
            slat2 = SLAT2 * DEGRAD
            olon = OLON * DEGRAD
            olat = OLAT * DEGRAD
            
            sn = np.tan(3.14159265359 * 0.25 + slat2 * 0.5) / np.tan(3.14159265359 * 0.25 + slat1 * 0.5)
            sn = np.log(np.cos(slat1) / np.cos(slat2)) / np.log(sn)
            sf = np.tan(3.14159265359 * 0.25 + slat1 * 0.5)
            sf = sf ** sn * np.cos(slat1) / sn
            ro = np.tan(3.14159265359 * 0.25 + olat * 0.5)
            ro = re * sf / ro ** sn
            
            ra = np.tan(3.14159265359 * 0.25 + lat * DEGRAD * 0.5)
            theta = lng * DEGRAD - olon
            
            if ra == 0:
                theta = 0
            else:
                theta = np.arctan2(np.sin(theta), np.cos(theta) * ra - np.sin(lat * DEGRAD) * np.cos(theta))
                theta = theta * RADDEG
            
            x = int(ra * np.sin(theta) + XO + 0.5)
            y = int(ro - ra * np.cos(theta) + YO + 0.5)
            
            return {"nx": x, "ny": y}
            
        except Exception as e:
            logger.error(f"격자 좌표 변환 실패: {str(e)}")
            return {"nx": 0, "ny": 0}
    
    def _get_base_time(self, now: datetime) -> str:
        """기상청 API 기준 시간 계산"""
        hour = now.hour
        
        if hour < 2:
            return "2300"
        elif hour < 5:
            return "0200"
        elif hour < 8:
            return "0500"
        elif hour < 11:
            return "0800"
        elif hour < 14:
            return "1100"
        elif hour < 17:
            return "1400"
        elif hour < 20:
            return "1700"
        elif hour < 23:
            return "2000"
        else:
            return "2300"
    
    async def _call_weather_api(
        self, 
        nx: int, 
        ny: int, 
        base_date: str, 
        base_time: str
    ) -> Optional[Dict[str, Any]]:
        """기상청 API 호출"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.api_endpoint}/getVilageFcst",
                    params={
                        "serviceKey": self.api_key,
                        "numOfRows": 1000,
                        "pageNo": 1,
                        "dataType": "XML",
                        "base_date": base_date,
                        "base_time": base_time,
                        "nx": nx,
                        "ny": ny
                    },
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    # XML 파싱
                    root = ET.fromstring(response.text)
                    
                    # 응답 코드 확인
                    result_code = root.find(".//resultCode")
                    if result_code is not None and result_code.text == "00":
                        # 데이터 추출
                        items = root.findall(".//item")
                        weather_data = {}
                        
                        for item in items:
                            category = item.find("category")
                            fcst_value = item.find("fcstValue")
                            fcst_time = item.find("fcstTime")
                            
                            if category is not None and fcst_value is not None and fcst_time is not None:
                                key = f"{category.text}_{fcst_time.text}"
                                weather_data[key] = fcst_value.text
                        
                        return weather_data
                    else:
                        logger.error(f"기상청 API 오류: {result_code.text if result_code is not None else 'Unknown'}")
                        return None
                else:
                    logger.error(f"기상청 API 호출 실패: {response.status_code}")
                    return None
                    
        except Exception as e:
            logger.error(f"기상청 API 호출 중 오류: {str(e)}")
            return None
    
    def _extract_current_weather(self, weather_data: Dict[str, Any]) -> Dict[str, Any]:
        """현재 날씨 정보 추출"""
        try:
            # 현재 시간 기준으로 가장 가까운 데이터 찾기
            current_hour = datetime.now().hour
            target_time = f"{current_hour:02d}00"
            
            # 온도 (T1H)
            temperature = None
            for key, value in weather_data.items():
                if key.startswith("T1H_") and key.endswith(target_time):
                    temperature = float(value)
                    break
            
            # 습도 (REH)
            humidity = None
            for key, value in weather_data.items():
                if key.startswith("REH_") and key.endswith(target_time):
                    humidity = float(value)
                    break
            
            # 풍속 (WSD)
            wind_speed = None
            for key, value in weather_data.items():
                if key.startswith("WSD_") and key.endswith(target_time):
                    wind_speed = float(value)
                    break
            
            # 풍향 (WAV)
            wind_direction = None
            for key, value in weather_data.items():
                if key.startswith("WAV_") and key.endswith(target_time):
                    wind_direction = float(value)
                    break
            
            # 기압 (PTY)
            air_pressure = None
            for key, value in weather_data.items():
                if key.startswith("PTY_") and key.endswith(target_time):
                    air_pressure = float(value)
                    break
            
            # 강수형태 (PTY)
            precipitation_type = None
            for key, value in weather_data.items():
                if key.startswith("PTY_") and key.endswith(target_time):
                    precipitation_type = int(value)
                    break
            
            return {
                "temperature": temperature,
                "humidity": humidity,
                "wind_speed": wind_speed,
                "wind_direction": wind_direction,
                "air_pressure": air_pressure,
                "precipitation_type": precipitation_type,
                "timestamp": datetime.now().isoformat(),
                "source": "기상청"
            }
            
        except Exception as e:
            logger.error(f"현재 날씨 정보 추출 실패: {str(e)}")
            return {}
    
    def _extract_weather_forecast(
        self, 
        weather_data: Dict[str, Any], 
        hours: int
    ) -> Dict[str, Any]:
        """날씨 예보 추출"""
        try:
            forecast = {
                "hourly": [],
                "summary": {},
                "timestamp": datetime.now().isoformat()
            }
            
            # 시간별 예보 데이터 정리
            hourly_data = {}
            for key, value in weather_data.items():
                parts = key.split("_")
                if len(parts) >= 2:
                    category = parts[0]
                    time = parts[1]
                    
                    if time not in hourly_data:
                        hourly_data[time] = {}
                    hourly_data[time][category] = value
            
            # 시간별 데이터 정렬 및 추출
            sorted_times = sorted(hourly_data.keys())
            for time in sorted_times[:hours]:
                data = hourly_data[time]
                hour_forecast = {
                    "time": time,
                    "temperature": float(data.get("T1H", 0)),
                    "humidity": float(data.get("REH", 0)),
                    "wind_speed": float(data.get("WSD", 0)),
                    "wind_direction": float(data.get("WAV", 0)),
                    "air_pressure": float(data.get("PTY", 0)),
                    "precipitation_type": int(data.get("PTY", 0))
                }
                forecast["hourly"].append(hour_forecast)
            
            # 요약 정보 생성
            if forecast["hourly"]:
                temps = [h["temperature"] for h in forecast["hourly"] if h["temperature"]]
                humidities = [h["humidity"] for h in forecast["hourly"] if h["humidity"]]
                wind_speeds = [h["wind_speed"] for h in forecast["hourly"] if h["wind_speed"]]
                
                forecast["summary"] = {
                    "max_temperature": max(temps) if temps else None,
                    "min_temperature": min(temps) if temps else None,
                    "avg_humidity": sum(humidities) / len(humidities) if humidities else None,
                    "max_wind_speed": max(wind_speeds) if wind_speeds else None,
                    "forecast_hours": len(forecast["hourly"])
                }
            
            return forecast
            
        except Exception as e:
            logger.error(f"날씨 예보 추출 실패: {str(e)}")
            return {"hourly": [], "summary": {}, "timestamp": datetime.now().isoformat()}

# numpy import 추가
import numpy as np
