import streamlit as st
import pandas as pd


st.title("개발환경")


# Library
st.markdown("### 🛠 Libraries")
st.markdown("""
- 이 프로젝트에서는 아래와 같은 개발환경 사용
- conda 가상환경을 통해 패키지 관리
""")

env_data = [
    ("Pandas, Numpy", "데이터 처리 및 전처리, 시계열 데이터 처리, 결측치 처리"),
    ("Matplotlib, Seaborn", "데이터 시각화, 시계열 패턴/이상치 시각화"),
    ("Scikit-learn", "머신러닝 기반 이상탐지 모델 (One-Class SVM, Isolation Forest)"),
    ("TensorFlow", "딥러닝 기반 이상탐지 모델 (AutoEncoder)"),
    ("Streamlit", "대시보드 및 UI 개발, 페이지 구성, 실시간 그래프 표시"),
    ("FastAPI", "모델 API 서버, 비동기 요청 처리"),
    ("oracledb", "Oracle DB 연결, 성능 로그 수집"),
    ("asyncio", "비동기 데이터 수집/모니터링 루프"),
    ("joblib", "학습 모델 저장/불러오기"),
]

# DataFrame 변환
df_env = pd.DataFrame(env_data, columns=["라이브러리", "설명"])

# Streamlit 테이블로 표시
df_env.index = df_env.index + 1
st.dataframe(df_env)

st.markdown("\n\n")

# Database
st.markdown("### 🗄 Database")
st.markdown("""
- **Oracle 11g**
    - 어떤 Oracle DB 에도 이식이 가능해야하는 서비스이므로, 낮은 버전의 11g 로 개발 진행 
    - 유저, 테이블, 뷰 생성 쿼리 : [Github Issue #3](https://github.com/sealamen/db_anomaly_detection/issues/3)
""")


# Language
st.markdown("### 💻 Language")
st.markdown("""
- **Python 3.11**
    - Tensorflow 가 가장 안정적으로 돌아갈 수 있는 Python version
    - 로컬에서 Tensorflow 를 돌리기 위해 Anaconda 가상환경 사용
""")


# IDE
st.markdown("### 🖊 IDE")
st.markdown("""
- **Pycharm**
    - Github 를 용이하게 쓰기 위해 사용 
""")


# Github
st.markdown("### 🌐 형상관리도구")
st.markdown("""
- **Github**
    - 용이한 협업을 위해 현업에서 하는 레포지토리 관리 방식 차용 
    - 개발 이슈 및 내용 기록 -> 추후 관련 주제로 최종 프로젝트 진행 시, 레퍼런스 자료로 사용 
""")