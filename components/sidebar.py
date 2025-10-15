"""
사이드바 컴포넌트
로그인 및 네비게이션
"""

import streamlit as st
import requests
import os

from utils.auth import (
    save_token,
    clear_token,
    is_authenticated,
    get_stored_token,
    make_api_request
)

API_BASE_URL = os.getenv("API_BASE_URL", "https://toki-auth-964943834069.asia-northeast3.run.app")


def render_sidebar():
    """사이드바 렌더링"""
    
    with st.sidebar:
        st.title("🔐 Toki Auth")
        st.markdown("**관리자 대시보드**")
        st.markdown("---")
        
        # 인증 상태에 따라 다른 UI 표시
        if is_authenticated():
            render_authenticated_sidebar()
        else:
            render_login_sidebar()


def render_login_sidebar():
    """로그인 폼 렌더링"""
    
    st.subheader("🔑 관리자 로그인")
    
    # 로그인 방법 선택
    login_method = st.radio(
        "로그인 방법",
        ["JWT 토큰 직접 입력", "카카오/구글 로그인"],
        help="관리자 JWT 토큰을 입력하거나 OAuth로 로그인하세요"
    )
    
    if login_method == "JWT 토큰 직접 입력":
        # JWT 토큰 직접 입력
        st.info("Toki Auth 서비스에서 로그인 후 받은 JWT 토큰을 입력하세요.")
        
        access_token = st.text_input(
            "Access Token",
            type="password",
            help="JWT 액세스 토큰"
        )
        
        refresh_token = st.text_input(
            "Refresh Token",
            type="password",
            help="JWT 리프레시 토큰"
        )
        
        if st.button("로그인", type="primary", use_container_width=True):
            if access_token and refresh_token:
                # 토큰 검증
                try:
                    headers = {"Authorization": f"Bearer {access_token}"}
                    response = requests.get(
                        f"{API_BASE_URL}/api/v1/auth/me",
                        headers=headers,
                        timeout=5
                    )
                    
                    if response.status_code == 200:
                        save_token(access_token, refresh_token)
                        st.success("✅ 로그인 성공!")
                        st.rerun()
                    else:
                        st.error("❌ 유효하지 않은 토큰입니다.")
                except Exception as e:
                    st.error(f"❌ 로그인 실패: {str(e)}")
            else:
                st.warning("⚠️ 토큰을 모두 입력해주세요.")
    
    else:
        # OAuth 로그인
        st.info("카카오 또는 구글로 로그인한 후 토큰을 받으세요.")
        
        # 카카오 로그인 버튼
        kakao_url = f"{API_BASE_URL}/api/v1/auth/kakao/url"
        st.link_button(
            "💬 카카오 로그인",
            kakao_url,
            use_container_width=True
        )
        
        # 구글 로그인 버튼
        google_url = f"{API_BASE_URL}/api/v1/auth/google/url"
        st.link_button(
            "🔵 구글 로그인",
            google_url,
            use_container_width=True
        )
        
        st.info("로그인 후 받은 JWT 토큰을 '토큰 직접 입력' 방식으로 입력하세요.")
    
    # 도움말
    st.markdown("---")
    st.caption("💡 **도움말**")
    st.caption("1. Toki Auth 서비스에서 로그인")
    st.caption("2. 받은 JWT 토큰을 복사")
    st.caption("3. 위에 토큰을 붙여넣기")


def render_authenticated_sidebar():
    """인증된 사용자용 사이드바"""
    
    # 사용자 정보 표시
    profile = make_api_request("/api/v1/auth/me")
    
    if profile:
        st.success("✅ 로그인됨")
        
        user = profile['user']
        
        # 프로필 이미지
        if user.get('profile_image'):
            st.image(user['profile_image'], width=100)
        
        st.write(f"**{user.get('name', '관리자')}**")
        st.caption(user['email'])
        
        st.markdown("---")
    
    # 네비게이션
    st.subheader("📂 메뉴")
    
    st.page_link("app.py", label="🏠 대시보드 홈", icon="🏠")
    st.page_link("pages/1_👥_Users.py", label="사용자 관리", icon="👥")
    st.page_link("pages/2_📊_Statistics.py", label="통계", icon="📊")
    st.page_link("pages/3_🔗_OAuth.py", label="OAuth 계정", icon="🔗")
    st.page_link("pages/4_⚙️_Settings.py", label="설정", icon="⚙️")
    
    st.markdown("---")
    
    # 로그아웃 버튼
    if st.button("🚪 로그아웃", use_container_width=True):
        clear_token()
        st.success("✅ 로그아웃되었습니다.")
        st.rerun()
    
    # 정보
    st.markdown("---")
    st.caption("**Toki Auth Dashboard**")
    st.caption("v1.0.0")

