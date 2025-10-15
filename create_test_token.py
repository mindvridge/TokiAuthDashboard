"""
테스트용 JWT 토큰 직접 생성
실제 프로덕션에서는 사용하지 마세요!
"""

from jose import jwt
from datetime import datetime, timedelta

# Toki Auth Service와 동일한 설정 사용
JWT_SECRET_KEY = "Duln32ZVTOPFKF3eQnxRfmwSH0BPa6ZMY-7r-xIcwG8"  # Toki Auth의 실제 키
JWT_ALGORITHM = "HS256"

def create_test_tokens():
    """테스트용 JWT 토큰 생성"""
    
    print("=" * 60)
    print("Test JWT Token Generator")
    print("WARNING: For development/testing only!")
    print("=" * 60)
    
    # 테스트 사용자 데이터
    test_user = {
        "user_id": 1,
        "email": "admin@test.com"
    }
    
    # Access Token 생성
    access_token_data = {
        **test_user,
        "exp": datetime.utcnow() + timedelta(minutes=60),
        "iat": datetime.utcnow(),
        "type": "access"
    }
    
    access_token = jwt.encode(
        access_token_data,
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM
    )
    
    # Refresh Token 생성
    refresh_token_data = {
        "user_id": test_user["user_id"],
        "exp": datetime.utcnow() + timedelta(days=30),
        "iat": datetime.utcnow(),
        "type": "refresh"
    }
    
    refresh_token = jwt.encode(
        refresh_token_data,
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM
    )
    
    print("\n✅ 토큰 생성 완료!")
    print("=" * 60)
    print("\n📋 대시보드에 입력하세요:\n")
    print("Access Token:")
    print(access_token)
    print("\nRefresh Token:")
    print(refresh_token)
    print("\n" + "=" * 60)
    
    # 파일로 저장
    with open('test_admin_tokens.txt', 'w') as f:
        f.write(f"Access Token:\n{access_token}\n\n")
        f.write(f"Refresh Token:\n{refresh_token}\n\n")
        f.write(f"생성 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"만료: Access Token 60분, Refresh Token 30일\n")
    
    print("\n💾 토큰이 'test_admin_tokens.txt' 파일에 저장되었습니다.\n")
    print("⚠️  이 토큰으로 로그인하면 'admin@test.com' 사용자로 표시됩니다.")
    print("    실제 데이터를 조회할 수 있지만, 이 사용자는 DB에 없을 수 있습니다.\n")


if __name__ == "__main__":
    create_test_tokens()

