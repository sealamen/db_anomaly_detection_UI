import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import datetime
import requests
from streamlit_autorefresh import st_autorefresh

# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(page_title="Oracle DB 성능 모니터링", layout="wide", initial_sidebar_state="collapsed")

# 다크 테마 CSS
st.markdown("""
<style>
    .main {
        background-color: #1e2936;
    }
    .stApp {
        background-color: #1e2936;
    }
    h1, h2, h3, h4, h5, h6, p, span, div, label {
        color: #e0e6ed !important;
    }
    .kpi-card {
        background-color: #2d3e50;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        border: 1px solid #3d5266;
    }
    .kpi-label {
        color: #8b98a9;
        font-size: 14px;
        margin-bottom: 10px;
    }
    .kpi-value {
        font-size: 36px;
        font-weight: bold;
        margin: 0;
    }
    .kpi-cyan { color: #00d9ff; }
    .kpi-orange { color: #ff9500; }
    .alert-table {
        background-color: #2d3e50;
        border-radius: 10px;
        padding: 20px;
        border: 1px solid #8b3a3a;
    }
    .chart-container {
        background-color: #2d3e50;
        border-radius: 10px;
        padding: 20px;
        border: 1px solid #3d5266;
    }
    /* Selectbox 스타일 */
    .stSelectbox > div > div {
        background-color: #2d3e50 !important;
        color: #e0e6ed !important;
        border: 1px solid #3d5266 !important;
    }
    .stSelectbox label {
        color: #8b98a9 !important;
    }
    /* Selectbox 드롭다운 */
    [data-baseweb="select"] > div {
        background-color: #2d3e50 !important;
        border-color: #3d5266 !important;
    }
    [data-baseweb="select"] span {
        color: #e0e6ed !important;
    }
    /* 드롭다운 메뉴 */
    [role="listbox"] {
        background-color: #2d3e50 !important;
    }
    [role="option"] {
        background-color: #2d3e50 !important;
        color: #e0e6ed !important;
    }
    [role="option"]:hover {
        background-color: #3d5266 !important;
    }
    /* Input 필드 */
    input {
        background-color: #2d3e50 !important;
        color: #e0e6ed !important;
        border: 1px solid #3d5266 !important;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# 1. 데이터 불러오기 + 세션 누적
# -----------------------------
# 자동 새로고침 (10초)
st_autorefresh(interval=10000, key="refresh")

response = requests.get("http://192.168.4.49:8000/metrics/getMetrics5m")
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
# 2. 타이틀 및 시각
# -----------------------------
col_title, col_time = st.columns([3, 1])
with col_title:
    st.markdown("<h1 style='color: #00d9ff; margin-bottom: 30px;'>Oracle DB 성능 모니터링</h1>", unsafe_allow_html=True)
with col_time:
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.markdown(f"<p style='text-align: right; color: #8b98a9; font-size: 14px; margin-top: 20px;'>{current_time}</p>", unsafe_allow_html=True)

# -----------------------------
# 3. KPI 카드
# -----------------------------
latest = df.iloc[-1]

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">CPU_USAGE_PER_SEC</div>
        <div class="kpi-value kpi-cyan">{float(latest["CPU_USAGE_PER_SEC"]):.1f}%</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">DB_TIME_PER_SEC</div>
        <div class="kpi-value kpi-cyan">{float(latest["DB_TIME_PER_SEC"]):.1f}ms</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">AVG_ACTIVE_SESSIONS</div>
        <div class="kpi-value kpi-cyan">{int(float(latest["AVG_ACTIVE_SESSIONS"]))}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    last_anomaly = df[df["ANOMALY_YN"] == "Y"].sort_values(by="TIME", ascending=False)
    last_anomaly_time = last_anomaly.iloc[0]["TIME"].strftime("%H:%M:%S") if len(last_anomaly) > 0 else "-"
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">최근 이상 발생</div>
        <div class="kpi-value kpi-orange">{last_anomaly_time}</div>
    </div>
    """, unsafe_allow_html=True)

st.write("\n")

# -----------------------------
# 4. 선택 지표 추이 차트
# -----------------------------
st.markdown("<div class='chart-container'>", unsafe_allow_html=True)

col_chart_title, col_chart_filter = st.columns([3, 1])
with col_chart_title:
    st.markdown("<h3>선택 지표 추이</h3>", unsafe_allow_html=True)
with col_chart_filter:
    # 시간 범위 필터는 현재 표시만
    st.markdown("<p style='text-align: right; color: #8b98a9;'>시간 범위: 최근 데이터</p>", unsafe_allow_html=True)

# 선택 지표 (기본값: CPU_USAGE_PER_SEC)
features = [
    "CPU_USAGE_PER_SEC",
    "DB_TIME_PER_SEC",
    "AVG_ACTIVE_SESSIONS",
    "IO_MB_PER_SEC",
    "PHYSICAL_READS_PER_SEC",
    "PHYSICAL_WRITES_PER_SEC"
]

selected_metric = st.selectbox("지표 선택", features, index=0, label_visibility="collapsed")

# Plotly 차트 생성
fig = go.Figure()

# 정상 데이터
normal_data = df[df["ANOMALY_YN"] == "N"]
fig.add_trace(go.Scatter(
    x=normal_data["TIME"],
    y=normal_data[selected_metric],
    mode='lines',
    name='정상',
    line=dict(color='#00d9ff', width=2),
    showlegend=True
))

# 이상 데이터 - 크고 눈에 띄는 마커
anomaly_data = df[df["ANOMALY_YN"] == "Y"]
if len(anomaly_data) > 0:
    fig.add_trace(go.Scatter(
        x=anomaly_data["TIME"],
        y=anomaly_data[selected_metric],
        mode='markers',
        name='⚠️ 이상치 감지',
        marker=dict(
            color='#ff4444',
            size=16,
            symbol='circle',
            line=dict(color='#ffffff', width=2)
        ),
        showlegend=True
    ))
    
    # 80% 참고선
    max_val = df[selected_metric].max()
    threshold_val = max_val * 0.8
    
    fig.add_hline(
        y=threshold_val, 
        line_dash="dash", 
        line_color="#ffa500", 
        line_width=2,
        opacity=0.7
    )
    
    # 참고선 텍스트 어노테이션
    fig.add_annotation(
        x=df["TIME"].max(),
        y=threshold_val,
        text="📊 80% 참고선",
        showarrow=False,
        xanchor="right",
        yanchor="bottom",
        font=dict(size=13, color="#ffa500", family="Arial Black"),
        bgcolor="rgba(45, 62, 80, 0.9)",
        bordercolor="#ffa500",
        borderwidth=2,
        borderpad=6
    )
    
    # 상위 구간 강조 (80% 이상 영역)
    fig.add_hrect(
        y0=threshold_val, 
        y1=df[selected_metric].max() * 1.1,
        fillcolor="#ffa500", 
        opacity=0.08,
        line_width=0
    )
    
    # 상위 구간 텍스트
    fig.add_annotation(
        x=df["TIME"].min() + (df["TIME"].max() - df["TIME"].min()) * 0.95,
        y=df[selected_metric].max() * 1.05,
        text="상위 20% 구간",
        showarrow=False,
        font=dict(size=12, color="#ffcc66"),
        bgcolor="rgba(255, 165, 0, 0.2)",
        borderpad=4
    )

# 차트 레이아웃
fig.update_layout(
    plot_bgcolor='#1e2936',
    paper_bgcolor='#2d3e50',
    font=dict(color='#e0e6ed'),
    xaxis=dict(
        gridcolor='#3d5266',
        showgrid=True,
        title="시간",
        title_font=dict(size=14, color='#8b98a9'),
        range=[df["TIME"].min(), df["TIME"].max()]
    ),
    yaxis=dict(
        gridcolor='#3d5266',
        showgrid=True,
        title=selected_metric,
        title_font=dict(size=14, color='#8b98a9'),
        range=[0, df[selected_metric].max() * 1.1]
    ),
    height=400,
    margin=dict(l=50, r=50, t=30, b=50),
    showlegend=True,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1,
        bgcolor="rgba(45, 62, 80, 0.8)",
        bordercolor="#3d5266",
        borderwidth=1,
        font=dict(size=12, color="#e0e6ed")
    ),
    hovermode='x unified'
)

st.plotly_chart(fig, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

st.write("\n")

# -----------------------------
# 5. 최근 이상 이벤트 표
# -----------------------------
st.markdown("<div class='alert-table'>", unsafe_allow_html=True)

col_alert_title, col_alert_count = st.columns([3, 1])
with col_alert_title:
    st.markdown("<h3>⚠️ 최근 이상 이벤트 표</h3>", unsafe_allow_html=True)
with col_alert_count:
    recent_count = len(df[df["ANOMALY_YN"] == "Y"].tail(10))
    st.markdown(f"<p style='text-align: right; color: #8b98a9;'>최근 {recent_count}건</p>", unsafe_allow_html=True)

recent_anomalies = df[df["ANOMALY_YN"] == "Y"].sort_values(by="TIME", ascending=False).head(10)

if len(recent_anomalies) > 0:
    # 표시용 데이터 가공
    display_data = []
    for idx, row in recent_anomalies.iterrows():
        # 가장 높은 값을 가진 지표 찾기
        metrics = ["CPU_USAGE_PER_SEC", "DB_TIME_PER_SEC", "AVG_ACTIVE_SESSIONS"]
        max_metric = max(metrics, key=lambda m: float(row[m]) if pd.notna(row[m]) else 0)
        
        # 심각도 결정
        max_val = float(row[max_metric])
        if max_val > 90:
            severity = "🔴 심각"
        elif max_val > 75:
            severity = "🟠 중위"
        else:
            severity = "🟡 경고"
        
        # 처리 상태 (무작위로 설정)
        import random
        status = random.choice(["🔄 처리 중", "✅ 완료"])
        
        display_data.append({
            "발생 시각": row["TIME"].strftime("%H:%M:%S"),
            "지표": max_metric,
            "값": f"{max_val:.1f}" + ("ms" if "TIME" in max_metric else ""),
            "심각도": severity,
            "처리 상태": status
        })
    
    # DataFrame으로 변환하여 표시
    display_df = pd.DataFrame(display_data)
    
    # Streamlit 스타일로 표시
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "발생 시각": st.column_config.TextColumn("발생 시각", width="small"),
            "지표": st.column_config.TextColumn("지표", width="medium"),
            "값": st.column_config.TextColumn("값", width="small"),
            "심각도": st.column_config.TextColumn("심각도", width="small"),
            "처리 상태": st.column_config.TextColumn("처리 상태", width="small")
        }
    )
else:
    st.info("최근 이상 이벤트가 없습니다.")

st.markdown("</div>", unsafe_allow_html=True)
