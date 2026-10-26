
import streamlit as st
import json
import os
import tempfile
from pathlib import Path

st.set_page_config(
    page_title="🥕 당근 모임 관리",
    page_icon="🥕",
    layout="centered"
)

# 현재 파이썬 파일과 같은 폴더에 데이터 저장
DATA_FILE = Path(__file__).resolve().parent / "club_members.json"

DEFAULT_MEMBER = {
    "성별": "F",
    "지역": "",
    "월1회_참석여부": "미참석",
    "활동특징": "",
    "외모": "중",
    "성격": "중"
}


def normalize_members(data):
    """회원 데이터 형식 검증 및 누락된 항목 보완."""
    if not isinstance(data, dict):
        raise ValueError("회원 데이터는 JSON 객체 형식이어야 합니다.")

    normalized = {}

    for uid, info in data.items():
        if not isinstance(uid, str) or not uid.strip():
            raise ValueError("회원 아이디가 비어 있거나 올바르지 않습니다.")

        if not isinstance(info, dict):
            raise ValueError(f"{uid} 회원의 정보 형식이 올바르지 않습니다.")

        member = DEFAULT_MEMBER.copy()
        member.update(info)

        if member["성별"] not in ["F", "M"]:
            member["성별"] = "F"

        if member["월1회_참석여부"] not in ["참석", "미참석"]:
            member["월1회_참석여부"] = "미참석"

        for field in ["지역", "활동특징"]:
            if member[field] is None:
                member[field] = ""
            member[field] = str(member[field])

        for field in ["외모", "성격"]:
            if member[field] not in ["상", "중", "하"]:
                member[field] = "중"

        normalized[uid.strip()] = member

    return normalized


def load_data():
    """저장된 회원 정보 불러오기."""
    if not DATA_FILE.exists():
        return {}

    try:
        with DATA_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)

        return normalize_members(data)

    except (OSError, json.JSONDecodeError, ValueError) as e:
        st.error(
            f"회원 데이터 파일을 읽지 못했습니다: {e}. "
            "기존 파일을 확인해 주세요."
        )
        return {}


def save_data(data):
    """임시 파일에 먼저 저장한 뒤 교체하여 파일 손상 위험 줄이기."""
    try:
        normalized = normalize_members(data)
        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

        temp_path = None

        try:
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                suffix=".tmp",
                dir=DATA_FILE.parent,
                delete=False
            ) as f:
                json.dump(
                    normalized,
                    f,
                    ensure_ascii=False,
                    indent=4
                )
                f.flush()
                os.fsync(f.fileno())
                temp_path = f.name

            os.replace(temp_path, DATA_FILE)
            return True

        finally:
            if temp_path and os.path.exists(temp_path):
                os.remove(temp_path)

    except (OSError, TypeError, ValueError) as e:
        st.error(f"저장에 실패했습니다: {e}")
        return False


members = load_data()

st.title("🥕 당근 모임 회원 관리")
st.caption("초보 운영자를 위한 직관적인 회원 관리 도구")

tab1, tab2, tab3, tab4 = st.tabs([
    "📋 회원 목록",
    "➕ 회원 등록",
    "⚙️ 참석 관리",
    "💾 데이터 백업/복원"
])


# ---------------------------
# TAB 1: 회원 목록
# ---------------------------
with tab1:
    st.subheader("전체 회원 현황")

    search_query = st.text_input(
        "🔍 아이디 또는 지역 검색",
        placeholder="검색어를 입력하세요..."
    )

    filtered_members = {
        uid: info for uid, info in members.items()
        if search_query.lower() in uid.lower()
        or search_query.lower() in info["지역"].lower()
    }

    col1, col2 = st.columns(2)
    col1.metric("전체 회원 수", f"{len(members)}명")
    col2.metric("검색 결과", f"{len(filtered_members)}명")

    if not members:
        st.info("등록된 회원이 없습니다. 회원 등록 탭을 이용해 주세요.")

    for uid, info in filtered_members.items():
        badge = (
            "✅ 참석"
            if info["월1회_참석여부"] == "참석"
            else "❌ 미참석"
        )

        with st.expander(f"👤 {uid} ({info['성별']}) | {badge}"):
            col1, col2 = st.columns(2)

            with col1:
                st.write(f"**📍 지역:** {info['지역']}")
                st.write(f"**✨ 외모:** {info['외모']}")

            with col2:
                st.write(f"**📅 참석:** {info['월1회_참석여부']}")
                st.write(f"**💖 성격:** {info['성격']}")

            st.write(f"**📝 활동 특징:** {info['활동특징']}")

            if st.button("🗑️ 회원 삭제", key=f"del_{uid}"):
                updated_members = members.copy()
                updated_members.pop(uid, None)

                if save_data(updated_members):
                    st.success(f"{uid} 회원이 삭제되었습니다.")
                    st.rerun()


# ---------------------------
# TAB 2: 회원 등록
# ---------------------------
with tab2:
    st.subheader("신규 회원 등록")

    with st.form("add_member_form", clear_on_submit=True):
        user_id = st.text_input(
            "아이디 (필수)",
            placeholder="예: 당근이123"
        ).strip()

        gender = st.radio("성별", ["F", "M"], horizontal=True)
        region = st.text_input(
            "지역",
            placeholder="예: 강남구 역삼동"
        )

        attendance = st.radio(
            "이번 달 참석 여부",
            ["참석", "미참석"],
            horizontal=True
        )

        feature = st.text_area(
            "활동 특징",
            placeholder="예: 주말 모임 선호, 친화력 좋음"
        )

        st.write("**평가 요소 (상/중/하)**")

        looks = st.select_slider(
            "외모",
            options=["하", "중", "상"],
            value="중"
        )

        personality = st.select_slider(
            "성격",
            options=["하", "중", "상"],
            value="중"
        )

        submitted = st.form_submit_button(
            "➕ 회원 저장하기",
            use_container_width=True
        )

        if submitted:
            if not user_id:
                st.error("아이디를 입력해 주세요.")

            elif user_id in members:
                st.error("이미 존재하는 아이디입니다.")

            else:
                updated_members = members.copy()
                updated_members[user_id] = {
                    "성별": gender,
                    "지역": region.strip(),
                    "월1회_참석여부": attendance,
                    "활동특징": feature.strip(),
                    "외모": looks,
                    "성격": personality
                }

                if save_data(updated_members):
                    st.success(f"🎉 {user_id} 회원이 저장되었습니다.")
                    st.rerun()


# ---------------------------
# TAB 3: 참석 관리
# ---------------------------
with tab3:
    st.subheader("이번 달 참석 체크")

    if not members:
        st.info("등록된 회원이 없습니다.")

    else:
        target_uid = st.selectbox(
            "회원 선택",
            list(members.keys())
        )

        current_status = members[target_uid]["월1회_참석여부"]

        st.write(f"현재 상태: **{current_status}**")

        new_status = st.radio(
            "참석 여부 변경",
            ["참석", "미참석"],
            index=["참석", "미참석"].index(current_status),
            key="update_status",
            horizontal=True
        )

        if st.button("상태 업데이트", use_container_width=True):
            updated_members = {
                uid: info.copy()
                for uid, info in members.items()
            }

            updated_members[target_uid]["월1회_참석여부"] = new_status

            if save_data(updated_members):
                st.success(
                    f"{target_uid} 회원의 상태가 "
                    f"'{new_status}'로 저장되었습니다."
                )
                st.rerun()


# ---------------------------
# TAB 4: 데이터 백업/복원
# ---------------------------
with tab4:
    st.subheader("회원 데이터 업로드")

    st.caption(
        "JSON 파일을 업로드하여 회원 정보를 불러오거나 "
        "기존 회원 데이터와 합칠 수 있습니다."
    )

    uploaded_file = st.file_uploader(
        "회원 데이터 JSON 파일 선택",
        type=["json"],
        key="member_json_upload"
    )

    import_mode = st.radio(
        "가져오기 방식",
        ["기존 회원과 병합", "전체 교체"],
        help=(
            "병합: 같은 아이디는 업로드 데이터로 갱신합니다. "
            "전체 교체: 현재 회원 목록을 업로드 데이터로 대체합니다."
        )
    )

    if uploaded_file is not None:
        if st.button("📥 업로드 데이터 저장", use_container_width=True):
            try:
                raw_data = json.loads(
                    uploaded_file.getvalue().decode("utf-8-sig")
                )
                imported_members = normalize_members(raw_data)

                if import_mode == "기존 회원과 병합":
                    updated_members = {
                        uid: info.copy()
                        for uid, info in members.items()
                    }
                    updated_members.update(imported_members)
                else:
                    updated_members = imported_members

                if save_data(updated_members):
                    st.success(
                        f"{len(imported_members)}명의 데이터를 "
                        "파일에 저장했습니다."
                    )
                    st.rerun()

            except (
                UnicodeDecodeError,
                json.JSONDecodeError,
                ValueError
            ) as e:
                st.error(f"업로드 파일을 처리할 수 없습니다: {e}")

    st.divider()

    st.subheader("회원 데이터 백업")

    if members:
        backup_json = json.dumps(
            members,
            ensure_ascii=False,
            indent=4
        )

        st.download_button(
            "⬇️ 전체 회원 데이터 다운로드",
            data=backup_json,
            file_name="club_members_backup.json",
            mime="application/json",
            use_container_width=True
        )
    else:
        st.info("백업할 회원 데이터가 없습니다.")
