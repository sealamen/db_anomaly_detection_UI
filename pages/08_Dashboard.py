import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
import requests
from streamlit_autorefresh import st_autorefresh



# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(page_title="📈 DB 모니터링 대시보드", layout="wide")

# 사이드바: 새로고침 주기
with st.sidebar:
    refresh_sec = st.slider("⏱ 새로고침 주기 (초)", 5, 60, 10)
    st_autorefresh(interval=refresh_sec * 1000, key="refresh")

# -----------------------------
# 1. 데이터 불러오기 + 세션 누적
# -----------------------------
response = requests.get("http://192.168.4.50:8000/metrics/getMetrics5m")
data_json = response.json()

# 세션 상태 초기화
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame()

# 단일 row / 여러 row 처리
if isinstance(data_json, list):
    new_df = pd.DataFrame(data_json)
else:
    new_df = pd.DataFrame([data_json])

print(new_df)

# 컬럼명 대문자, TIME datetime 변환
new_df.columns = [col.upper() for col in new_df.columns]
new_df["TIME"] = pd.to_datetime(new_df["TIME"])

# 기존 df에 누적
st.session_state.df = pd.concat([st.session_state.df, new_df], ignore_index=True)

# 최신 300행만 유지
df = st.session_state.df.sort_values("TIME").tail(300).reset_index(drop=True)

# 숫자형 컬럼 처리
numeric_cols = [
    "CPU_USAGE_PER_SEC",
    "DB_TIME_PER_SEC",
    "AVG_ACTIVE_SESSIONS"
]
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")  # 변환 실패 시 NaN

# -----------------------------
# 2. KPI 카드
# -----------------------------
st.title("📊 DB 성능 모니터링 대시보드")
st.subheader("🎯 KPI Check")

latest = df.iloc[-1]
prev = df.iloc[-2] if len(df) >= 2 else None


def kpi_card(label, value, prev_value=None, unit="", threshold=None, higher_is_bad=True):
    # 숫자 변환
    try:
        value = float(value)
    except (ValueError, TypeError):
        value = 0
    if prev_value is not None:
        try:
            prev_value = float(prev_value)
        except (ValueError, TypeError):
            prev_value = None

    # 변화율 계산
    change_str = ""
    if prev_value is not None:
        change_pct = ((value - prev_value) / prev_value) * 100 if prev_value != 0 else 0
        arrow = "▲" if change_pct > 0 else "▼"
        change_str = f"{arrow} {abs(change_pct):.1f}%"

    # 색상 결정
    color = "olivedrab"
    if threshold is not None:
        if higher_is_bad and value > threshold:
            color = "red"
        elif not higher_is_bad and value < threshold:
            color = "red"

    st.markdown(
        f"""
         <div style="padding:10px; border-radius:10px; background-color:#f0f2f6; text-align:center;">
             <h5 style="margin:0;">{label}</h5>
             <h3 style="margin:0; color:{color};">{value:.1f} {unit} {change_str}</h3>
         </div>
         """,
        unsafe_allow_html=True
    )


col1, col2, col3, col4 = st.columns(4)
with col1:
    kpi_card("CPU_USAGE_PER_SEC", latest["CPU_USAGE_PER_SEC"], prev["CPU_USAGE_PER_SEC"] if prev is not None else None,
             "%", threshold=75)
with col2:
    kpi_card("DB_TIME_PER_SEC", latest["DB_TIME_PER_SEC"], prev["DB_TIME_PER_SEC"] if prev is not None else None, "ms",
             threshold=800)
with col3:
    kpi_card("AVG_ACTIVE_SESSIONS", latest["AVG_ACTIVE_SESSIONS"],
             prev["AVG_ACTIVE_SESSIONS"] if prev is not None else None, "", threshold=80)
with col4:
    kpi_card("최근 이상 발생", df["ANOMALY_YN"].eq("Y").sum(), None, "")

st.write("\n")
st.write("\n")
st.write("\n")
# -----------------------------
# 3. 라인 차트
# -----------------------------
st.subheader("📈 주요 지표 추이 (이상치 포함)")

features = [
    "CPU_USAGE_PER_SEC",
    "DB_TIME_PER_SEC",
    "IO_MB_PER_SEC",
    "PHYSICAL_READS_PER_SEC",
    "PHYSICAL_WRITES_PER_SEC",
    "REDO_GENERATED_PER_SEC",
    "EXECUTIONS_PER_SEC",
    "DB_BLOCK_CHANGES_PER_SEC"
]

selected = st.multiselect("지표 선택", features, default=["CPU_USAGE_PER_SEC", "DB_TIME_PER_SEC"])

df_range = df.copy()

for metric in selected:
    fig, ax = plt.subplots(figsize=(10, 3))
    ax.plot(df_range["TIME"], df_range[metric], label=metric, color="lightslategray")

    # 이상치 점 찍기
    anomalies = df_range[df_range["ANOMALY_YN"] == "Y"]
    ax.scatter(anomalies["TIME"], anomalies[metric], color="firebrick", label="Anomaly", zorder=5)

    ax.set_title(metric)
    ax.set_xlabel("TIME")
    ax.legend()
    st.pyplot(fig)

st.write("\n")
st.write("\n")
st.write("\n")
# -----------------------------
# 4. 최근 이상 이벤트
# -----------------------------
st.subheader("⚠️ 최근 이상 이벤트")
recent_anomalies = df[df["ANOMALY_YN"] == "Y"].sort_values(by="TIME", ascending=False)
st.dataframe(recent_anomalies.tail(10).reset_index(drop=True))
