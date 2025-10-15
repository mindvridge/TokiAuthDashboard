"""
사용자 관리 페이지
전체 사용자 목록 조회 및 검색
"""

import streamlit as st
import pandas as pd
from datetime import datetime

from utils.auth import require_auth, make_api_request

st.set_page_config(
    page_title="사용자 관리 - Toki Auth Dashboard",
    page_icon="👥",
    layout="wide"
)

# 인증 확인
require_auth()

# 헤더
st.title("👥 사용자 관리")
st.markdown("---")

# ==================== 필터 및 검색 ====================
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    search_query = st.text_input(
        "🔍 검색",
        placeholder="이메일 또는 이름으로 검색...",
        help="사용자 이메일 또는 이름을 입력하세요"
    )

with col2:
    filter_active = st.selectbox(
        "활성화 상태",
        ["전체", "활성", "비활성"],
        help="사용자 활성화 상태로 필터링"
    )

with col3:
    limit = st.selectbox(
        "표시 개수",
        [10, 25, 50, 100],
        index=2,
        help="한 번에 표시할 사용자 수"
    )

# 필터 파라미터 구성
params = {"limit": limit, "skip": 0}

if search_query:
    params["search"] = search_query

if filter_active == "활성":
    params["is_active"] = True
elif filter_active == "비활성":
    params["is_active"] = False

# ==================== 사용자 목록 조회 ====================
users = make_api_request("/api/v1/admin/users", params=params)

if users:
    st.success(f"✅ {len(users)}명의 사용자를 찾았습니다.")
    
    # 데이터프레임으로 변환
    users_data = []
    for user in users:
        users_data.append({
            "ID": user['id'],
            "이메일": user['email'],
            "이름": user['name'] or "미설정",
            "프로필": "🖼️" if user['profile_image'] else "❌",
            "활성화": "✅" if user['is_active'] else "❌",
            "가입일": user['created_at'][:19].replace('T', ' ')
        })
    
    df = pd.DataFrame(users_data)
    
    # 데이터프레임 표시
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "ID": st.column_config.NumberColumn("ID", width="small"),
            "이메일": st.column_config.TextColumn("이메일", width="large"),
            "이름": st.column_config.TextColumn("이름", width="medium"),
            "프로필": st.column_config.TextColumn("프로필", width="small"),
            "활성화": st.column_config.TextColumn("활성화", width="small"),
            "가입일": st.column_config.TextColumn("가입일", width="medium")
        }
    )
    
    # ==================== 사용자 상세 정보 ====================
    st.markdown("---")
    st.subheader("📋 사용자 상세 정보")
    
    selected_user_id = st.number_input(
        "사용자 ID 입력",
        min_value=1,
        step=1,
        help="상세 정보를 볼 사용자 ID를 입력하세요"
    )
    
    if st.button("🔍 조회", type="primary"):
        user_detail = make_api_request(f"/api/v1/admin/users/{selected_user_id}")
        
        if user_detail:
            st.success("✅ 사용자 정보를 찾았습니다.")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("기본 정보")
                st.write(f"**ID**: {user_detail['user']['id']}")
                st.write(f"**이메일**: {user_detail['user']['email']}")
                st.write(f"**이름**: {user_detail['user']['name'] or '미설정'}")
                st.write(f"**활성화**: {'✅ 활성' if user_detail['user']['is_active'] else '❌ 비활성'}")
                st.write(f"**가입일**: {user_detail['user']['created_at'][:19]}")
                
                if user_detail['user']['profile_image']:
                    st.image(user_detail['user']['profile_image'], width=150)
            
            with col2:
                st.subheader("연동 계정")
                
                if user_detail['oauth_accounts']:
                    for oauth in user_detail['oauth_accounts']:
                        provider_emoji = "💬" if oauth['provider'] == "kakao" else "🔵"
                        st.write(f"{provider_emoji} **{oauth['provider'].upper()}**")
                        st.write(f"   - 이메일: {oauth['provider_email'] or '미제공'}")
                        st.write(f"   - 연동일: {oauth['created_at'][:19]}")
                        st.markdown("---")
                else:
                    st.info("연동된 OAuth 계정이 없습니다.")
    
    # ==================== 내보내기 ====================
    st.markdown("---")
    st.subheader("💾 데이터 내보내기")
    
    csv = df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📥 CSV 다운로드",
        data=csv,
        file_name=f"toki_auth_users_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )

else:
    st.error("사용자 데이터를 불러올 수 없습니다.")
    st.info("API 연결을 확인하거나 로그인 상태를 확인해주세요.")

# 푸터
st.markdown("---")
st.caption(f"마지막 업데이트: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

