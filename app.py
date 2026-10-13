import streamlit as st
import json
import os
import re
from datetime import datetime, date

st.set_page_config(page_title="🥕 당근 모임 관리", page_icon="🥕", layout="centered")

DATA_FILE = "club_members.json"

# 이미지에서 추출한 기본 회원 데이터 (이모티콘 포함)
INITIAL_MEMBERS = {
    "개동👑": {"성별": "M", "출생년도": "87년생", "지역": "응암동", "가입일자": "2025-12-09", "월1회_참석여부": "미참석", "최근참석일": "2025-12-09", "활동특징": "-", "외모": "중", "성격": "중"},
    "그레이": {"성별": "F", "출생년도": "90년생", "지역": "성산동", "가입일자": "2025-12-16", "월1회_참석여부": "미참석", "최근참석일": "2025-12-16", "활동특징": "-", "외모": "중", "성격": "중"},
    "용진": {"성별": "M", "출생년도": "84년생", "지역": "북가좌제1동", "가입일자": "2026-01-05", "월1회_참석여부": "미참석", "최근참석일": "2026-01-05", "활동특징": "-", "외모": "중", "성격": "중"},
    "희희": {"성별": "F", "출생년도": "91년생", "지역": "성산동", "가입일자": "2026-01-19", "월1회_참석여부": "미참석", "최근참석일": "2026-01-19", "활동특징": "-", "외모": "중", "성격": "중"},
    "농뇽": {"성별": "F", "출생년도": "88년생", "지역": "성산동", "가입일자": "2026-01-26", "월1회_참석여부": "미참석", "최근참석일": "2026-01-26", "활동특징": "-", "외모": "중", "성격": "중"},
    "마포🍀": {"성별": "M", "출생년도": "90년생", "지역": "성산제2동", "가입일자": "2026-02-27", "월1회_참석여부": "미참석", "최근참석일": "2026-02-27", "활동특징": "-", "외모": "중", "성격": "중"},
    "레이": {"성별": "F", "출생년도": "84년생", "지역": "연희동", "가입일자": "2026-03-02", "월1회_참석여부": "미참석", "최근참석일": "2026-03-02", "활동특징": "-", "외모": "중", "성격": "중"},
    "제이": {"성별": "M", "출생년도": "83년생", "지역": "홍은제2동", "가입일자": "2026-03-09", "월1회_참석여부": "미참석", "최근참석일": "2026-03-09", "활동특징": "-", "외모": "중", "성격": "중"},
    "머핀": {"성별": "F", "출생년도": "86년생", "지역": "삼산동", "가입일자": "2026-03-15", "월1회_참석여부": "미참석", "최근참석일": "2026-03-15", "활동특징": "-", "외모": "중", "성격": "중"},
    "하리": {"성별": "F", "출생년도": "87년생", "지역": "응암제1동", "가입일자": "2026-03-31", "월1회_참석여부": "미참석", "최근참석일": "2026-03-31", "활동특징": "-", "외모": "중", "성격": "중"},
    "힘내자": {"성별": "F", "출생년도": "86년생", "지역": "연희동", "가입일자": "2026-04-23", "월1회_참석여부": "미참석", "최근참석일": "2026-04-23", "활동특징": "-", "외모": "중", "성격": "중"},
    "기강승🐷": {"성별": "M", "출생년도": "89년생", "지역": "신사동", "가입일자": "2026-07-02", "월1회_참석여부": "미참석", "최근참석일": "2026-07-02", "활동특징": "-", "외모": "중", "성격": "중"},
    "로나": {"성별": "F", "출생년도": "87년생", "지역": "북가좌동", "가입일자": "2026-07-05", "월1회_참석여부": "미참석", "최근참석일": "2026-07-05", "활동특징": "-", "외모": "중", "성격": "중"},
    "상이": {"성별": "M", "출생년도": "91년생", "지역": "효창동", "가입일자": "2026-07-06", "월1회_참석여부": "미참석", "최근참석일": "2026-07-06", "활동특징": "-", "외모": "중", "성격": "중"},
    "말타": {"성별": "M", "출생년도": "86년생", "지역": "연남동", "가입일자": "2026-07-16", "월1회_참석여부": "미참석", "최근참석일": "2026-07-16", "활동특징": "-", "외모": "중", "성격": "중"},
    "포톤": {"성별": "M", "출생년도": "87년생", "지역": "녹번동", "가입일자": "2026-07-17", "월1회_참석여부": "미참석", "최근참석일": "2026-07-17", "활동특징": "-", "외모": "중", "성격": "중"},
    "만물상아재": {"성별": "M", "출생년도": "87년생", "지역": "영등포동4가", "가입일자": "2026-07-22", "월1회_참석여부": "미참석", "최근참석일": "2026-07-22", "활동특징": "-", "외모": "중", "성격": "중"},
    "토토": {"성별": "F", "출생년도": "87년생", "지역": "서초1동", "가입일자": "2026-07-31", "월1회_참석여부": "미참석", "최근참석일": "2026-07-31", "활동특징": "-", "외모": "중", "성격": "중"},
    "라디": {"성별": "M", "출생년도": "90년생", "지역": "신사동", "가입일자": "2026-07-31", "월1회_참석여부": "미참석", "최근참석일": "2026-07-31", "활동특징": "-", "외모": "중", "성격": "중"},
    "은호": {"성별": "F", "출생년도": "88년생", "지역": "상수동", "가입일자": "2026-08-02", "월1회_참석여부": "미참석", "최근참석일": "2026-08-02", "활동특징": "-", "외모": "중", "성격": "중"},
    "보미": {"성별": "F", "출생년도": "85년생", "지역": "서교동", "가입일자": "2026-08-31", "월1회_참석여부": "미참석", "최근참석일": "2026-08-31", "활동특징": "-", "외모": "중", "성격": "중"},
    "서율": {"성별": "M", "출생년도": "88년생", "지역": "가양제3동", "가입일자": "2026-09-04", "월1회_참석여부": "미참석", "최근참석일": "2026-09-04", "활동특징": "-", "외모": "중", "성격": "중"},
    "부이브이": {"성별": "M", "출생년도": "82년생", "지역": "목2동", "가입일자": "2026-09-04", "월1회_참석여부": "미참석", "최근참석일": "2026-09-04", "활동특징": "-", "외모": "중", "성격": "중"},
    "이클립스": {"성별": "M", "출생년도": "85년생", "지역": "불광제1동", "가입일자": "2026-09-08", "월1회_참석여부": "미참석", "최근참석일": "2026-09-08", "활동특징": "-", "외모": "중", "성격": "중"},
    "혀날도": {"성별": "M", "출생년도": "85년생", "지역": "북가좌동", "가입일자": "2026-09-13", "월1회_참석여부": "미참석", "최근참석일": "2026-09-13", "활동특징": "-", "외모": "중", "성격": "중"},
    "두루미": {"성별": "M", "출생년도": "88년생", "지역": "홍은동", "가입일자": "2026-09-14", "월1회_참석여부": "미참석", "최근참석일": "2026-09-14", "활동특징": "-", "외모": "중", "성격": "중"},
    "공주영": {"성별": "M", "출생년도": "89년생", "지역": "홍은동", "가입일자": "2026-09-16", "월1회_참석여부": "미참석", "최근참석일": "2026-09-16", "활동특징": "-", "외모": "중", "성격": "중"},
    "슈퍼홍": {"성별": "M", "출생년도": "89년생", "지역": "마두1동", "가입일자": "2026-09-17", "월1회_참석여부": "미참석", "최근참석일": "2026-09-17", "활동특징": "-", "외모": "중", "성격": "중"},
    "데이빗": {"성별": "M", "출생년도": "90년생", "지역": "홍은제2동", "가입일자": "2026-09-28", "월1회_참석여부": "미참석", "최근참석일": "2026-09-28", "활동특징": "-", "외모": "중", "성격": "중"},
    "리키": {"성별": "M", "출생년도": "88년생", "지역": "북가좌제2동", "가입일자": "2026-09-28", "월1회_참석여부": "미참석", "최근참석일": "2026-09-28", "활동특징": "-", "외모": "중", "성격": "중"},
    "메크리": {"성별": "M", "출생년도": "87년생", "지역": "신사동", "가입일자": "2026-09-30", "월1회_참석여부": "미참석", "최근참석일": "2026-09-30", "활동특징": "-", "외모": "중", "성격": "중"},
    "벡스": {"성별": "M", "출생년도": "82년생", "지역": "녹번동", "가입일자": "2026-10-02", "월1회_참석여부": "미참석", "최근참석일": "2026-10-02", "활동특징": "-", "외모": "중", "성격": "중"},
    "또유니": {"성별": "M", "출생년도": "86년생", "지역": "상수동", "가입일자": "2026-10-03", "월1회_참석여부": "미참석", "최근참석일": "2026-10-03", "활동특징": "-", "외모": "중", "성격": "중"},
    "콩이": {"성별": "F", "출생년도": "85년생", "지역": "홍제제3동", "가입일자": "2026-10-04", "월1회_참석여부": "미참석", "최근참석일": "2026-10-04", "활동특징": "-", "외모": "중", "성격": "중"},
    "줄스": {"성별": "F", "출생년도": "83년생", "지역": "대조동", "가입일자": "2026-10-06", "월1회_참석여부": "미참석", "최근참석일": "2026-10-06", "활동특징": "-", "외모": "중", "성격": "중"},
    "우지": {"성별": "M", "출생년도": "90년생", "지역": "역촌동", "가입일자": "2026-10-06", "월1회_참석여부": "미참석", "최근참석일": "2026-10-06", "활동특징": "-", "외모": "중", "성격": "중"},
    "호야": {"성별": "M", "출생년도": "82년생", "지역": "구산동", "가입일자": "2026-10-11", "월1회_참석여부": "미참석", "최근참석일": "2026-10-11", "활동특징": "-", "외모": "중", "성격": "중"}
}

def extract_emoji(text):
    """텍스트에서 이모티콘만 추출하는 함수"""
    emojis = re.findall(r'[\U00010000-\U0010ffff\u2600-\u27ff]', text)
    return emojis[0] if emojis else None

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if data:
                    return data
        except:
            pass
    save_data(INITIAL_MEMBERS)
    return INITIAL_MEMBERS

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

members = load_data()

# 커플(동일한 이모티콘 보유 회원) 맵핑 생성
emoji_map = {}
for uid in members.keys():
    emo = extract_emoji(uid)
    if emo:
        emoji_map.setdefault(emo, []).append(uid)

couple_dict = {}
for emo, uids in emoji_map.items():
    if len(uids) > 1:
        for u in uids:
            partner = [other for other in uids if other != u]
            couple_dict[u] = partner

# --- Custom CSS ---
st.markdown("""
    <style>
    .custom-title {
        font-size: 24px !important;
        font-weight: bold;
        color: #ff6f0f;
        margin-bottom: 2px;
    }
    .custom-caption {
        font-size: 13px;
        color: #666666;
        margin-bottom: 15px;
    }
    button[data-baseweb="tab"] {
        font-size: 15px !important;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# --- 상단 헤더 ---
st.markdown('<div class="custom-title">🥕3040솔로메이트 어드민🥕</div>', unsafe_allow_html=True)
st.markdown('<div class="custom-caption">초보 운영자를 위한 직관적인 회원 관리 도구</div>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📋 회원 목록", "➕ 회원 등록", "⚙️ 참석 관리"])

today = date.today()

# [TAB 1] 회원 목록
with tab1:
    st.subheader("전체 회원 현황")
    if not members:
        st.info("아직 등록된 회원이 없습니다.")
    else:
        col_search, col_sort = st.columns([2, 1])
        with col_search:
            search_query = st.text_input("🔍 검색 (아이디/지역/출생년도)", placeholder="검색어를 입력하세요...")
        with col_sort:
            sort_order = st.selectbox("정렬 순서", ["가입일 최신순", "가입일 오래된순", "아이디순"])

        filtered_members = members
        if search_query:
            filtered_members = {
                uid: info for uid, info in members.items()
                if search_query.lower() in uid.lower() 
                or search_query in info.get('지역', '')
                or search_query in info.get('출생년도', '')
            }

        member_items = list(filtered_members.items())
        if sort_order == "가입일 최신순":
            member_items.sort(key=lambda x: x[1].get("가입일자", "1900-01-01"), reverse=True)
        elif sort_order == "가입일 오래된순":
            member_items.sort(key=lambda x: x[1].get("가입일자", "1900-01-01"))
        elif sort_order == "아이디순":
            member_items.sort(key=lambda x: x[0])

        st.metric(label="총 회원 수", value=f"{len(member_items)} 명")

        for uid, info in member_items:
            last_date_str = info.get("최근참석일", str(today))
            try:
                last_date = datetime.strptime(last_date_str, "%Y-%m-%d").date()
                days_passed = (today - last_date).days
            except:
                days_passed = 0

            if days_passed > 30:
                count_status = f"⚠️ {days_passed}일 경과"
            else:
                count_status = f"✅ D+{days_passed}일"

            badge = "✅ 참석" if info.get("월1회_참석여부") == "참석" else "❌ 미참석"
            birth_year = info.get("출생년도", "미입력")
            join_date = info.get("가입일자", "미입력")
            
            # 커플 여부 텍스트 추가
            couple_badge = ""
            if uid in couple_dict:
                partners = ", ".join(couple_dict[uid])
                couple_badge = f" | 👩‍❤️‍👨 커플 ({partners})"

            with st.expander(f"👤 {uid} ({info['성별']} / {birth_year}){couple_badge} | 가입: {join_date}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**🎂 출생년도:** {birth_year}")
                    st.write(f"**📍 지역:** {info['지역']}")
                    st.write(f"**📅 가입일자:** {join_date}")
                    st.write(f"**✨ 외모:** {info.get('외모', '중')}")
                with col2:
                    st.write(f"**💖 성격:** {info.get('성격', '중')}")
                    st.write(f"**⏳ 참석 경과:** {days_passed}일 째 ({count_status})")
                    st.write(f"**📌 월1회 상태:** {info.get('월1회_참석여부', '미참석')}")
                    st.write(f"**🕒 최근 참석일:** {last_date_str}")
                
                if uid in couple_dict:
                    st.info(f"👩‍❤️‍👨 **커플 매칭 회원:** {', '.join(couple_dict[uid])}")

                st.write(f"**📝 활동 특징:** {info.get('활동특징', '-')}")
                
                if st.button(f"🗑️ {uid} 삭제", key=f"del_{uid}"):
                    del members[uid]
                    save_data(members)
                    st.success(f"{uid} 회원이 삭제되었습니다.")
                    st.rerun()

# [TAB 2] 회원 등록
with tab2:
    st.subheader("신규 회원 등록")
    with st.form("add_member_form", clear_on_submit=True):
        user_id = st.text_input("아이디 (이모티콘 포함 가능)", placeholder="예: 당근이👑")
        gender = st.radio("성별", ["F", "M"], horizontal=True)
        birth_year_input = st.text_input("출생년도", placeholder="예: 85년생 또는 1985")
        region = st.text_input("지역", placeholder="예: 강남구 역삼동")
        join_date_input = st.date_input("가입일자", value=today)
        
        attendance = st.radio("이번 달 참석 여부", ["참석", "미참석"], horizontal=True)
        attend_date = st.date_input("최근 참석 날짜", value=today)
        
        feature = st.text_area("활동 특징", placeholder="예: 주말 모임 선호, 친화력 좋음", value="-")
        
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
                    "가입일자": str(join_date_input),
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
