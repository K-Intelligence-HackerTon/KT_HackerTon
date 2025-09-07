#!/usr/bin/env python3
"""
테스트 실행 스크립트
"""

import subprocess
import sys
import os
from pathlib import Path

def run_tests():
    """테스트 실행"""
    print("🧪 테스트 실행 시작...")
    print("=" * 50)
    
    # 프로젝트 루트 디렉토리로 이동
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    try:
        # pytest 실행
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "tests/", 
            "-v", 
            "--tb=short",
            "--cov=backend/app",
            "--cov-report=html",
            "--cov-report=term"
        ], check=True)
        
        print("\n✅ 모든 테스트가 통과했습니다!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ 테스트 실패: {e}")
        return False
    except Exception as e:
        print(f"\n❌ 테스트 실행 중 오류: {str(e)}")
        return False

def run_linting():
    """린팅 실행"""
    print("\n🔍 코드 린팅 실행...")
    print("=" * 50)
    
    try:
        # Python 코드 린팅
        subprocess.run([
            sys.executable, "-m", "flake8", 
            "backend/", 
            "--max-line-length=100",
            "--ignore=E203,W503"
        ], check=True)
        
        # Type checking
        subprocess.run([
            sys.executable, "-m", "mypy", 
            "backend/",
            "--ignore-missing-imports"
        ], check=True)
        
        print("✅ 린팅 통과!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ 린팅 실패: {e}")
        return False
    except Exception as e:
        print(f"❌ 린팅 실행 중 오류: {str(e)}")
        return False

def main():
    """메인 함수"""
    print("🔥 산불 대응 AI Agent 시스템 테스트")
    print("=" * 50)
    
    success = True
    
    # 1. 린팅 실행
    if not run_linting():
        success = False
    
    # 2. 테스트 실행
    if not run_tests():
        success = False
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 모든 검사가 통과했습니다!")
        sys.exit(0)
    else:
        print("❌ 일부 검사가 실패했습니다.")
        sys.exit(1)

if __name__ == "__main__":
    main()
