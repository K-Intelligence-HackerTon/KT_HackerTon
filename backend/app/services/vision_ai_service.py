"""
Vision AI 서비스 모듈
KT 기가아이즈, 드론, 위성 이미지 분석
"""

import asyncio
import logging
import httpx
import cv2
import numpy as np
from PIL import Image
import io
import base64
from typing import Dict, Any, Optional, List
import json

from app.core.config import settings

logger = logging.getLogger(__name__)

class VisionAIService:
    """Vision AI 서비스 클래스"""
    
    def __init__(self):
        self.api_endpoint = settings.VISION_AI_ENDPOINT
        self.api_key = settings.VISION_AI_API_KEY
        self.confidence_threshold = settings.VISION_CONFIDENCE_THRESHOLD
        
        # 화재 탐지를 위한 색상 범위 (HSV)
        self.fire_color_ranges = [
            # 빨간색 범위 1
            (np.array([0, 50, 50]), np.array([10, 255, 255])),
            # 빨간색 범위 2
            (np.array([170, 50, 50]), np.array([180, 255, 255])),
            # 주황색 범위
            (np.array([10, 50, 50]), np.array([25, 255, 255])),
            # 노란색 범위
            (np.array([25, 50, 50]), np.array([35, 255, 255]))
        ]
    
    async def analyze_image(
        self, 
        image_url: Optional[str] = None, 
        image_data: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        이미지 분석 (화재 탐지, 연기 탐지 등)
        
        Args:
            image_url: 이미지 URL
            image_data: Base64 인코딩된 이미지 데이터
            
        Returns:
            분석 결과 딕셔너리
        """
        try:
            # 이미지 로드
            image = await self._load_image(image_url, image_data)
            if image is None:
                return self._create_empty_analysis()
            
            # 화재 탐지
            fire_detection = await self._detect_fire(image)
            
            # 연기 탐지
            smoke_detection = await self._detect_smoke(image)
            
            # 전체적인 이미지 품질 평가
            image_quality = self._assess_image_quality(image)
            
            # 종합 신뢰도 계산
            overall_confidence = self._calculate_overall_confidence(
                fire_detection, smoke_detection, image_quality
            )
            
            analysis_result = {
                "fire_detected": fire_detection["detected"],
                "fire_confidence": fire_detection["confidence"],
                "fire_areas": fire_detection["areas"],
                "smoke_detected": smoke_detection["detected"],
                "smoke_confidence": smoke_detection["confidence"],
                "smoke_areas": smoke_detection["areas"],
                "image_quality": image_quality,
                "overall_confidence": overall_confidence,
                "analysis_timestamp": str(asyncio.get_event_loop().time()),
                "data_quality": image_quality
            }
            
            logger.info(f"🔍 이미지 분석 완료 - 화재: {fire_detection['detected']}, 신뢰도: {overall_confidence:.2f}")
            return analysis_result
            
        except Exception as e:
            logger.error(f"❌ 이미지 분석 실패: {str(e)}")
            return self._create_empty_analysis()
    
    async def _load_image(
        self, 
        image_url: Optional[str] = None, 
        image_data: Optional[str] = None
    ) -> Optional[np.ndarray]:
        """이미지 로드"""
        try:
            if image_data:
                # Base64 데이터에서 이미지 로드
                image_bytes = base64.b64decode(image_data)
                image = Image.open(io.BytesIO(image_bytes))
                return np.array(image)
            
            elif image_url:
                # URL에서 이미지 다운로드
                async with httpx.AsyncClient() as client:
                    response = await client.get(image_url, timeout=30.0)
                    if response.status_code == 200:
                        image = Image.open(io.BytesIO(response.content))
                        return np.array(image)
            
            return None
            
        except Exception as e:
            logger.error(f"이미지 로드 실패: {str(e)}")
            return None
    
    async def _detect_fire(self, image: np.ndarray) -> Dict[str, Any]:
        """화재 탐지"""
        try:
            # BGR을 HSV로 변환
            hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
            
            # 화재 색상 마스크 생성
            fire_mask = np.zeros(hsv.shape[:2], dtype=np.uint8)
            
            for lower, upper in self.fire_color_ranges:
                mask = cv2.inRange(hsv, lower, upper)
                fire_mask = cv2.bitwise_or(fire_mask, mask)
            
            # 노이즈 제거
            kernel = np.ones((5, 5), np.uint8)
            fire_mask = cv2.morphologyEx(fire_mask, cv2.MORPH_CLOSE, kernel)
            fire_mask = cv2.morphologyEx(fire_mask, cv2.MORPH_OPEN, kernel)
            
            # 화재 영역 찾기
            contours, _ = cv2.findContours(fire_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            fire_areas = []
            total_fire_area = 0
            
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > 100:  # 최소 면적 필터링
                    x, y, w, h = cv2.boundingRect(contour)
                    fire_areas.append({
                        "x": int(x),
                        "y": int(y),
                        "width": int(w),
                        "height": int(h),
                        "area": int(area)
                    })
                    total_fire_area += area
            
            # 화재 탐지 여부 및 신뢰도 계산
            image_area = image.shape[0] * image.shape[1]
            fire_ratio = total_fire_area / image_area if image_area > 0 else 0
            
            detected = fire_ratio > 0.001  # 0.1% 이상이면 화재로 판단
            confidence = min(0.99, fire_ratio * 100)  # 비율에 따른 신뢰도
            
            return {
                "detected": detected,
                "confidence": confidence,
                "areas": fire_areas,
                "total_area": int(total_fire_area),
                "fire_ratio": fire_ratio
            }
            
        except Exception as e:
            logger.error(f"화재 탐지 실패: {str(e)}")
            return {
                "detected": False,
                "confidence": 0.0,
                "areas": [],
                "total_area": 0,
                "fire_ratio": 0.0
            }
    
    async def _detect_smoke(self, image: np.ndarray) -> Dict[str, Any]:
        """연기 탐지"""
        try:
            # 그레이스케일 변환
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            
            # 가우시안 블러 적용
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            
            # Canny 엣지 검출
            edges = cv2.Canny(blurred, 50, 150)
            
            # 연기 패턴 탐지 (불규칙한 형태의 엣지)
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            smoke_areas = []
            total_smoke_area = 0
            
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > 200:  # 최소 면적 필터링
                    # 연기 특성 분석 (불규칙한 형태)
                    perimeter = cv2.arcLength(contour, True)
                    if perimeter > 0:
                        circularity = 4 * np.pi * area / (perimeter * perimeter)
                        if circularity < 0.3:  # 원형이 아닌 불규칙한 형태
                            x, y, w, h = cv2.boundingRect(contour)
                            smoke_areas.append({
                                "x": int(x),
                                "y": int(y),
                                "width": int(w),
                                "height": int(h),
                                "area": int(area),
                                "circularity": float(circularity)
                            })
                            total_smoke_area += area
            
            # 연기 탐지 여부 및 신뢰도 계산
            image_area = image.shape[0] * image.shape[1]
            smoke_ratio = total_smoke_area / image_area if image_area > 0 else 0
            
            detected = smoke_ratio > 0.002  # 0.2% 이상이면 연기로 판단
            confidence = min(0.99, smoke_ratio * 50)  # 비율에 따른 신뢰도
            
            return {
                "detected": detected,
                "confidence": confidence,
                "areas": smoke_areas,
                "total_area": int(total_smoke_area),
                "smoke_ratio": smoke_ratio
            }
            
        except Exception as e:
            logger.error(f"연기 탐지 실패: {str(e)}")
            return {
                "detected": False,
                "confidence": 0.0,
                "areas": [],
                "total_area": 0,
                "smoke_ratio": 0.0
            }
    
    def _assess_image_quality(self, image: np.ndarray) -> float:
        """이미지 품질 평가"""
        try:
            # 그레이스케일 변환
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            
            # Laplacian을 이용한 선명도 측정
            laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
            
            # 선명도 점수 (0-1)
            sharpness_score = min(1.0, laplacian_var / 1000)
            
            # 밝기 균일성 측정
            brightness_std = np.std(gray)
            brightness_score = min(1.0, 1.0 - (brightness_std / 128))
            
            # 전체 품질 점수
            quality_score = (sharpness_score + brightness_score) / 2
            
            return quality_score
            
        except Exception as e:
            logger.error(f"이미지 품질 평가 실패: {str(e)}")
            return 0.5
    
    def _calculate_overall_confidence(
        self, 
        fire_detection: Dict[str, Any], 
        smoke_detection: Dict[str, Any], 
        image_quality: float
    ) -> float:
        """종합 신뢰도 계산"""
        try:
            # 화재 탐지 신뢰도
            fire_confidence = fire_detection["confidence"]
            
            # 연기 탐지 신뢰도
            smoke_confidence = smoke_detection["confidence"]
            
            # 이미지 품질 가중치
            quality_weight = image_quality
            
            # 종합 신뢰도 계산
            if fire_detection["detected"] and smoke_detection["detected"]:
                # 화재와 연기 모두 탐지된 경우
                overall_confidence = (fire_confidence + smoke_confidence) / 2 * quality_weight
            elif fire_detection["detected"]:
                # 화재만 탐지된 경우
                overall_confidence = fire_confidence * quality_weight * 0.8
            elif smoke_detection["detected"]:
                # 연기만 탐지된 경우
                overall_confidence = smoke_confidence * quality_weight * 0.6
            else:
                # 아무것도 탐지되지 않은 경우
                overall_confidence = 0.0
            
            return min(0.99, max(0.0, overall_confidence))
            
        except Exception as e:
            logger.error(f"종합 신뢰도 계산 실패: {str(e)}")
            return 0.0
    
    def _create_empty_analysis(self) -> Dict[str, Any]:
        """빈 분석 결과 생성"""
        return {
            "fire_detected": False,
            "fire_confidence": 0.0,
            "fire_areas": [],
            "smoke_detected": False,
            "smoke_confidence": 0.0,
            "smoke_areas": [],
            "image_quality": 0.0,
            "overall_confidence": 0.0,
            "analysis_timestamp": str(asyncio.get_event_loop().time()),
            "data_quality": 0.0
        }
