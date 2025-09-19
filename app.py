import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
from data_generator import generate_sample_data
from streamlit_autorefresh import st_autorefresh


# 페이지 설정
st.set_page_config(page_title="DB 모니터링 대시보드", layout="wide")

# 사이드바: 새로고침 주기
with st.sidebar:
    refresh_sec = st.slider("⏱ 새로고침 주기 (초)", 5, 60, 10)
    st_autorefresh = st_autorefresh(interval=refresh_sec * 1000, key="refresh")

# 2. 데이터 불러오기
df = generate_sample_data(200)

print(df)

# 마지막 및 이전 시점 데이터
latest = df.iloc[-1]
prev = df.iloc[-2]


# DASHBOARD 1. KPI 카드 (임계치 색상 + 변화율)
st.title("📊 DB 성능 모니터링 대시보드")
st.write("\n")
st.subheader(" 🎯 KPI Check ")

def kpi_card(label, value, prev_value=None, unit="", threshold=None, higher_is_bad=True):
    # 변화율 계산
    change_str = ""
    if prev_value is not None:
        change_pct = ((value - prev_value) / prev_value) * 100 if prev_value != 0 else 0
        arrow = "▲" if change_pct > 0 else "▼"
        change_str = f"{arrow} {abs(change_pct):.1f}%"

    # 색상 결정
    color = "green"
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
    kpi_card("CPU_TIME_MS", latest["CPU_TIME_MS"], prev["CPU_TIME_MS"], "ms", threshold=8000, higher_is_bad=True)
with col2:
    kpi_card("USER_IO_WAIT_MS", latest["USER_IO_WAIT_MS"], prev["USER_IO_WAIT_MS"], "ms", threshold=50, higher_is_bad=True)
with col3:
    kpi_card("TXN_PER_SEC", latest["TXN_PER_SEC"], prev["TXN_PER_SEC"], "", threshold=400, higher_is_bad=True)
with col4:
    kpi_card("HARD_PARSE_RATIO_PCT", latest["HARD_PARSE_RATIO_PCT"], prev["HARD_PARSE_RATIO_PCT"], "%", threshold=20, higher_is_bad=True)

st.write("\n")
st.write("\n")
st.write("\n")

# DASHBOARD 2: 라인 차트 + 이상치 표시 + 범위 슬라이더
st.subheader("📈 주요 지표 추이 (이상치 포함)")

features = ["CPU_TIME_MS", "USER_IO_WAIT_MS", "TXN_PER_SEC", "EXECUTIONS_PER_SEC"]
selected = st.multiselect("지표 선택", features, default=["CPU_TIME_MS", "TXN_PER_SEC"])

time_min = df["TIME"].min().to_pydatetime()
time_max = df["TIME"].max().to_pydatetime()

start_time = time_min
end_time = time_max

df_range = df[(df["TIME"] >= start_time) & (df["TIME"] <= end_time)]

for metric in selected:
    fig, ax = plt.subplots(figsize=(8, 3))
    ax.plot(df_range["TIME"], df_range[metric], label=metric, color="blue")

    # 이상치 점 찍기
    anomalies = df_range[df_range["ANOMALY_YN"] == 1]
    ax.scatter(anomalies["TIME"], anomalies[metric], color="red", label="Anomaly", zorder=5)

    ax.set_title(metric)
    ax.legend()
    st.pyplot(fig)

st.write("\n")
st.write("\n")
st.write("\n")

# DASHBOARD 3 : 상관관계 히트맵 (대표 지표만)
st.subheader("📌 메트릭 상관관계")
corr_features = ["CPU_TIME_MS", "USER_IO_WAIT_MS", "TXN_PER_SEC", "EXECUTIONS_PER_SEC",
                 "HARD_PARSE_RATIO_PCT", "BUFFER_CACHE_HIT_RATIO", "LOGONS_PER_SEC"]
corr = df[corr_features].corr()

fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
st.pyplot(fig)

st.write("\n")
st.write("\n")
st.write("\n")

# DASHBOARD 4 : 세션 현황 (ACTIVE / INACTIVE / BLOCKED)
st.subheader("👥 세션 관련 지표")
# 임시 세션 상태 생성 (샘플)
df["SESSIONS_ACTIVE_COUNT"] = df["ACTIVE_SESSIONS"]
df["SESSIONS_INACTIVE_COUNT"] = np.random.randint(0, 20, len(df))
df["SESSIONS_BLOCKED_COUNT"] = np.random.randint(0, 5, len(df))

col1, col2, col3 = st.columns(3)
col1.bar_chart(df.set_index("TIME")[["SESSIONS_ACTIVE_COUNT"]])
col2.bar_chart(df.set_index("TIME")[["SESSIONS_INACTIVE_COUNT"]])
col3.bar_chart(df.set_index("TIME")[["SESSIONS_BLOCKED_COUNT"]])