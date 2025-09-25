import streamlit as st
import pandas as pd

st.set_page_config(page_title="⚠️ 발생 이슈", layout="wide")

st.title("⚠️ 발생 이슈")
st.markdown("""
위의 모델을 통해 실제 실시간 탐지를 구현했으나, 이상치 탐지 X
- 현업 기반의 데이터 및 이상치를 생성하여 작업했다보니, 운영 DB 가 아닌 상태에서는 실시간 이상치 탐지가 안됨
- 아래 그래프처럼, 정상 범위를 벗어나지 못함
""")

col1, col2 = st.columns(2)  # 2개의 컬럼 생성

with col1:
    st.image("assets/CPU_USAGE_PER_SEC_detection.png",
             caption="이상치 탐지 결과(CPU_USAGE_PER_SEC)",
             use_container_width=True)

with col2:
    st.image("assets/DB_TIME_PER_SEC_detection.png",
             caption="이상치 탐지 결과(DB_TIME_PER_SEC)",
             use_container_width=True)


# --- 1. 데이터 테이블 ---
data = {
    "구분": ["학습 정상", "평가 이상치", "실제 부하"],
    "DB_TIME_PER_SEC": [1472, 2499, 2036],
    "CPU_USAGE_PER_SEC": [1.51, 0.52, 153],
    "LOGICAL_READS_PER_SEC": [395, 164, 894772],
    "ANOMALY_YN": ["N", "Y", "N"],
    "평가 결과": ["정상", "이상치 탐지 성공", "이상치 탐지 실패"]
}

df = pd.DataFrame(data)

st.markdown("### '실제 부하' 이상치 탐지 실패 이유")
st.markdown("""
- DB_TIME 컬럼의 학습용 정상 데이터, 모델 평가 시 사용된 이상치 데이터, DB 부하를 통한 조회 데이터의 MAX 값 비교 
""")
st.table(df)

# --- 2. 이상치 탐지 실패 이유 ---
st.markdown("""
1. **학습 데이터 범위 제한**
- CPU, LOGICAL_READS, DB_TIME 등 정상 범위가 너무 낮아 모델이 극단치를 경험하지 못함.
- 실제 개발 현장이 아니다보니, 논문에서 정상으로 표시하는 정도에 차이가 있음 

2. **모델 구조 특성**
- One-Class SVM, Isolation Forest, Autoencoder 모두 학습 데이터 분포 기반 탐지.
- 학습 범위를 벗어난 실제 부하 데이터는 정상으로 판단될 수 있음.

3. **스케일링 및 전처리 문제**
- 일부 컬럼 누락 시 0으로 채워 입력이 왜곡됨.
- 실제 부하 데이터는 학습 데이터 대비 값이 매우 커서 스케일링 후 MSE나 SVM 판단에 영향을 줌.

> 💡 핵심: 학습 데이터의 정상 범위를 실제 부하 수준까지 확장해야 모델이 이상치를 정확히 탐지할 수 있음.
""")