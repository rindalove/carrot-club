import streamlit as st
import json, os, re
from datetime import datetime, date

st.set_page_config(page_title="3040솔로메이트 어드민", page_icon="🥕", layout="centered")

DATA_FILE = "club_members.json"

# 📸 이미지 기반 51명 회원 명단
RAW_DATA = [
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
    ("호야", "M", "82년생", "구산동", "2026-10-11")
]

# 운영진 명단 지정 (바론이, 보리, 쥬니, 개동)
ADMIN_MEMBERS = ["바론이👑", "보리👑", "쥬니👑", "개동👑"]

INITIAL_MEMBERS = {}
for u, g, b, r, j in RAW_DATA:
    INITIAL_MEMBERS[u] = {
        "성별": g, "출생년도": b, "지역": r, "가입일자": j, 
        "월1회_참석여부": "미참석", "최근참석일": j, "활동특징": "-", 
        "외모": "중", "성격": "중", "운영진": (u in ADMIN_MEMBERS)
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

# 커플 자동 매칭 (쥬니👑와 개동👑 커플 직접 지정 및 기타 이모티콘 커플 매칭)
couple_dict = {
    "쥬니👑": ["개동👑"],
    "개동👑": ["쥬니👑"]
}

# 👑가 아닌 다른 이모티콘(💎, 🍀, 🐷 등) 커플 자동 분석
emoji_map = {}
for uid in members.keys():
    emo = re.findall(r'[\U00010000-\U0010ffff\u2600-\u27ff]', uid)
    if emo and emo[0] != "👑":
        emoji_map.setdefault(emo[0], []).append(uid)

for emo, uids in emoji_map.items():
    if len(uids) > 1:
        for u in uids:
            partner = [other for other in uids if other != u]
            couple_dict[u] = partner

st.markdown("<h3 style='color:#ff6f0f; margin-bottom:5px;'>🥕 3040솔로메이트 어드민</h3>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📋 회원 목록", "➕ 회원 등록", "⚙️ 참석 관리"])
today = date.today()

# [TAB 1] 회원 목록
with tab1:
    st.subheader("전체 회원 현황")
    if st.button("🔄 전체 데이터 강제 초기화/리셋", use_container_width=True):
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
        
        # 태그 부여 (운영진 & 커플 병행 표시)
        role_badges = []
        if info.get("운영진", False):
            role_badges.append("👑 운영진")
        if uid in couple_dict:
            role_badges.append(f"👩‍❤️‍👨 커플 ({', '.join(couple_dict[uid])})")
        
        badge_str = f" | {' | '.join(role_badges)}" if role_badges else ""
        
        with st.expander(f"👤 {uid} ({info['성별']}/{info.get('출생년도','미입력')}){badge_str} | 가입: {info.get('가입일자','-')}"):
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
    with st.form("add_form", clear_on_submit=True):
        uid = st.text_input("아이디 (이모티콘 포함 가능)")
        gen = st.radio("성별", ["F", "M"], horizontal=True)
        by = st.text_input("출생년도 (예: 85년생)")
        reg = st.text_input("지역")
        jd = st.date_input("가입일자", value=today)
        is_admin_check = st.checkbox("👑 초록 왕관 운영진 권한 부여")
        att = st.radio("참석여부", ["참석", "미참석"], horizontal=True)
        feat = st.text_area("특징", value="-")
        lk = st.select_slider("외모", ["하", "중", "상"], value="중")
        ps = st.select_slider("성격", ["하", "중", "상"], value="중")
        
        if st.form_submit_button("저장"):
            if not uid.strip():
                st.error("아이디를 입력해주세요!")
            elif uid in members:
                st.error("이미 존재하는 아이디입니다.")
            else:
                members[uid] = {
                    "성별": gen, "출생년도": by or "미입력", "지역": reg, 
                    "가입일자": str(jd), "월1회_참석여부": att, 
                    "최근참석일": str(today), "활동특징": feat, "외모": lk, "성격": ps,
                    "운영진": is_admin_check
                }
                save_data(members)
                st.success("회원이 성공적으로 등록되었습니다!")
                st.rerun()

# [TAB 3] 참석 관리
with tab3:
    st.subheader("참석 상태 관리")
    if members:
        t_uid = st.selectbox("회원 선택", list(members.keys()))
        ns = st.radio("참석 여부", ["참석", "미참석"], horizontal=True)
        nd = st.date_input("참석 날짜", value=today)
        if st.button("업데이트"):
            members[t_uid]["월1회_참석여부"] = ns
            members[t_uid]["최근참석일"] = str(nd)
            save_data(members)
            st.success("참석 정보가 업데이트되었습니다!")
            st.rerun()
