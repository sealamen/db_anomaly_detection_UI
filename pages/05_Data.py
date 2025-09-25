import streamlit as st
import pandas as pd

st.set_page_config(page_title="DB 성능 지표 정리", layout="wide")

st.title("📊 데이터 ")
st.markdown("\n")
st.markdown("\n")

# --- 탭 생성 ---
tab1, tab2 = st.tabs(["1. 평가 데이터 목록", "2. 데이터 생성"])

# -------------------
# 탭 1 : 평가 데이터 목록
# -------------------
with tab1:
    st.markdown("\n")
    st.markdown("""
    ### 1. 평가 데이터 목록
    
    - **AS-IS** : 샘플 테스트 당시, **GEN AI** 를 통해 33개의 컬럼을 뽑아서 학습 및 평가 진행
    - **TO-BE** : 수천 개의 메트릭 중, 실제로 **Oracle DB의 `V$SYSMETRIC` 뷰에서 논문과 현업 및 공식 문서에서 공통적으로 중요하다고 언급된 핵심 지표 19개 분류**
    """)

    # --- 상세 지표 테이블 ---

    data = [
        [1, "DB_TIME_PER_SEC", "DB가 요청 처리에 소요한 총 시간 (CPU+I/O+Wait)", "DB 전체 성능 종합 지표", "Oracle AWR, Cornejo, tesi"],
        [2, "CPU_USAGE_PER_SEC", "DB 차원의 CPU 사용률", "임계치 초과시 anomaly", "AWR/V$SYSMETRIC, Cornejo"],
        [3, "HOST_CPU_USAGE_PER_SEC", "OS 전체의 CPU 사용률", "DB vs OS 문제 구분", "AWR Host CPU Utilization"],
        [4, "PHYSICAL_READS_PER_SEC", "디스크 물리적 읽기", "I/O 성능 병목", "V$SYSMETRIC, 논문"],
        [5, "PHYSICAL_WRITES_PER_SEC", "디스크 물리적 쓰기", "Undo/Redo 병목", "AWR I/O metrics, tesi.pdf"],
        [6, "IO_MB_PER_SEC", "초당 I/O 전송량", "I/O throughput", "Oracle 성능 가이드, Cornejo"],
        [7, "REDO_GENERATED_PER_SEC", "REDO 생성량", "트랜잭션 양 지표", "AWR, 논문"],
        [8, "DB_BLOCK_CHANGES_PER_SEC", "DB 블록 변경 수", "TXN 충돌 예측", "V$SYSMETRIC, 논문"],
        [9, "CONSISTENT_READ_GETS_PER_SEC", "캐시 일관성 읽기", "Read contention 가능", "V$SYSSTAT, 논문"],
        [10, "LOGICAL_READS_PER_SEC", "논리적 블록 읽기", "SQL 효율성 평가", "V$SYSSTAT, Cornejo"],
        [11, "DBWR_CHECKPOINTS_PER_SEC", "Checkpoint 횟수", "디스크 병목 탐지", "V$SYSSTAT, 논문"],
        [12, "EXECUTIONS_PER_SEC", "SQL 실행 횟수", "Workload 반영", "V$SQLAREA, 논문"],
        [13, "HARD_PARSE_COUNT_PER_SEC", "Hard Parse 횟수", "Library Cache 효율성", "V$SYSSTAT, Cornejo"],
        [14, "AVG_ACTIVE_SESSIONS (AAS)", "평균 활성 세션", "동시부하 대표 지표", "Oracle, Cornejo, 논문"],
        [15, "LOGONS_PER_SEC", "세션 로그인 수", "연결 관리 탐지", "V$SYSSTAT, Cornejo"],
        [16, "USER_CALLS_PER_SEC", "App→DB 호출 수", "루프 쿼리 탐지", "V$SYSSTAT, 논문"],
        [17, "USER_COMMITS_PER_SEC", "Commit 횟수", "트랜잭션 패턴 분석", "V$SYSSTAT, 논문"],
        [18, "USER_ROLLBACKS_PER_SEC", "Rollback 횟수", "Deadlock 탐지", "V$SYSSTAT, 논문"],
        [19, "ENQUEUE_WAITS_PER_SEC", "Enqueue Lock 대기", "동시성/Deadlock 원인", "V$SYSTEM_EVENT, Cornejo"],
    ]

    df = pd.DataFrame(data, columns=["번호", "지표", "설명", "중요성", "선정 근거"])
    st.dataframe(df.set_index("번호"), use_container_width=True)


    st.markdown("\n")
    st.markdown("\n")

    st.markdown("""
    ##### 참조 문서
    - Database Performance Analytics Using Anomaly Detection (Roger Cornejo, 2022) (Oracle Engineer)
        - Feature Selection 전략 : 서로 중복성을 가지는 지표는 제외 → 모델의 과적합을 피하고, 엔지니어가 직관적으로 해석할 수 있도록 작업
        - Cornejo(2022)가 제안한 Feature Selection 방식을 참고하여 기존 33개의 컬럼을 축소 ( ex : AVG_ACTIVE_SESSIONS, SESSIONS_TOTAL 컬럼 통합)
    - Unsupervised Anomaly Detection on Multivariate Time Series in an Oracle Database (Davide Di Mauro, 2022-2023)
        - 동료 DB 엔지니어들의 경험을 바탕으로 19개의 지표를 선택
    - Oracle 공식 문서 :
        - [Oracle 문서 : AWR 리포트 UI 및 AWR 리포트 생성](https://docs.oracle.com/en-us/iaas/performance-hub/doc/awr-report-ui.html?utm_source=chatgpt.com) : AWR 리포트가 어떤 metric을 포함하는지, 어떻게 보여주는지 설명된 문서
        - [Oracle Database 23 문서](https://docs.oracle.com/en/database/oracle/oracle-database/23/arpls/DBMS_WORKLOAD_REPOSITORY.html?utm_source=chatgpt.com) : AWR 관련 metric이 어떻게 구조화되는지 기술
    """)

    st.markdown("\n")
    st.markdown("\n")

    st.markdown("""
    ##### 데이터 분류
    - **① DB 전반 상태**
        - DB_TIME_PER_SEC, AVG_ACTIVE_SESSIONS (AAS)
    - **② CPU, I/O, Memory**
        - CPU_USAGE_PER_SEC, HOST_CPU_USAGE_PER_SEC, PHYSICAL_READS_PER_SEC, PHYSICAL_WRITES_PER_SEC, IO_MB_PER_SEC, DBWR_CHECKPOINTS_PER_SEC
    - **③ SQL 효율성과 트랜잭션**
        - LOGICAL_READS_PER_SEC, CONSISTENT_READ_GETS_PER_SEC, EXECUTIONS_PER_SEC, HARD_PARSE_COUNT_PER_SEC, REDO_GENERATED_PER_SEC, USER_COMMITS_PER_SEC
    - **④ 동시성·락·롤백**
        - ENQUEUE_WAITS_PER_SEC, USER_ROLLBACKS_PER_SEC, LOGONS_PER_SEC, USER_CALLS_PER_SEC, DB_BLOCK_CHANGES_PER_SEC
    """)


with tab2:
    st.markdown("\n")
    st.markdown("### 2. 데이터 생성")

    st.markdown("\n")
    st.markdown("""
    ##### 데이터 확보 한계 
    - 운영 데이터는 보안 문제로 사용 불가  
        - 방법 1 : 학습할 데이터 직접 생성  
        - 방법 2 : 실제 DB에 부하 발생시켜 수집  
    - 본 프로젝트에서는 모델 학습/평가 시스템 구축이 목적이므로 **방법 1 (데이터 직접 생성)** 채택
    """)
    st.markdown("\n")
    st.markdown("\n")
    st.markdown("""
    ##### 학습 및 이상치 데이터 생성
    - 정상치 범위는 < Unsupervised Anomaly Detection on Multivariate Time Series in an Oracle Database ( Davide Di Mauro, 2022-2023) > 논문을 토대로 정의  
    - 단순 랜덤 값으로 이상치를 정의할 경우 실제 성능과 무관하므로, 최대한 현실성을 띄게 하기 위해 아래 내용을 고려하여 데이터 생성  
        1. **시간 패턴 반영**  
           - 시간대 영향 : 낮 시간대/피크 타임 값 상승 반영  
           - 요일 영향 : 주중 > 주말  
        2. **정규분포 기반 노이즈**  
           - 평균±표준편차 중심의 자연스러운 변동  
           - 단순 난수 대비 현실적인 흔들림  
        3. **지표 간 상관관계**  
           - CPU ↑ → DB Time ↑  
           - Transactions ↑ → Redo/Commits ↑ 
    """)
    st.markdown("\n")
    st.markdown("\n")
    st.markdown("""
    ##### 정상 데이터 분포 확인
    - 대부분 지표는 평균 중심의 정규분포 형태  
    - 정상 상태에서는 일정 범위 내에서 유지되는 특성이 반영됨  
    """)

    # 이미지 띄우기 (파일이 있을 경우)
    st.image("assets/normal_정규분포.png", caption="컬럼 별 데이터 분포", use_container_width=True)
    st.markdown("""
    - 시간 패턴 반영 → 낮/주중 값 상승, 분포가 한쪽으로 치우치지 않음  
    - 정규분포 기반 노이즈 → 종 모양(bell-shape) 또는 long tail 형태  
    - 지표 상관관계 반영 → CPU, DB Time, User Calls/Commits 등 유사한 분포 확인
    """)