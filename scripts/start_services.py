#!/usr/bin/env python3
"""
서비스 시작 스크립트
"""

import asyncio
import subprocess
import sys
import os
import time
import signal
from pathlib import Path

def start_backend():
    """백엔드 서비스 시작"""
    print("🚀 백엔드 서비스 시작...")
    backend_dir = Path(__file__).parent.parent / "backend"
    os.chdir(backend_dir)
    
    try:
        # 백엔드 서버 시작
        process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", 
            "main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--reload"
        ])
        return process
    except Exception as e:
        print(f"❌ 백엔드 서비스 시작 실패: {str(e)}")
        return None

def start_frontend():
    """프론트엔드 서비스 시작"""
    print("🚀 프론트엔드 서비스 시작...")
    frontend_dir = Path(__file__).parent.parent / "frontend"
    os.chdir(frontend_dir)
    
    try:
        # 의존성 설치
        print("📦 프론트엔드 의존성 설치...")
        subprocess.run(["npm", "install"], check=True)
        
        # 프론트엔드 서버 시작
        process = subprocess.Popen(["npm", "start"])
        return process
    except Exception as e:
        print(f"❌ 프론트엔드 서비스 시작 실패: {str(e)}")
        return None

def start_websocket():
    """WebSocket 서버 시작"""
    print("🚀 WebSocket 서버 시작...")
    
    try:
        # WebSocket 서버 시작
        process = subprocess.Popen([
            "bunx", "cursor-talk-to-figma-socket"
        ])
        return process
    except Exception as e:
        print(f"❌ WebSocket 서버 시작 실패: {str(e)}")
        return None

def signal_handler(sig, frame):
    """시그널 핸들러"""
    print("\n🛑 서비스 종료 중...")
    sys.exit(0)

def main():
    """메인 함수"""
    print("🔥 산불 대응 AI Agent 시스템 시작")
    print("=" * 50)
    
    # 시그널 핸들러 등록
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    processes = []
    
    try:
        # 1. 데이터베이스 초기화
        print("🔧 데이터베이스 초기화...")
        subprocess.run([sys.executable, "scripts/setup_db.py"], check=True)
        
        # 2. WebSocket 서버 시작
        ws_process = start_websocket()
        if ws_process:
            processes.append(ws_process)
            time.sleep(2)  # WebSocket 서버 시작 대기
        
        # 3. 백엔드 서비스 시작
        backend_process = start_backend()
        if backend_process:
            processes.append(backend_process)
            time.sleep(5)  # 백엔드 서버 시작 대기
        
        # 4. 프론트엔드 서비스 시작
        frontend_process = start_frontend()
        if frontend_process:
            processes.append(frontend_process)
        
        print("\n✅ 모든 서비스가 시작되었습니다!")
        print("🌐 대시보드: http://localhost:3000")
        print("🔧 API 문서: http://localhost:8000/docs")
        print("📡 WebSocket: ws://localhost:3055")
        print("\n종료하려면 Ctrl+C를 누르세요.")
        
        # 프로세스 대기
        for process in processes:
            if process:
                process.wait()
                
    except KeyboardInterrupt:
        print("\n🛑 사용자에 의해 종료됨")
    except Exception as e:
        print(f"❌ 서비스 시작 실패: {str(e)}")
    finally:
        # 모든 프로세스 종료
        for process in processes:
            if process:
                process.terminate()
        print("👋 서비스가 종료되었습니다.")

if __name__ == "__main__":
    main()
