"""
대시보드 인증 유틸리티
관리자 로그인 및 토큰 관리
"""

import streamlit as st
import requests
import os
from typing import Optional, Dict, Any

# Streamlit Cloud에서는 st.secrets 사용, 로컬에서는 os.getenv 사용
try:
    API_BASE_URL = st.secrets.get("API_BASE_URL", "https://toki-auth-964943834069.asia-northeast3.run.app")
except:
    API_BASE_URL = os.getenv("API_BASE_URL", "https://toki-auth-964943834069.asia-northeast3.run.app")


def get_stored_token() -> Optional[str]:
    """세션에서 저장된 토큰 가져오기"""
    return st.session_state.get("access_token")


def save_token(access_token: str, refresh_token: str):
    """토큰을 세션에 저장"""
    st.session_state["access_token"] = access_token
    st.session_state["refresh_token"] = refresh_token
    st.session_state["authenticated"] = True


def clear_token():
    """토큰 삭제 (로그아웃)"""
    st.session_state["access_token"] = None
    st.session_state["refresh_token"] = None
    st.session_state["authenticated"] = False


def is_authenticated() -> bool:
    """인증 상태 확인"""
    return st.session_state.get("authenticated", False)


def make_api_request(
    endpoint: str,
    method: str = "GET",
    data: Optional[Dict[Any, Any]] = None,
    params: Optional[Dict[str, Any]] = None
) -> Optional[Dict[Any, Any]]:
    """
    Toki Auth API에 요청 보내기
    
    Args:
        endpoint: API 엔드포인트 경로 (예: "/api/v1/admin/users")
        method: HTTP 메서드 (GET, POST, etc.)
        data: 요청 본문 데이터
        params: 쿼리 파라미터
    
    Returns:
        API 응답 데이터 또는 None (에러 시)
    """
    token = get_stored_token()
    
    if not token:
        st.error("인증이 필요합니다. 로그인해주세요.")
        return None
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    url = f"{API_BASE_URL}{endpoint}"
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, params=params, timeout=10)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=data, timeout=10)
        else:
            st.error(f"지원하지 않는 HTTP 메서드: {method}")
            return None
        
        if response.status_code == 401:
            st.error("인증이 만료되었습니다. 다시 로그인해주세요.")
            clear_token()
            return None
        
        response.raise_for_status()
        return response.json()
        
    except requests.exceptions.RequestException as e:
        st.error(f"API 요청 실패: {str(e)}")
        return None


def verify_token() -> bool:
    """
    현재 토큰이 유효한지 확인
    
    Returns:
        토큰 유효 여부
    """
    token = get_stored_token()
    
    if not token:
        return False
    
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(
            f"{API_BASE_URL}/api/v1/auth/me",
            headers=headers,
            timeout=5
        )
        return response.status_code == 200
    except:
        return False


def require_auth():
    """
    인증이 필요한 페이지에서 호출
    인증되지 않은 경우 로그인 페이지로 리다이렉트
    """
    if not is_authenticated() or not verify_token():
        st.warning("⚠️ 관리자 인증이 필요합니다.")
        st.info("👉 사이드바에서 로그인해주세요.")
        st.stop()

