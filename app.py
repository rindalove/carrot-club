import streamlit as st
import json, os, re
from datetime import datetime, date

# 모바일 페이지 기본 설정
st.set_page_config(page_title="3040솔로메이트 어드민", page_icon="🥕", layout="centered")

DATA_FILE = "club_members.json"

# 📸 53명 회원 전체 데이터 목록
RAW_DATA = [
    ("보리👑", "F", "86년생", "갈현동", "2025-03-24"), ("쥬니👑", "F", "85년생", "북가좌제2동", "2025-03-24"),
    ("바론이👑", "F", "83년생", "신사동", "2025-03-26"), ("이예💎", "F", "89년생", "불광제2동", "2025-05-02"),
    ("쟈연", "F", "90년생", "녹번동", "2025-05-27"), ("윤철", "M", "84년생", "북가좌동", "2025-07-06"),
    ("낮도깨비", "F", "88년생", "불광동", "2025-09-02"), ("유미🍀", "F", "88년생", "갈현제1동", "2025-09-20"),
    ("조은💎", "M", "90년생", "남가좌동", "2025-10-15"), ("jin", "M", "86년생", "상암동", "2025-11-17"),
    ("우루루", "M", "86년생", "망원제1동", "2025-11-18"), ("꾸꿍🐷", "F", "89년생", "응암제3동", "2025-11-18"),
    ("개동👑", "M", "87년생", "응암동", "2025-12-09"), ("그레이", "F", "90년생", "성산동", "2025-12-16"),
    ("용진", "M", "84년생", "북가좌제1동", "2026-01-05"), ("희희", "F", "91년생", "성산동", "2026-01-19"),
    ("농뇽", "F", "88년생", "성산동", "2026-01-26"), ("마포🍀", "M", "90년생", "성산제2동", "2026-02-27"),
    ("레이", "F", "84년생", "연희동", "2026-03-02"), ("제이", "M", "83년생", "홍은제2동", "2026-03-09"),
    ("머핀", "F", "86년생", "삼산동", "2026-03-15"), ("하리", "F", "87년생", "응암제1동", "2026-03-31"),
    ("힘내자", "F", "86년생", "연희동", "2026-04-23"), ("기강승🐷", "M", "89년생", "신사동", "2026-07-02"),
    ("로나", "F", "87년생", "북가좌동", "2026-07-05"), ("상이", "M", "91년생", "효창동", "2026-07-06"),
    ("말타", "M", "86년생", "연남동", "2026-07-16"), ("포톤", "M", "87년생", "녹번동", "2026-07-17"),
    ("만물상아재", "M", "87년생", "영등포동4가", "2026-07-22"), ("토토", "F", "87년생", "서초1동", "2026-07-31"),
    ("라디", "M", "90년생", "신사동", "2026-07-31"), ("은호", "F", "88년생", "상수동", "2026-08-02"),
    ("쩡히", "F", "86년생", "역촌동", "2026-08-13"), ("시계", "M", "88년생", "연남동", "2026-08-18"),
    ("보미", "F", "85년생", "서교동", "2026-08-31"), ("서율", "M", "88년생", "가양제3동", "2026-09-04"),
    ("부이브이", "M", "82년생", "목2동", "2026-09-04"), ("이클립스", "M", "85년생", "불광제1동", "2026-09-08"),
    ("혀날도", "M", "85년생", "북가좌동", "2026-09-13"), ("두루미", "M", "88년생", "홍은동", "2026-09-14"),
    ("공주영", "M", "89년생", "홍은동", "2026-09-16"), ("슈퍼홍", "M", "89년생", "마두1동", "2026-09-17"),
    ("데이빗", "M", "90년생", "홍은제2동", "2026-09-28"), ("리키", "M", "88년생", "북가좌제2동", "2026-09-28"),
    ("메크리", "M", "87년생", "신사동", "2026-09-30"), ("벡스", "M", "82년생", "녹번동", "2026-10-02"),
    ("또유니", "M", "86년생", "상수동", "2026-10-03"), ("콩이", "F", "85년생", "홍제제3동", "2026-10-04"),
    ("줄스", "F", "83년생", "대조동", "2026-10-06"), ("우지", "M", "90년생", "역촌동", "2026-10-06"),
    ("호야", "M", "82년생", "구산동", "2026-10-11"), ("운영진1", "M", "85년생", "은평구", "2025-03-01"),
    ("운영진2", "F", "88년생", "마포구", "2025-03-01")
]

INITIAL_MEMBERS = {
    u: {"성별": g, "출생년도": b, "지역": r, "가입일자": j, "월1회_참석여부": "미참석", "최근참석일": j, "활동특징": "-", "외모": "중", "성격": "중"}
    for u, g, b, r, j in RAW_DATA
}

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                d = json.load(f)
                if len(d) == len(INITIAL_MEMBERS):
                    return d
        except:
            pass
    save_data(INITIAL_MEMBERS)
    return INITIAL_MEMBERS

def save_data(d):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=4)

members = load_data()

# 이모티콘 커플 매칭
emoji_map = {}
for uid in members.keys():
    emo = re.findall(r'[\U00010000-\U0010ffff\u2600-\u27ff]', uid)
    if emo:
        emoji_map.setdefault(emo[0], []).append(uid)

couple_dict = {u: [o for o in uids if o != u] for emo, uids in emoji_map.items() if len(uids) > 1 for u in uids}

# 타이틀 수정: 3040솔로메이트 어드민
st.markdown("<h3 style='color:#ff6f0f; margin-bottom:5px;'>🥕3040솔로메이트 어드민🥕</h3>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📋 회원 목록", "➕ 회원 등록", "⚙️ 참석 관리"])
today = date.today()

# [TAB 1] 회원 목록
with tab1:
    st.subheader("전체 회원 현황")
    if st.button("🔄 53명 전체 데이터 초기화/리셋", use_container_width=True):
        save_data(INITIAL_MEMBERS)
        st.rerun()

    c1, c2 = st.columns([2, 1])
    sq = c1.text_input("🔍 검색", placeholder="아이디/지역/출생년도")
    so = c2.selectbox("정렬", ["가입일 최신순", "가입일 오래된순", "아이디순"])

    filtered = {u: i for u, i in members.items() if not sq or sq.lower() in u.lower() or sq in i.get('지역','') or sq in i.get('출생년도','')}
    items = list(filtered.items())

    if so == "가입일 최신순":
        items.sort(key=lambda x: x[1].get("가입일자", ""), reverse=True)
    elif so == "가입일 오래된순":
        items.sort(key=lambda x: x[1].get("가입일자", ""))
    else:
        items.sort(key=lambda x: x[0])

    st.metric("총 회원 수", f"{len(items)} 명")

    for uid, info in items:
        ld_str = info.get("최근참석일", str(today))
        try:
            dp = (today - datetime.strptime(ld_str, "%Y-%m-%d").date()).days
        except:
            dp = 0

        st_txt = f"⚠️ {dp}일 경과" if dp > 30 else f"✅ D+{dp}일"
        cp_txt = f" | 👩‍❤️‍👨 커플 ({', '.join(couple_dict[uid])})" if uid in couple_dict else ""
        
        with st.expander(f"👤 {uid} ({info['성별']}/{info.get('출생년도','미입력')}){cp_txt} | 가입: {info.get('가입일자','-')}"):
            ca, cb = st.columns(2)
            ca.write(f"**📍 지역:** {info['지역']}\n\n**📅 가입:** {info.get('가입일자','-')}\n\n**✨ 외모:** {info.get('외모','중')}")
            cb.write(f"**💖 성격:** {info.get('성격','중')}\n\n**⏳ 경과:** {dp}일 ({st_txt})\n\n**📌 최근참석:** {ld_str}")
            st.write(f"**📝 특징:** {info.get('활동특징','-')}")
            if st.button(f"🗑️ 삭제", key=f"d_{uid}"):
                del members[uid]
                save_data(members)
                st.rerun()

# [TAB 2] 회원 등록
with tab2:
    st.subheader("신규 회원 등록")
    with st.form("add_form", clear_on_
