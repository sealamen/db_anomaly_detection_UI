import streamlit as st

st.set_page_config(page_title="프로젝트 개요", layout="wide")

st.title("📖 프로젝트 개요")

st.markdown("\n")
st.markdown("\n")

# --- 탭 생성 ---
tab1, tab2, tab3, tab4 = st.tabs(["Intro 1", "Intro 2", "Intro 3", "Intro 4"])

with tab1:

    # 1. 기존 프로젝트와의 차이점
    st.markdown("#### 기존 이상탐지 프로젝트와의 차이점")
    st.markdown("""
    일반적인 DB 이상탐지 프로젝트 보다 **DB 성능에 중점**을 두는 이상 탐지 프로젝트
    """)

    st.markdown("""
    ##### 🟢 기존 DB 이상탐지 프로젝트
    - 내용 : 정상적인 트랜잭션과 다른 행동을 탐지  
    - 상세 : 거래금액, 거래횟수, 거래위치, 쿼리유형 등을 통해 사용자의 행동/거래 패턴이 이상한지를 탐구
    - 예시
      - 동일 계정이 1분 동안 100번 로그인 시도
      - 특정 계정이 평소 거래 금액보다 훨씬 큰 금액 이체
      - 쿼리 패턴이 갑자기 달라짐 (SELECT만 하던 계정이 DELETE 쿼리 실행)
    """)


    st.markdown("""
    ##### 🔵 머신러닝 기반 운영 DB 성능 이상탐지
    - 내용 : DB 자체가 비정상적으로 느려지거나 부하 발생 여부 확인  
    - 상세 : 운영 DB 에서 발생하는 성능 지표를 수집하고, 정상 패턴과 다른 이상 패턴을 ML/DL로 탐지 
    - 예시
      - 쿼리 실행 시간이 갑자기 폭등
      - Lock wait 급증 → 응답 정지
      - 초당 트랜잭션(TPS)이 비정상적 증가
    """)


    st.markdown("\n")
    st.markdown("\n")

with tab2:

    # 2. 머신러닝을 사용하는 이유
    st.markdown("#### 이상탐지에 머신러닝을 사용하는 이유")
    st.markdown("""
    **Threshold 기반 탐지**
    - 단순 규칙: CPU 사용률 90% 이상이면 이상, 세션 수 1000 이상이면 이상
    - 구현이 간단하지만, 패턴이 변하거나 새로운 이상이 나타나면 탐지 어려움
    
    **머신러닝 기반 탐지**
    - 복합 패턴 이상(예: CPU 70%, I/O 50ms, 쿼리 300건 동시 발생) 탐지 가능
    - 새로운 유형의 문제(예: 특정 쿼리 조합으로 인한 성능 저하) 탐지 가능
    """)

    st.markdown("\n")
    st.markdown("\n")

with tab3:

    # 3. 기존 오라클 기능과의 차이
    st.markdown("#### 기존 오라클 기능과의 차이점")
    st.markdown("""
    - Oracle Autonomous DB, OML4SQL, OCI Anomaly Detection 등은 **내부 데이터 기반 ML** 지원
    - 하지만 **비용 문제** 때문에 많은 기업에서 사용하지 않음
    - 본 프로젝트는 **alert.log + V$뷰 + 사용자 정의 조건**을 종합해 **더 풍부한 이상 정의** 가능  
        """)

    st.markdown("\n")
    st.markdown("\n")

with tab4:

    # 4. 프로젝트 목표
    st.markdown("#### 프로젝트 목표")
    st.markdown("""
    - Oracle 운영 DB에서 발생하는 **성능 메트릭** (V$ 뷰, AWR/ASH, alert.log 등)을 주기적으로 수집하고, 정상 패턴을 학습하여 근실시간으로 성능 이상 탐지
    """)