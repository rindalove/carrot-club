import streamlit as st
import json, os, re
from datetime import datetime, date

st.set_page_config(page_title="🩷3040솔로메이트어드민🩵", page_icon="🥕", layout="centered")

DATA_FILE = "club_members.json"
CONFIG_FILE = "app_config.json"

# 📸 이미지 기반 검수 완료 회원 명단 (부이브이, 혀날도, 슈퍼홍, 리키 제외)
RAW_DATA = [
    ("보리", "F", "86년생", "갈현동", "2025-03-24"),
    ("쥬니👑", "F", "85년생", "북가좌제2동", "2025-03-24"),
    ("바론이", "F", "83년생", "신사동", "2025-03-26"),
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
    ("두나", "F", "89년생", "북가좌동", "2026-08-20"),
    ("땅콩", "M", "86년생", "북가좌제2동", "2026-08-29"),
    ("보미", "F", "85년생", "서교동", "2026-08-31"),
    ("서율", "M", "88년생", "가양제3동", "2026-09-04"),
    ("이클립스", "M", "85년생", "불광제1동", "2026-09-08"),
    ("두루미", "M", "88년생", "홍은동", "2026-09-14"),
    ("공주영", "M", "89년생", "홍은동", "2026-09-16"),
    ("데이빗", "M", "90년생", "홍은제2동", "2026-09-28"),
    ("메크리", "M", "87년생", "신사동", "2026-09-30"),
    ("벡스", "M", "82년생", "녹번동", "2026-10-02"),
    ("또유니", "M", "86년생", "상수동", "2026-10-03"),
    ("콩이", "F", "85년생", "홍제제3동", "2026-10-04"),
    ("줄스", "F", "83년생", "대조동", "2026-10-06"),
    ("우지", "M", "90년생", "역촌동", "2026-10-06"),
    ("호야", "M", "82년생", "구산동", "2026-10-11")
]

DEFAULT_NOTICE = """📢 3040솔로메이트 모임 공지사항

1. 한 달(30일)에 적어도 1회 이상 오프라인 모임 참석은 필수입니다.
2. 닉네임 양식을 반드시 준수해 주세요 (예: 바론이(여/83/새절)).
3. 매너 있는 소통과 모임 참여를 당부드립니다!"""

ADMIN_ROLES = {
    "쥬니👑": "방장",
    "바론이": "부방장",
    "개동👑": "부방장",
    "보리": "부방장"
}

def get_initial_data():
    data = {}
    for u, g, b, r, j in RAW_DATA:
        role = ADMIN_ROLES.get(u, "해당없음")
        data[u] = {
            "성별": g, "출생년도": b, "지역": r, "가입일자": j, 
            "월1회_참석여부": "미참석", "최근참석일": j, "활동특징": "-", 
            "외모": "중", "성격": "중", "운영진": (u in ADMIN_ROLES),
            "운영진직책": role, "후기작성여부": "미작성"
        }
    return data

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                d = json.load(f)
                if isinstance(d, dict) and len(d) > 0:
                    for u in d:
                        if "후기작성여부" not in d[u]:
                            d[u]["후기작성여부"] = "미작성"
                    return d
        except:
            pass
    init_d = get_initial_data()
    save_data(init_d)
    return init_d

def save_data(d):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=4)

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    cfg = {"notice": DEFAULT_NOTICE}
    save_config(cfg)
    return cfg

def save_config(cfg):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=4)

members = load_data()
app_config = load_config()

# 커플 자동 매칭 (이모지 기반 및 수동 설정)
couple_dict = {
    "쥬니👑": ["개동👑"],
    "개동👑": ["쥬니👑"]
}

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

st.markdown("<h3 style='color:#ff6f0f; margin-bottom:5px;'>🩷3040솔로메이트어드민🩵</h3>", unsafe_allow_html=True)

# 메인 상단 메뉴명 및 아이콘 적용
tab1, tab2, tab3, tab4 = st.tabs(["📋 전체 회원", "📊 한달 참석", "➕ 신규 회원 등록", "📢 공지사항"])
today = date.today()

# [TAB 1] 전체 회원
with tab1:
    st.subheader("전체 회원 현황 및 관리")

    c1, c2 = st.columns([2, 1])
    sq = c1.text_input("🔍 검색", placeholder="이름/지역/출생")
    so = c2.selectbox("정렬", ["가입 최신", "가입 오래된", "이름순"])

    filtered = {u: i for u, i in members.items() if not sq or sq.lower() in u.lower() or sq in i.get('지역','') or sq in i.get('출생년도','')}
    items = list(filtered.items())

    if so == "가입 최신":
        items.sort(key=lambda x: x[1].get("가입일자", ""), reverse=True)
    elif so == "가입 오래된":
        items.sort(key=lambda x: x[1].get("가입일자", ""))
    else:
        items.sort(key=lambda x: x[0])

    items.sort(key=lambda x: 0 if x[1].get("운영진", False) else 1)

    st.metric("현재 총 회원 수", f"{len(items)} 명")

    for uid, info in items:
        ld_str = info.get("최근참석일", str(today))
        try:
            dp = (today - datetime.strptime(ld_str, "%Y-%m-%d").date()).days
        except:
            dp = 0

        st_txt = f"⚠️ {dp}일 경과" if dp > 30 else f"✅ D+{dp}일"
        
        role_badges = []
        if info.get("운영진", False):
            role_title = info.get("운영진직책", "운영진")
            role_badges.append(f"🟢 {role_title}")
        if uid in couple_dict:
            role_badges.append(f"👩‍❤️‍👨 커플: {', '.join(couple_dict[uid])}")
        
        badge_str = f" | {' | '.join(role_badges)}" if role_badges else ""
        
        with st.expander(f"👤 {uid} ({info['성별']}/{info.get('출생년도','미입력')}){badge_str}"):
            ca, cb = st.columns(2)
            
            # 요청하신 개인 정보 상세 내용 순서 반영
            ca.write(f"**📍 지역:** {info['지역']}")
            ca.write(f"**📅 가입일자:** {info.get('가입일자','-')}")
            ca.write(f"**📌 최근 벙참여:** {ld_str}")
            ca.write(f"**⏳ 경과일자:** {dp}일 ({st_txt})")
            
            cb.write(f"**✍️ 후기작성:** {info.get('후기작성여부','미작성')}")
            cb.write(f"**✨ 외모:** {info.get('외모','중')}")
            cb.write(f"**💖 성격:** {info.get('성격','중')}")
            
            st.write(f"**📝 특징:** {info.get('활동특징','-')}")
            
            st.write("---")
            
            edit_key = f"show_edit_{uid}"
            if edit_key not in st.session_state:
                st.session_state[edit_key] = False

            col_btn1, col_btn2 = st.columns([1, 1])
            with col_btn1:
                if st.button("✏️ 정보수정", key=f"edit_btn_{uid}", use_container_width=True):
                    st.session_state[edit_key] = not st.session_state[edit_key]
                    st.rerun()
            with col_btn2:
                if st.button("🗑️ 삭제", key=f"del_btn_{uid}", use_container_width=True):
                    del members[uid]
                    save_data(members)
                    st.success(f"[{uid}] 회원이 삭제되었습니다.")
                    st.rerun()

            if st.session_state[edit_key]:
                st.info(f"⚙️ **{uid}** 회원 정보수정")
                with st.form(key=f"form_edit_{uid}"):
                    fe_gender = st.radio("성별", ["F", "M"], index=0 if info["성별"] == "F" else 1, horizontal=True)
                    fe_birth = st.text_input("출생년도", value=info.get("출생년도", ""))
                    fe_region = st.text_input("지역", value=info.get("지역", ""))
                    
                    try:
                        curr_j = datetime.strptime(info.get("가입일자", str(today)), "%Y-%m-%d").date()
                    except: curr_j = today
                    fe_join = st.date_input("가입일자", value=curr_j)

                    # 캘린더 현재 연도(2026년 등) 세팅 반영
                    try:
                        curr_a = datetime.strptime(info.get("최근참석일", str(today)), "%Y-%m-%d").date()
                    except: curr_a = today
                    fe_att_date = st.date_input("최근 벙참여 날짜", value=curr_a)

                    fe_is_admin = st.checkbox("🟢 운영진 여부", value=info.get("운영진", False))
                    curr_r = info.get("운영진직책", "해당없음")
                    r_opts = ["방장", "부방장", "운영진", "해당없음"]
                    r_idx = r_opts.index(curr_r) if curr_r in r_opts else 3
                    fe_role = st.selectbox("운영진 직책", r_opts, index=r_idx)

                    fe_att_status = st.radio("월1회 참석 상태", ["참석", "미참석"], index=0 if info.get("월1회_참석여부") == "참석" else 1, horizontal=True)
                    
                    curr_review = info.get("후기작성여부", "미작성")
                    rev_opts = ["작성완료", "미작성"]
                    rev_idx = rev_opts.index(curr_review) if curr_review in rev_opts else 1
                    fe_review_status = st.radio("후기작성 여부", rev_opts, index=rev_idx, horizontal=True)

                    fe_feature = st.text_area("특징", value=info.get("활동특징", "-"))
                    fe_looks = st.select_slider("외모", ["하", "중", "상"], value=info.get("외모", "중"))
                    fe_personality = st.select_slider("성격", ["하", "중", "상"], value=info.get("성격", "중"))

                    if st.form_submit_button("💾 정보 변경사항 저장"):
                        members[uid] = {
                            "성별": fe_gender, "출생년도": fe_birth, "지역": fe_region,
                            "가입일자": str(fe_join), "최근참석일": str(fe_att_date),
                            "월1회_참석여부": fe_att_status, "활동특징": fe_feature,
                            "외모": fe_looks, "성격": fe_personality, 
                            "운영진": fe_is_admin, "운영진직책": fe_role if fe_is_admin else "해당없음",
                            "후기작성여부": fe_review_status
                        }
                        save_data(members)
                        st.session_state[edit_key] = False
                        st.success(f"[{uid}] 회원 정보 저장이 완료되었습니다!")
                        st.rerun()

# [TAB 2] 한달 참석
with tab2:
    st.subheader("📊 한 달(30일) 참석 현황 분석")
    
    attended_list = []
    over_list = []
    normal_list = []
    
    for uid, info in members.items():
        ld_str = info.get("최근참석일", str(today))
        try:
            dp = (today - datetime.strptime(ld_str, "%Y-%m-%d").date()).days
        except:
            dp = 0
            
        if info.get("월1회_참석여부") == "참석":
            attended_list.append((uid, info, dp))
            
        if dp > 30:
            over_list.append((uid, info, dp))
        else:
            normal_list.append((uid, info, dp))
            
    m1, m2, m3 = st.columns(3)
    m1.metric("이번달 참석", f"{len(attended_list)}명")
    m2.metric("30일 이내", f"{len(normal_list)}명")
    m3.metric("⚠️ 30일 초과", f"{len(over_list)}명")
    
    st.write("---")
    st.write("### ⚠️ 한 달(30일) 초과 미참석 회원 목록")
    if not over_list:
        st.success("모든 회원이 30일 이내에 모임에 참여 중입니다!")
    else:
        for uid, info, dp in over_list:
            st.warning(f"👤 **{uid}** ({info['지역']}) - 최근 벙참여: {info.get('최근참석일','-')} (**{dp}일 지남**)")

# [TAB 3] 신규 회원 등록
with tab3:
    st.subheader("신규 회원 등록")
    with st.form("add_form", clear_on_submit=True):
        uid = st.text_input("아이디 (필수)")
        gen = st.radio("성별", ["F", "M"], horizontal=True)
        by = st.text_input("출생년도 (예: 85년생)")
        reg = st.text_input("지역")
        jd = st.date_input("가입일자", value=today)
        is_admin_check = st.checkbox("🟢 운영진 권한 부여")
        new_role = st.selectbox("운영진 직책", ["부방장", "방장", "운영진"])
        att = st.radio("참석여부", ["참석", "미참석"], horizontal=True)
        rev_reg = st.radio("후기작성 여부", ["작성완료", "미작성"], horizontal=True)
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
                    "운영진": is_admin_check, "운영진직책": new_role if is_admin_check else "해당없음",
                    "후기작성여부": rev_reg
                }
                save_data(members)
                st.success(f"🎉 [{uid}] 회원이 성공적으로 등록되었습니다!")
                st.rerun()

# [TAB 4] 공지사항
with tab4:
    st.subheader("📢 공지사항")
    
    if "edit_notice" not in st.session_state:
        st.session_state["edit_notice"] = False
        
    st.info("📌 모임 주요 공지사항 및 운영 지침입니다.")
    st.code(app_config.get("notice", DEFAULT_NOTICE), language=None)
    
    if st.button("✏️ 정보수정", key="btn_edit_notice"):
        st.session_state["edit_notice"] = not st.session_state["edit_notice"]
        st.rerun()
        
    if st.session_state["edit_notice"]:
        with st.form("form_notice_edit"):
            new_notice = st.text_area("공지 게시판 내용 입력 및 수정", value=app_config.get("notice", DEFAULT_NOTICE), height=200)
            if st.form_submit_button("💾 공지사항 저장"):
                app_config["notice"] = new_notice
                save_config(app_config)
                st.session_state["edit_notice"] = False
                st.success("공지 게시판 내용이 성공적으로 저장되었습니다!")
                st.rerun()
