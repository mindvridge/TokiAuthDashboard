"""
Toki Auth Dashboard - 메인 페이지
관리자 대시보드 홈 화면
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import pandas as pd

from utils.auth import require_auth, make_api_request
from components.sidebar import render_sidebar

# 페이지 설정
st.set_page_config(
    page_title="Toki Auth Dashboard",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 사이드바 렌더링
render_sidebar()

# 인증 확인
require_auth()

# 헤더
st.title("🔐 Toki Auth Dashboard")
st.markdown("---")

# 통계 데이터 가져오기
stats = make_api_request("/api/v1/admin/stats")

if stats:
    # ==================== 주요 지표 ====================
    st.header("📊 주요 지표")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="전체 사용자",
            value=stats['users']['total'],
            delta=f"+{stats['users']['today']} 오늘"
        )
    
    with col2:
        st.metric(
            label="활성 사용자",
            value=stats['users']['active'],
            delta=f"{stats['users']['active'] / max(stats['users']['total'], 1) * 100:.1f}%"
        )
    
    with col3:
        st.metric(
            label="최근 7일 가입",
            value=stats['users']['last_7_days']
        )
    
    with col4:
        st.metric(
            label="활성 세션",
            value=stats['tokens']['active_refresh_tokens']
        )
    
    st.markdown("---")
    
    # ==================== OAuth 제공자 통계 ====================
    st.header("🔗 OAuth 제공자별 통계")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 파이 차트
        oauth_data = {
            "제공자": ["카카오", "구글"],
            "사용자 수": [stats['oauth']['kakao'], stats['oauth']['google']]
        }
        df_oauth = pd.DataFrame(oauth_data)
        
        fig_pie = px.pie(
            df_oauth,
            values="사용자 수",
            names="제공자",
            title="OAuth 제공자 분포",
            color="제공자",
            color_discrete_map={"카카오": "#FEE500", "구글": "#4285F4"}
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # 바 차트
        fig_bar = px.bar(
            df_oauth,
            x="제공자",
            y="사용자 수",
            title="제공자별 사용자 수",
            color="제공자",
            color_discrete_map={"카카오": "#FEE500", "구글": "#4285F4"}
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    
    st.markdown("---")
    
    # ==================== 일별 가입자 추이 ====================
    st.header("📈 일별 가입자 추이 (최근 30일)")
    
    daily_stats = make_api_request("/api/v1/admin/stats/daily", params={"days": 30})
    
    if daily_stats:
        df_daily = pd.DataFrame(daily_stats)
        df_daily['date'] = pd.to_datetime(df_daily['date'])
        
        fig_line = px.line(
            df_daily,
            x='date',
            y='count',
            title='일별 신규 가입자 수',
            markers=True,
            labels={'date': '날짜', 'count': '가입자 수'}
        )
        fig_line.update_traces(line_color='#4CAF50')
        st.plotly_chart(fig_line, use_container_width=True)
    
    st.markdown("---")
    
    # ==================== 최근 가입 사용자 ====================
    st.header("👤 최근 가입 사용자 (최근 10명)")
    
    recent_users = make_api_request("/api/v1/admin/users", params={"limit": 10})
    
    if recent_users:
        # 데이터프레임으로 변환
        users_data = []
        for user in recent_users:
            users_data.append({
                "ID": user['id'],
                "이메일": user['email'],
                "이름": user['name'] or "미설정",
                "활성화": "✅" if user['is_active'] else "❌",
                "가입일": user['created_at'][:10]
            })
        
        df_users = pd.DataFrame(users_data)
        st.dataframe(df_users, use_container_width=True, hide_index=True)
    
    # ==================== 빠른 액션 ====================
    st.markdown("---")
    st.header("⚡ 빠른 액션")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 새로고침", use_container_width=True):
            st.rerun()
    
    with col2:
        if st.button("👥 전체 사용자 보기", use_container_width=True):
            st.switch_page("pages/1_👥_Users.py")
    
    with col3:
        if st.button("📊 상세 통계 보기", use_container_width=True):
            st.switch_page("pages/2_📊_Statistics.py")

else:
    st.error("통계 데이터를 불러올 수 없습니다.")
    st.info("API 연결을 확인해주세요.")

# 푸터
st.markdown("---")
st.caption(f"Toki Auth Dashboard | 마지막 업데이트: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

