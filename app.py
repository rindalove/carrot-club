import streamlit as st
import json, os, re
from datetime import datetime, date

st.set_page_config(page_title="3040솔로메이트 어드민", page_icon="🥕", layout="centered")

DATA_FILE = "club_members.json"
BACKUP_FILE = "club_members_backup.json"  # 🛡️ 2중 백업 안전장치 파일
CONFIG_FILE = "app_config.json"

# 📸 이미지 기반 검수 완료 회원 명단 (신규 회원 3명 포함)
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
    ("헬기", "M", "86년생", "증산동", "2026-10-21"),
    ("덕배", "M", "88년생", "향동", "2026-10-21"),
    ("베인", "F", "85년생", "응암동", "2026-10-23")
]

DEFAULT_GUIDE = """🩷솔로메이트 친목모임🩵
안녕하세요 00님☺️
가입신청하셔서 인사드립니다!

가입전 절차로 몇가지 여쭤볼께요~😺
✅️기혼,돌싱,애인있음에 해당안되시죠?
✅️현재 서대문,은평,마포구
동네모임을 여러곳 가입하여
활동중이신가요


네 그러시군요 ~
저희모임같은 동네친구모임을
여러군데 가입하여 활동하시는분을
지양하고 있어서 여쭤봤어요😿

저희는 소속감있게 친목중심의
모임만들기를 추구하고 있습니당 ^-^
( 친목중심으로 취미활동 소소하게
같이 할 모임을 찾으신다면
저희모임이랑 잘 맞으실꺼예요~ )

다만 다른 모임 가입하셨어도 
그쪽으로만 기울지않고😁
저희모임활동 꾸준히 활동 잘 해주신다면 가입 가능하셔요☘️☺️

(⭐️혹시나 다른 모임 일정과 하루안에 두탕? 스케줄 잡는 일은 없으셨음 해요
생각보다 매너없는분들이 많다보니
염려되어 더 미리미리 말씀드리게 되는점이해 부탁드려요🙏)


그리고 저희는 적어도 ✅️한달에 한번
오프라인벙에 ✅️필수 참여하시는게 멤버유지조건인데 가능하실까요?

✅️혹시 주말에 쉬시는 직업이신가요?
평일에는 퇴근후 저녁식사벙(간술,논알
콜) 등이 가끔 열리구요~
주말에는 맛집,취미벙들이 열리고
금,토,일요일에 열리는 경우가 훨씬 많아서요☺️

그럼 저희 🩷솔로메이트 친목모임🩵 활동 도전해보시겠어요? ^-^ 
지금 닉네임 수정하시면 승인해 드릴께요!

닉네임 양식: 이름(성별/생년연도/지역)
- 예시: 바론이(여/83/새절)

입장하시고 닉네임 수정하시고 가입 인사 부탁 드려요 😊"""

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
            "운영진직책": role
        }
    return data

# 🛡️ 2중 안전 복구 로직 (메인 파일 없으면 백업 파일에서 즉시 복원)
def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                d = json.load(f)
                if isinstance(d, dict) and len(d) > 0:
                    return d
        except:
            pass
            
    if os.path.exists(BACKUP_FILE):
        try:
            with open(BACKUP_FILE, "r", encoding="utf-8") as f:
                d = json.load(f)
                if isinstance(d, dict) and len(d) > 0:
                    save_data(d)  # 메인 파일 복구
                    return d
        except:
            pass
            
    init_d = get_initial_data()
    save_data(init_d)
    return init_d

# 🛡️ 2중 동시 저장 로직 (메인 파일과 백업 파일에 동시에 기록)
def save_data(d):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=4)
    with open(BACKUP_FILE, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=4)

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    cfg = {"guide": DEFAULT_GUIDE, "notice": DEFAULT_NOTICE}
    save_config(cfg)
    return cfg

def save_config(cfg):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=4)

members = load_data()
app_config = load_config()

# 커플 매칭
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

st.markdown("<h3 style='color:#ff6f0f; margin-bottom:5px;'>🩷3040솔로메이트 어드민🩵</h3>", unsafe_allow_html=True)

# 상단 메뉴: '한달 참석' -> '45일 미참석'으로 변경 반영
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📋 회원 목록", "📊 45일 미참석", "➕ 회원 등록", "💬 인터뷰 가이드", "📢 공지 게시판"])
today = date.today()

# [TAB 1] 회원 목록
with tab1:
    st.subheader("전체 회원 현황 및 관리")

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

    # 🟢 그린 왕관 운영진 최상단 배치
    items.sort(key=lambda x: 0 if x[1].get("운영진", False) else 1)

    st.metric("현재 총 회원 수", f"{len(items)} 명")

    for uid, info in items:
        ld_str = info.get("최근참석일", str(today))
        try:
            dp = (today - datetime.strptime(ld_str, "%Y-%m-%d").date()).days
        except:
            dp = 0

        # 45일 기준 경고 표시
        st_txt = f"⚠️ {dp}일 경과" if dp > 45 else f"✅ D+{dp}일"
        
        role_badges = []
        if info.get("운영진", False):
            role_title = info.get("운영진직책", "운영진")
            role_badges.append(f"🟢 {role_title}")
        if uid in couple_dict:
            role_badges.append(f"👩‍❤️‍👨 커플 ({', '.join(couple_dict[uid])})")
        
        badge_str = f" | {' | '.join(role_badges)}" if role_badges else ""
        
        with st.expander(f"👤 {uid} ({info['성별']}/{info.get('출생년도','미입력')}){badge_str} | 가입: {info.get('가입일자','-')}"):
            ca, cb = st.columns(2)
            
            ca.write(f"**📍 지역:** {info['지역']}")
            ca.write(f"**📅 가입일자:** {info.get('가입일자','-')}")
            ca.write(f"**✨ 외모 평가:** {info.get('외모','중')}")
            
            cb.write(f"**💖 성격 평가:** {info.get('성격','중')}")
            cb.write(f"**⏳ 참석 경과:** {dp}일 ({st_txt})")
            cb.write(f"**📌 최근 참석일:** {ld_str}")
            
            st.write(f"**📝 활동 특징:** {info.get('활동특징','-')}")
            
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

                    try:
                        curr_a = datetime.strptime(info.get("최근참석일", str(today)), "%Y-%m-%d").date()
                    except: curr_a = today
                    fe_att_date = st.date_input("최근 참석 날짜", value=curr_a)

                    fe_is_admin = st.checkbox("🟢 운영진 여부", value=info.get("운영진", False))
                    curr_r = info.get("운영진직책", "해당없음")
                    r_opts = ["방장", "부방장", "운영진", "해당없음"]
                    r_idx = r_opts.index(curr_r) if curr_r in r_opts else 3
                    fe_role = st.selectbox("운영진 직책", r_opts, index=r_idx)

                    fe_att_status = st.radio("참석 상태", ["참석", "미참석"], index=0 if info.get("월1회_참석여부") == "참석" else 1, horizontal=True)
                    fe_feature = st.text_area("활동 특징", value=info.get("활동특징", "-"))
                    fe_looks = st.select_slider("외모", ["하", "중", "상"], value=info.get("외모", "중"))
                    fe_personality = st.select_slider("성격", ["하", "중", "상"], value=info.get("성격", "중"))

                    if st.form_submit_button("💾 정보 변경사항 저장"):
                        members[uid] = {
                            "성별": fe_gender, "출생년도": fe_birth, "지역": fe_region,
                            "가입일자": str(fe_join), "최근참석일": str(fe_att_date),
                            "월1회_참석여부": fe_att_status, "활동특징": fe_feature,
                            "외모": fe_looks, "성격": fe_personality, 
                            "운영진": fe_is_admin, "운영진직책": fe_role if fe_is_admin else "해당없음"
                        }
                        save_data(members)
                        st.session_state[edit_key] = False
                        st.success(f"[{uid}] 회원 정보 저장이 완료되었습니다!")
                        st.rerun()

    st.write("---")
    if st.button("🔄 기본 명단으로 강제 초기화/리셋", use_container_width=True):
        init_d = get_initial_data()
        save_data(init_d)
        st.success("기본 명단으로 초기화되었습니다!")
        st.rerun()

# [TAB 2] 45일 미참석 (기준 변경 및 지나간 일자 확인 기능)
with tab2:
    st.subheader("📊 45일 초과 미참석 회원 분석")
    
    over_45_list = []
    normal_list = []
    
    for uid, info in members.items():
        ld_str = info.get("최근참석일", str(today))
        try:
            dp = (today - datetime.strptime(ld_str, "%Y-%m-%d").date()).days
        except:
            dp = 0
            
        if dp > 45:
            over_45_list.append((uid, info, dp))
        else:
            normal_list.append((uid, info, dp))
            
    m1, m2 = st.columns(2)
    m1.metric("45일 이내 정상 활동", f"{len(normal_list)} 명")
    m2.metric("⚠️ 45일 초과 미참석", f"{len(over_45_list)} 명")
    
    st.write("---")
    st.write("### ⚠️ 45일 이상 미참석 회원 목록 (지나간 일자 확인)")
    if not over_45_list:
        st.success("모든 회원이 45일 이내에 모임에 참여 중입니다!")
    else:
        for uid, info, dp in over_45_list:
            st.warning(f"👤 **{uid}** ({info['성별']}/{info.get('출생년도','미입력')} | {info['지역']}) — 최근 참석일: {info.get('최근참석일','-')} (**총 {dp}일 지남**)")

# [TAB 3] 회원 등록
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
                    "운영진": is_admin_check, "운영진직책": new_role if is_admin_check else "해당없음"
                }
                save_data(members)
                st.success(f"🎉 [{uid}] 회원이 성공적으로 등록되었습니다!")
                st.rerun()

# [TAB 4] 인터뷰 가이드
with tab4:
    st.subheader("💬 신규 회원 가입 인터뷰 가이드")
    
    if "edit_guide" not in st.session_state:
        st.session_state["edit_guide"] = False
        
    st.info("💡 아래 문구를 복사해서 신규 가입 신청자에게 안내 메시지로 보내세요.")
    st.code(app_config.get("guide", DEFAULT_GUIDE), language=None)
    
    if st.button("✏️ 정보수정", key="btn_edit_guide"):
        st.session_state["edit_guide"] = not st.session_state["edit_guide"]
        st.rerun()
        
    if st.session_state["edit_guide"]:
        with st.form("form_guide_edit"):
            new_guide = st.text_area("인터뷰 가이드 문구 내용 수정", value=app_config.get("guide", DEFAULT_GUIDE), height=350)
            if st.form_submit_button("💾 가이드 문구 저장"):
                app_config["guide"] = new_guide
                save_config(app_config)
                st.session_state["edit_guide"] = False
                st.success("인터뷰 가이드 문구가 성공적으로 저장되었습니다!")
                st.rerun()

# [TAB 5] 공지 게시판
with tab5:
    st.subheader("📢 운영진 공지 게시판")
    
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
