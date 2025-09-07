#!/usr/bin/env python3
"""
배포 스크립트
"""

import subprocess
import sys
import os
from pathlib import Path

def check_dependencies():
    """의존성 확인"""
    print("🔍 의존성 확인...")
    
    required_commands = ["docker", "docker-compose", "bun"]
    
    for cmd in required_commands:
        try:
            subprocess.run([cmd, "--version"], check=True, capture_output=True)
            print(f"✅ {cmd} 설치됨")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print(f"❌ {cmd}가 설치되지 않았습니다")
            return False
    
    return True

def build_images():
    """Docker 이미지 빌드"""
    print("\n🏗️ Docker 이미지 빌드...")
    
    try:
        # 백엔드 이미지 빌드
        print("백엔드 이미지 빌드 중...")
        subprocess.run([
            "docker", "build", 
            "-t", "forest-fire-ai-backend", 
            "./backend"
        ], check=True)
        
        # 프론트엔드 이미지 빌드
        print("프론트엔드 이미지 빌드 중...")
        subprocess.run([
            "docker", "build", 
            "-t", "forest-fire-ai-frontend", 
            "./frontend"
        ], check=True)
        
        print("✅ 이미지 빌드 완료")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ 이미지 빌드 실패: {e}")
        return False

def start_services():
    """서비스 시작"""
    print("\n🚀 서비스 시작...")
    
    try:
        # Docker Compose로 서비스 시작
        subprocess.run([
            "docker-compose", "up", "-d"
        ], check=True)
        
        print("✅ 서비스 시작 완료")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ 서비스 시작 실패: {e}")
        return False

def check_services():
    """서비스 상태 확인"""
    print("\n🔍 서비스 상태 확인...")
    
    services = [
        ("postgres", "5432"),
        ("redis", "6379"),
        ("rabbitmq", "5672"),
        ("backend", "8000"),
        ("frontend", "3000")
    ]
    
    for service, port in services:
        try:
            result = subprocess.run([
                "docker-compose", "ps", service
            ], capture_output=True, text=True)
            
            if "Up" in result.stdout:
                print(f"✅ {service} 실행 중 (포트: {port})")
            else:
                print(f"❌ {service} 실행되지 않음")
                return False
        except Exception as e:
            print(f"❌ {service} 상태 확인 실패: {e}")
            return False
    
    return True

def run_migrations():
    """데이터베이스 마이그레이션 실행"""
    print("\n🗄️ 데이터베이스 마이그레이션...")
    
    try:
        # 데이터베이스 초기화
        subprocess.run([
            "python", "scripts/setup_db.py"
        ], check=True)
        
        print("✅ 데이터베이스 마이그레이션 완료")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ 데이터베이스 마이그레이션 실패: {e}")
        return False

def main():
    """메인 함수"""
    print("🚀 산불 대응 AI Agent 시스템 배포")
    print("=" * 50)
    
    # 프로젝트 루트 디렉토리로 이동
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    success = True
    
    # 1. 의존성 확인
    if not check_dependencies():
        print("❌ 필요한 의존성이 설치되지 않았습니다.")
        sys.exit(1)
    
    # 2. 이미지 빌드
    if not build_images():
        success = False
    
    # 3. 서비스 시작
    if success and not start_services():
        success = False
    
    # 4. 서비스 상태 확인
    if success and not check_services():
        success = False
    
    # 5. 데이터베이스 마이그레이션
    if success and not run_migrations():
        success = False
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 배포가 완료되었습니다!")
        print("\n📱 접속 정보:")
        print("🌐 대시보드: http://localhost:3000")
        print("🔧 API 문서: http://localhost:8000/docs")
        print("📊 Grafana: http://localhost:3001")
        print("📈 Prometheus: http://localhost:9090")
        print("\n🛑 서비스 중지: docker-compose down")
    else:
        print("❌ 배포 중 오류가 발생했습니다.")
        sys.exit(1)

if __name__ == "__main__":
    main()
