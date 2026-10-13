import streamlit as st
import json
import os
from datetime import datetime, date

st.set_page_config(page_title="🥕 3040 솔로메이트 회원관리", page_icon="🥕", layout="centered")

DATA_FILE = "club_members.json"

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

members = load_data()

st.title("🥕3040솔로메이트")
st.caption("운영진을 위한 직관적인 회원 관리 도구")

tab1, tab2, tab3 = st.tabs(["📋 회원 목록", "➕ 회원 등록", "⚙️ 참석 관리"])

# 오늘 날짜
today = date.today()

# [TAB 1] 회원 목록
with tab1:
    st.subheader("전체 회원 현황")
    if not members:
        st.info("아직 등록된 회원이 없습니다. '회원 등록' 탭에서 첫 회원을 추가해보세요!")
    else:
        search_query = st.text_input("🔍 아이디, 지역 또는 출생년도 검색", placeholder="검색어를 입력하세요...")
        
        filtered_members = members
        if search_query:
            filtered_members = {
                uid: info for uid, info in members.items()
                if search_query.lower() in uid.lower() 
                or search_query in info.get('지역', '')
                or search_query in info.get('출생년도', '')
            }

        st.metric(label="총 회원 수", value=f"{len(filtered_members)} 명")

        for uid, info in filtered_members.items():
            last_date_str = info.get("최근참석일", str(today))
            last_date = datetime.strptime(last_date_str, "%Y-%m-%d").date()
            days_passed = (today - last_date).days

            # 30일(한달) 경과 여부 카운팅 상태 표시
            if days_passed > 30:
                count_status = f"⚠️ {days_passed}일 경과 (한달 초과!)"
            else:
                count_status = f"✅ D+{days_passed}일 (정상)"

            badge = "✅ 참석" if info.get("월1회_참석여부") == "참석" else "❌ 미참석"
            birth_year = info.get("출생년도", "미입력")
            
            with st.expander(f"👤 {uid} ({info['성별']} / {birth_year}) | {badge} | {count_status}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**🎂 출생년도:** {birth_year}")
                    st.write(f"**📍 지역:** {info['지역']}")
                    st.write(f"**✨ 외모:** {info['외모']}")
                    st.write(f"**📅 최근 참석일:** {last_date_str}")
                with col2:
                    st.write(f"**💖 성격:** {info['성격']}")
                    st.write(f"**⏳ 지나간 날짜:** {days_passed}일 째")
                    st.write(f"**📌 월1회 상태:** {info.get('월1회_참석여부', '미참석')}")
                
                st.write(f"**📝 활동 특징:** {info['활동특징']}")
                
                if st.button(f"🗑️ {uid} 삭제", key=f"del_{uid}"):
                    del members[uid]
                    save_data(members)
                    st.success(f"{uid} 회원이 삭제되었습니다.")
                    st.rerun()

# [TAB 2] 회원 등록
with tab2:
    st.subheader("신규 회원 등록")
    with st.form("add_member_form", clear_on_submit=True):
        user_id = st.text_input("아이디 (필수)", placeholder="예: 당근이123")
        gender = st.radio("성별", ["F", "M"], horizontal=True)
        birth_year_input = st.text_input("출생년도", placeholder="예: 85년생 또는 1985")
        region = st.text_input("지역", placeholder="예: 강남구 역삼동")
        
        attendance = st.radio("이번 달 참석 여부", ["참석", "미참석"], horizontal=True)
        attend_date = st.date_input("최근 참석 날짜", value=today)
        
        feature = st.text_area("활동 특징", placeholder="예: 주말 모임 선호, 친화력 좋음")
        
        st.write("---")
        st.write("**평가 요소 (상/중/하)**")
        looks = st.select_slider("외모", options=["하", "중", "상"], value="중")
        personality = st.select_slider("성격", options=["하", "중", "상"], value="중")
        
        submitted = st.form_submit_button("➕ 회원 저장하기", use_container_width=True)
        
        if submitted:
            if not user_id.strip():
                st.error("아이디를 입력해주세요!")
            elif user_id in members:
                st.error("이미 존재하는 아이디입니다.")
            else:
                formatted_birth = birth_year_input.strip() if birth_year_input.strip() else "미입력"
                members[user_id] = {
                    "성별": gender,
                    "출생년도": formatted_birth,
                    "지역": region,
                    "월1회_참석여부": attendance,
                    "최근참석일": str(attend_date),
                    "활동특징": feature,
                    "외모": looks,
                    "성격": personality
                }
                save_data(members)
                st.success(f"🎉 [{user_id}] 회원이 성공적으로 등록되었습니다!")

# [TAB 3] 참석 관리
with tab3:
    st.subheader("이번 달 참석 체크 & 날짜 갱신")
    if not members:
        st.info("등록된 회원이 없습니다.")
    else:
        target_uid = st.selectbox("회원 선택", list(members.keys()))
        current_status = members[target_uid].get("월1회_참석여부", "미참석")
        current_date = members[target_uid].get("최근참석일", str(today))
        
        st.write(f"현재 참석 상태: **{current_status}** | 마지막 참석일: **{current_date}**")
        
        new_status = st.radio("참석 여부 변경", ["참석", "미참석"], key="update_status", horizontal=True)
        new_date = st.date_input("참석 날짜 선택", value=today)
        
        if st.button("상태 및 날짜 업데이트", use_container_width=True):
            members[target_uid]["월1회_참석여부"] = new_status
            members[target_uid]["최근참석일"] = str(new_date)
            save_data(members)
            st.success(f"[{target_uid}] 회원의 참석 정보가 업데이트되었습니다!")
            st.rerun()
