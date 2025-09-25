import streamlit as st
import pandas as pd

st.title("데이터")

# 1. 학습 및 평가 대상 데이터
st.header("1️⃣ 학습 및 평가 대상 데이터")
st.table(pd.DataFrame({
    "컬럼명": ["CPU_USAGE_PER_SEC", "DB_TIME_PER_SEC", "AVG_ACTIVE_SESSIONS"],
    "설명": ["CPU 사용률", "DB 처리 시간(ms)", "평균 활성 세션 수"]
}))
st.markdown("""
- 컬럼 선정 기준 및 컬럼 목록은 [Wiki 링크](https://www.notion.so/2767eb9760b78087aad3fa302fce20ae?pvs=21) 참고
- 주요 데이터 예시:
    - CPU 사용률 (CPU_USAGE_PER_SEC)
    - DB Time (DB_TIME_PER_SEC)
    - Active Sessions (AVG_ACTIVE_SESSIONS)
    - I/O 관련 지표 (IO_MB_PER_SEC, PHYSICAL_READS_PER_SEC 등)
    - Redo, Execution, Block Changes 등
""")

# 2. 데이터 생성 및 학습 방법
st.header("2️⃣ 데이터 생성 및 학습 방법")
st.markdown("""
- 방법 1: 실제 DB 환경에서 운영 DB처럼 데이터를 주기적으로 수집  
  (운영 DB의 성능 데이터를 그대로 학습하면 현실성 높음)
- 방법 2: 학습용 데이터를 직접 생성  
  - CPU, Buffer Gets 등 주요 지표를 기반으로 시뮬레이션
  - 운영환경 데이터는 보안상 사용 불가 → 시뮬레이션 데이터 사용
- 선택: 방법 2
  - 실제 운영 데이터 대신 유사 시뮬레이션 데이터를 학습
  - 주기적 수집, 이상치 포함 등 실제 운영 환경과 비슷하게 구성
""")

st.markdown("자세한 내용은 [Github 링크](https://github.com/sealamen/db_anomaly_detection_tools/issues/3) 참고")
