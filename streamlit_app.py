import os, re
import requests
import streamlit as st
import pandas as pd

API_BASE = os.getenv("JOB_API_BASE", "http://localhost:8000")  # point to FastAPI

st.set_page_config(page_title="채용공고 추적기", layout="wide")
st.title("🚀 채용공고 추적기 (RocketPunch 기반)")

# --- Session State
if "df" not in st.session_state:
    st.session_state.df = None
if "email_result" not in st.session_state:
    st.session_state.email_result = None

# --- Inputs
keyword = st.text_input("🔍 검색 키워드", placeholder="예: 백엔드, 데이터, AI 등")
seniority_map = {"신입":"BEGINNER","주니어":"JUNIOR","미들":"MID","시니어":"SENIOR","C레벨":"C_LEVEL"}
selected_seniority_kor = st.selectbox("🧑‍💼 숙련도", list(seniority_map.keys()))
selected_seniority_eng = seniority_map[selected_seniority_kor]

def is_valid_gmail(email: str) -> bool:
    return re.fullmatch(r"[a-zA-Z0-9_.+-]+@gmail\.com", email or "") is not None

def fetch_jobs(keyword, seniority):
    params = {"seniority": seniority}
    if keyword:
        params["keyword"] = keyword
    r = requests.get(f"{API_BASE}/jobs/", params=params, timeout=60)
    r.raise_for_status()
    return r.json()

def send_email_via_api(to_email: str, keyword, seniority):
    payload = {"to_email": to_email, "keyword": keyword or None, "seniority": seniority}
    r = requests.post(f"{API_BASE}/email/send", json=payload, timeout=120)
    r.raise_for_status()
    return r.json()

# --- Search
if st.button("공고 검색 시작"):
    st.info("🔄 공고를 불러오는 중입니다...")
    try:
        with st.spinner("API 호출 중..."):
            jobs = fetch_jobs(keyword if keyword else None, selected_seniority_eng)
            st.session_state.df = pd.DataFrame(jobs)
            st.session_state.email_result = None
    except requests.RequestException as e:
        st.error(f"API 오류: {e}")
        st.session_state.df = pd.DataFrame()

# --- Results & Email
if st.session_state.df is not None:
    df = st.session_state.df
    if df.empty:
        st.warning("❌ 공고를 찾을 수 없습니다.")
    else:
        st.success(f"✅ 총 {len(df)}건의 공고를 찾았습니다.")
        st.dataframe(df, use_container_width=True)

        csv_data = df.to_csv(index=False, encoding="utf-8-sig")
        st.download_button("📥 CSV 다운로드", data=csv_data, file_name="rocket_jobs.csv", mime="text/csv")

        with st.form("email_form"):
            email = st.text_input("📧 Gmail 주소를 입력하세요 (예: you@gmail.com)")
            submitted = st.form_submit_button("이메일 전송")
            if submitted:
                if not is_valid_gmail(email):
                    st.warning("⚠️ 유효한 Gmail 주소(@gmail.com)만 입력할 수 있습니다.")
                else:
                    try:
                        with st.spinner("이메일 전송 중..."):
                            _ = send_email_via_api(email, keyword, selected_seniority_eng)
                        st.session_state.email_result = "성공"
                        st.session_state.email_target = email
                    except requests.HTTPError as e:
                        # Show backend error message if present
                        try:
                            detail = e.response.json().get("detail")
                        except Exception:
                            detail = str(e)
                        st.session_state.email_result = f"실패: {detail}"
                        st.session_state.email_target = email
                    finally:
                        st.rerun()

# --- Toast
if st.session_state.email_result:
    target = st.session_state.get("email_target", "")
    if st.session_state.email_result == "성공":
        st.success(f"✅ {target} 으로 이메일을 전송했습니다.")
    else:
        st.error(f"❌ 이메일 전송 {st.session_state.email_result}")
    st.session_state.email_result = None
    st.session_state.email_target = None