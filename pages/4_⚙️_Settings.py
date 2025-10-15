"""
설정 페이지
대시보드 설정 및 계정 관리
"""

import streamlit as st
import os
from datetime import datetime

from utils.auth import (
    require_auth,
    make_api_request,
    get_stored_token,
    clear_token,
    verify_token
)

st.set_page_config(
    page_title="설정 - Toki Auth Dashboard",
    page_icon="⚙️",
    layout="wide"
)

# 인증 확인
require_auth()

# 헤더
st.title("⚙️ 설정")
st.markdown("---")

# ==================== 계정 정보 ====================
st.header("👤 계정 정보")

# 현재 사용자 프로필 조회
profile = make_api_request("/api/v1/auth/me")

if profile:
    col1, col2 = st.columns([1, 2])
    
    with col1:
        if profile['user'].get('profile_image'):
            st.image(profile['user']['profile_image'], width=150)
        else:
            st.image("https://via.placeholder.com/150?text=No+Image", width=150)
    
    with col2:
        st.subheader(profile['user']['name'] or "관리자")
        st.write(f"**이메일**: {profile['user']['email']}")
        st.write(f"**사용자 ID**: {profile['user']['id']}")
        st.write(f"**가입일**: {profile['user']['created_at'][:19]}")
        
        # 연동 계정
        st.write("**연동 계정**:")
        for account in profile['linked_accounts']:
            provider_emoji = "💬" if account['provider'] == "kakao" else "🔵"
            st.write(f"  {provider_emoji} {account['provider'].upper()}")

st.markdown("---")

# ==================== API 연결 설정 ====================
st.header("🔌 API 연결 설정")

api_url = os.getenv("API_BASE_URL", "https://toki-auth-964943834069.asia-northeast3.run.app")
st.info(f"**API URL**: {api_url}")

# 연결 테스트
if st.button("🧪 API 연결 테스트", type="primary"):
    with st.spinner("API 연결 확인 중..."):
        health = make_api_request("/health")
        
        if health:
            st.success(f"✅ API 연결 성공: {health.get('service', 'Unknown')}")
        else:
            st.error("❌ API 연결 실패")

st.markdown("---")

# ==================== 토큰 정보 ====================
st.header("🔑 인증 토큰")

token = get_stored_token()

if token:
    # 토큰 유효성 확인
    is_valid = verify_token()
    
    if is_valid:
        st.success("✅ 토큰이 유효합니다.")
    else:
        st.warning("⚠️ 토큰이 만료되었거나 유효하지 않습니다.")
    
    # 토큰 정보 (일부만 표시)
    st.code(f"{token[:20]}...{token[-20:]}")
    
    # 로그아웃 버튼
    if st.button("🚪 로그아웃", type="secondary"):
        clear_token()
        st.success("✅ 로그아웃되었습니다.")
        st.info("👉 사이드바에서 다시 로그인하세요.")
        st.rerun()
else:
    st.warning("⚠️ 토큰이 없습니다. 로그인이 필요합니다.")

st.markdown("---")

# ==================== 대시보드 정보 ====================
st.header("ℹ️ 대시보드 정보")

col1, col2 = st.columns(2)

with col1:
    st.write("**버전**: 1.0.0")
    st.write("**프레임워크**: Streamlit")
    st.write("**Python**: 3.11")

with col2:
    st.write("**서비스**: Toki Auth Dashboard")
    st.write("**배포**: Google Cloud Run")
    st.write("**리전**: asia-northeast3 (서울)")

# 푸터
st.markdown("---")
st.caption(f"Toki Auth Dashboard v1.0.0 | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

