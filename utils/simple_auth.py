"""
대시보드 전용 간단한 아이디/비밀번호 인증
Streamlit Secrets를 사용하여 관리자 계정 관리
"""

import streamlit as st
import hashlib
from datetime import datetime, timedelta
from jose import jwt

# JWT 설정 (Toki Auth와 동일한 키 사용)
JWT_SECRET_KEY = "Duln32ZVTOPFKF3eQnxRfmwSH0BPa6ZMY-7r-xIcwG8"
JWT_ALGORITHM = "HS256"


def get_admin_credentials():
    """
    Streamlit Secrets에서 관리자 계정 정보 가져오기
    """
    try:
        # Streamlit Cloud Secrets 사용
        username = st.secrets.get("ADMIN_USERNAME", "admin")
        password = st.secrets.get("ADMIN_PASSWORD", "admin123")
    except:
        # 로컬 환경 기본값
        username = "admin"
        password = "admin123"
    
    return username, password


def verify_password(input_password: str, stored_password: str) -> bool:
    """
    비밀번호 검증
    
    Args:
        input_password: 사용자가 입력한 비밀번호
        stored_password: 저장된 비밀번호
    
    Returns:
        일치 여부
    """
    # 단순 비교 (프로덕션에서는 해싱 사용 권장)
    return input_password == stored_password


def create_jwt_tokens_for_admin(email: str = "admin@dashboard.local"):
    """
    관리자용 JWT 토큰 생성
    Toki Auth Service와 호환되는 형식
    
    Args:
        email: 관리자 이메일
    
    Returns:
        (access_token, refresh_token) 튜플
    """
    # Access Token 생성
    access_token_data = {
        "user_id": 999,  # 관리자 전용 ID
        "email": email,
        "exp": datetime.utcnow() + timedelta(hours=8),  # 8시간 유효
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
        "user_id": 999,
        "exp": datetime.utcnow() + timedelta(days=30),
        "iat": datetime.utcnow(),
        "type": "refresh"
    }
    
    refresh_token = jwt.encode(
        refresh_token_data,
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM
    )
    
    return access_token, refresh_token


def simple_login(username: str, password: str) -> bool:
    """
    간단한 아이디/비밀번호 로그인
    
    Args:
        username: 사용자명
        password: 비밀번호
    
    Returns:
        로그인 성공 여부
    """
    admin_username, admin_password = get_admin_credentials()
    
    # 계정 검증
    if username == admin_username and verify_password(password, admin_password):
        # JWT 토큰 생성
        access_token, refresh_token = create_jwt_tokens_for_admin(
            email=f"{username}@dashboard.local"
        )
        
        # 세션에 저장
        st.session_state["access_token"] = access_token
        st.session_state["refresh_token"] = refresh_token
        st.session_state["authenticated"] = True
        st.session_state["username"] = username
        
        return True
    
    return False

