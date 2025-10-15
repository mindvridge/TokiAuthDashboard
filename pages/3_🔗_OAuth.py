"""
OAuth 계정 관리 페이지
OAuth 연동 계정 조회 및 관리
"""

import streamlit as st
import pandas as pd
from datetime import datetime

from utils.auth import require_auth, make_api_request

st.set_page_config(
    page_title="OAuth 관리 - Toki Auth Dashboard",
    page_icon="🔗",
    layout="wide"
)

# 인증 확인
require_auth()

# 헤더
st.title("🔗 OAuth 계정 관리")
st.markdown("---")

# ==================== 필터 ====================
col1, col2 = st.columns([1, 1])

with col1:
    provider_filter = st.selectbox(
        "OAuth 제공자",
        ["전체", "kakao", "google"],
        help="OAuth 제공자로 필터링"
    )

with col2:
    limit = st.selectbox(
        "표시 개수",
        [25, 50, 100, 200],
        index=1
    )

# 파라미터 구성
params = {"limit": limit, "skip": 0}

if provider_filter != "전체":
    params["provider"] = provider_filter

# ==================== OAuth 계정 목록 ====================
oauth_accounts = make_api_request("/api/v1/admin/oauth-accounts", params=params)

if oauth_accounts:
    st.success(f"✅ {len(oauth_accounts)}개의 OAuth 계정을 찾았습니다.")
    
    # 데이터프레임으로 변환
    accounts_data = []
    for account in oauth_accounts:
        provider_emoji = "💬" if account['provider'] == "kakao" else "🔵"
        
        accounts_data.append({
            "ID": account['id'],
            "사용자 ID": account['user_id'],
            "제공자": f"{provider_emoji} {account['provider'].upper()}",
            "제공자 사용자 ID": account['provider_user_id'],
            "이메일": account.get('provider_email', '미제공'),
            "연동일": account['created_at'][:19].replace('T', ' ')
        })
    
    df = pd.DataFrame(accounts_data)
    
    # 데이터프레임 표시
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "ID": st.column_config.NumberColumn("ID", width="small"),
            "사용자 ID": st.column_config.NumberColumn("사용자 ID", width="small"),
            "제공자": st.column_config.TextColumn("제공자", width="medium"),
            "제공자 사용자 ID": st.column_config.TextColumn("제공자 사용자 ID", width="medium"),
            "이메일": st.column_config.TextColumn("이메일", width="large"),
            "연동일": st.column_config.TextColumn("연동일", width="medium")
        }
    )
    
    # ==================== 통계 요약 ====================
    st.markdown("---")
    st.subheader("📈 OAuth 계정 통계")
    
    # 제공자별 그룹화
    provider_counts = df['제공자'].value_counts()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("💬 카카오 계정", len(df[df['제공자'].str.contains('kakao', case=False)]))
    
    with col2:
        st.metric("🔵 구글 계정", len(df[df['제공자'].str.contains('google', case=False)]))
    
    # ==================== 내보내기 ====================
    st.markdown("---")
    st.subheader("💾 데이터 내보내기")
    
    csv = df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📥 CSV 다운로드",
        data=csv,
        file_name=f"oauth_accounts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )

else:
    st.error("OAuth 계정 데이터를 불러올 수 없습니다.")

# 푸터
st.markdown("---")
st.caption(f"마지막 업데이트: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

