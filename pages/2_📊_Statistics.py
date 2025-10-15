"""
통계 페이지
상세 통계 및 차트
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime

from utils.auth import require_auth, make_api_request

st.set_page_config(
    page_title="통계 - Toki Auth Dashboard",
    page_icon="📊",
    layout="wide"
)

# 인증 확인
require_auth()

# 헤더
st.title("📊 상세 통계")
st.markdown("---")

# ==================== 전체 통계 ====================
stats = make_api_request("/api/v1/admin/stats")

if stats:
    # 사용자 통계
    st.header("👥 사용자 통계")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 활성/비활성 사용자 파이 차트
        user_status_data = pd.DataFrame({
            "상태": ["활성 사용자", "비활성 사용자"],
            "수": [stats['users']['active'], stats['users']['inactive']]
        })
        
        fig_status = px.pie(
            user_status_data,
            values="수",
            names="상태",
            title="사용자 활성화 상태",
            color="상태",
            color_discrete_map={
                "활성 사용자": "#4CAF50",
                "비활성 사용자": "#F44336"
            }
        )
        st.plotly_chart(fig_status, use_container_width=True)
    
    with col2:
        # 게이지 차트 - 활성률
        active_rate = (stats['users']['active'] / max(stats['users']['total'], 1)) * 100
        
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=active_rate,
            title={'text': "활성 사용자 비율 (%)"},
            delta={'reference': 80},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': "#4CAF50"},
                'steps': [
                    {'range': [0, 50], 'color': "lightgray"},
                    {'range': [50, 80], 'color': "gray"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        st.plotly_chart(fig_gauge, use_container_width=True)
    
    st.markdown("---")
    
    # ==================== OAuth 통계 ====================
    st.header("🔗 OAuth 연동 통계")
    
    provider_stats = make_api_request("/api/v1/admin/stats/providers")
    
    if provider_stats:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # 제공자별 상세 데이터
            st.subheader("제공자별 연동 수")
            
            for stat in provider_stats:
                provider_name = "💬 카카오" if stat['provider'] == "kakao" else "🔵 구글"
                st.metric(
                    label=provider_name,
                    value=stat['count']
                )
        
        with col2:
            # 비교 바 차트
            df_providers = pd.DataFrame(provider_stats)
            
            fig_providers = px.bar(
                df_providers,
                x='provider',
                y='count',
                title="제공자별 연동 계정 수",
                labels={'provider': 'OAuth 제공자', 'count': '연동 수'},
                color='provider',
                color_discrete_map={
                    'kakao': '#FEE500',
                    'google': '#4285F4'
                }
            )
            st.plotly_chart(fig_providers, use_container_width=True)
    
    st.markdown("---")
    
    # ==================== 일별 가입자 상세 ====================
    st.header("📅 일별 가입자 상세 분석")
    
    # 기간 선택
    days_range = st.slider(
        "조회 기간 (일)",
        min_value=7,
        max_value=90,
        value=30,
        step=7
    )
    
    daily_stats = make_api_request("/api/v1/admin/stats/daily", params={"days": days_range})
    
    if daily_stats:
        df_daily = pd.DataFrame(daily_stats)
        df_daily['date'] = pd.to_datetime(df_daily['date'])
        
        col1, col2 = st.columns(2)
        
        with col1:
            # 라인 차트
            fig_line = px.line(
                df_daily,
                x='date',
                y='count',
                title=f'최근 {days_range}일 가입자 추이',
                markers=True,
                labels={'date': '날짜', 'count': '가입자 수'}
            )
            fig_line.update_traces(line_color='#2196F3', line_width=3)
            st.plotly_chart(fig_line, use_container_width=True)
        
        with col2:
            # 영역 차트
            fig_area = px.area(
                df_daily,
                x='date',
                y='count',
                title=f'누적 가입자 추이',
                labels={'date': '날짜', 'count': '가입자 수'}
            )
            fig_area.update_traces(fillcolor='rgba(76, 175, 80, 0.3)', line_color='#4CAF50')
            st.plotly_chart(fig_area, use_container_width=True)
        
        # 통계 요약
        st.subheader("📈 통계 요약")
        
        total_signups = df_daily['count'].sum()
        avg_daily = df_daily['count'].mean()
        max_daily = df_daily['count'].max()
        
        col1, col2, col3 = st.columns(3)
        col1.metric("총 가입자", f"{total_signups}명")
        col2.metric("일평균 가입자", f"{avg_daily:.1f}명")
        col3.metric("최대 일 가입자", f"{max_daily}명")

else:
    st.error("통계 데이터를 불러올 수 없습니다.")

# 푸터
st.markdown("---")
st.caption(f"마지막 업데이트: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

