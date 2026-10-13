import streamlit as st
import json
import os
import re
from datetime import datetime, date

st.set_page_config(page_title="🥕 당근 모임 관리", page_icon="🥕", layout="centered")

DATA_FILE = "club_members.json"

# 📸 검토 완료된 53명 회원 명단 (복사 중 잘림 현상을 완전 방지한 원자적 튜플 구조)
RAW_MEMBER_DATA = [
    ("보리👑", "F", "86년생", "갈현동", "2025-03-24"),
    ("쥬니👑", "F", "85년생", "북가좌제2동", "2025-03-24"),
    ("바론이👑", "F", "83년생", "신사동", "2025-03-26"),
    ("이예💎", "F", "89년생", "불광제2동", "2025-05-02"),
    ("쟈연", "F", "90년생", "녹번동", "2025-05-27"),
    ("윤철", "M", "84년생", "북가좌동", "2025-07-06"),
    ("낮도깨비", "F", "88년생", "불광동", "2025-09-02"),
    ("유미🍀", "F", "88년생", "갈현제1동", "2025-09-20"),
    ("조은💎", "M", "90년생", "남가좌동", "2025-10-15"),
    ("jin", "M", "86년생", "상암동", "2025-11-17"),
    ("우루루", "M", "86년생", "망원제1동", "2025-11-18"),
    ("꾸꿍🐷", "F", "89년생", "응암제3동", "2025-11-18"),
    ("개동👑", "M", "87년생", "응암동", "2025-12-09"),
    ("그레이", "F", "90년생", "성산동", "2025-12-16"),
    ("용진", "M", "84년생", "북가좌제1동", "2026-01-05"),
    ("희희", "F", "91년생", "성산동", "2026-01-19"),
    ("농뇽", "F", "88년생", "성산동", "2026-01-26"),
    ("마포🍀", "M", "90년생", "성산제2동", "2026-02-27"),
    ("레이", "F", "84년생", "연희동", "2026-03-02"),
    ("제이", "M", "83년생", "홍은제2동", "2026-03-09"),
    ("머핀", "F", "86년생", "삼산동", "2026-03-15"),
    ("하리", "F", "87년생", "응암제1동", "2026-03-31"),
    ("힘내자", "F", "86년생", "연희동", "2026-04-23"),
    ("기강승🐷", "M", "89년생", "신사동", "2026-07-02"),
    ("로나", "F", "87년생", "북가좌동", "2026-07-05"),
    ("상이", "M", "91년생", "효창동", "2026-07-06"),
    ("말타", "M", "86년생", "연남동", "2026-07-16"),
    ("포톤", "M", "87년생", "녹번동", "2026-07-17"),
    ("만물상아재", "M", "87년생", "영등포동4가", "2026-07-22"),
    ("토토", "F", "87년생", "서초1동", "2026-07-31"),
    ("라디", "M", "90년생", "신사동", "2026-07-31"),
    ("은호", "F", "88년생", "상수동", "2026-08-02"),
    ("쩡히", "F", "86년생", "역촌동", "2026-08-13"),
    ("시계", "M", "88년생", "연남동", "2026-08-18"),
    ("보미", "F", "85년생", "서교동", "2026-08-31"),
    ("서율", "M", "88년생", "가양제3동", "2026-09-04"),
    ("부이브이", "M", "82년생", "목2동", "2026-09-04"),
    ("이클립스", "M", "85년생", "불광제1동", "2026-09-08"),
    ("혀날도", "M", "85년생", "북가좌동", "2026-09-13"),
    ("두루미", "M", "88년생", "홍은동", "2026-09-14"),
    ("공주영", "M", "89년생", "홍은동", "2026-09-16"),
    ("슈퍼홍", "M", "89년생", "마두1동", "2026-09-17"),
    ("데이빗", "M", "90년생", "홍은제2동", "2026-09-28"),
    ("리키", "M", "88년생", "북가좌제2동", "2026-09-28"),
    ("메크리", "M", "87년생", "신사동", "2026-09-30"),
    ("벡스", "M", "82년생", "녹번동", "2026-10-02"),
    ("또유니", "M", "86년생", "상수동", "2026-10-03"),
    ("콩이", "F", "85년생", "홍제제3동", "2026-10-04"),
    ("줄스", "F", "83년생", "대조동", "2026-10-06"),
    ("우지", "M", "90년생", "역촌동", "2026-10-06"),
    ("호야", "M", "82년생", "구산동", "2026-10-11"),
    ("운영진1", "M", "85년생", "은평구", "2025-03-01"),
    ("운영진2", "F", "88년생", "마포구", "2025-03-01")
]

# Dictionary 변환
INITIAL_MEMBERS = {}
for uid, gender, birth, region, join_date in RAW_MEMBER_DATA:
    INITIAL_MEMBERS[uid] = {
        "성별": gender,
        "출생년도": birth,
        "지역": region,
        "가입일자": join_date,
        "월1회_참석여부": "미참석",
        "최근참석일": join_date,
        "활동특징": "-",
        "외모": "중",
        "성격": "중"
    }

def extract_emoji(text):
    """텍스트에서 이모티콘만 추출"""
    emojis = re.findall(r'[\U00010000-\U0010ffff\u2600-\u27ff]', text)
    return emojis[0] if emojis else None

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if len(data) != len(INITIAL_MEMBERS):
                    save_data(INITIAL_MEMBERS)
                    return INITIAL_MEMBERS
                return data
        except:
            pass
    save_data(INITIAL_MEMBERS)
    return INITIAL_MEMBERS

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

members = load_data()

# 커플(동일한 이모티콘) 매칭
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
    
    if st.button("🔄 53명 회원 전체 강제 리셋/업데이트", use_container_width=True):
        save_data(INITIAL_MEMBERS)
        st.success("53명 전체 데이터로 완벽히 리셋되었습니다!")
        st.rerun()

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
    with st.
