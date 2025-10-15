"""
관리자용 JWT 토큰 생성 스크립트
대시보드 테스트용으로 사용
"""

import requests
import json

API_BASE_URL = "https://toki-auth-964943834069.asia-northeast3.run.app"

def get_admin_token():
    """
    테스트용 관리자 토큰 받기
    
    주의: 실제 카카오 액세스 토큰이 필요합니다.
    """
    
    print("=" * 60)
    print("Toki Auth - 관리자 토큰 생성")
    print("=" * 60)
    
    print("\n카카오 액세스 토큰을 입력하세요.")
    print("(카카오 개발자 도구 또는 앱에서 받은 토큰)")
    
    kakao_token = input("\n카카오 액세스 토큰: ").strip()
    
    if not kakao_token:
        print("❌ 토큰이 입력되지 않았습니다.")
        return
    
    print("\n🔄 Toki Auth Service에 요청 중...")
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/v1/auth/kakao/callback",
            json={"access_token": kakao_token},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            
            print("\n✅ 토큰 발급 성공!")
            print("=" * 60)
            print("\n📋 아래 토큰을 대시보드에 입력하세요:\n")
            print("Access Token:")
            print(data['access_token'])
            print("\nRefresh Token:")
            print(data['refresh_token'])
            print("\n" + "=" * 60)
            
            # 파일로 저장
            with open('admin_tokens.txt', 'w') as f:
                f.write(f"Access Token:\n{data['access_token']}\n\n")
                f.write(f"Refresh Token:\n{data['refresh_token']}\n")
            
            print("\n💾 토큰이 'admin_tokens.txt' 파일에 저장되었습니다.")
            
        else:
            print(f"\n❌ 토큰 발급 실패: {response.status_code}")
            print(f"응답: {response.text}")
            
    except Exception as e:
        print(f"\n❌ 오류 발생: {str(e)}")


if __name__ == "__main__":
    get_admin_token()

