import streamlit as st


def run():
    st.set_page_config(page_title="한계점 및 보완점", layout="wide")

    st.title("⚠️ 한계점 및 보완점")

    st.markdown("""
    이번 프로젝트는 운영 DB 환경 접근과 일부 Oracle 기능 제한으로 인해 다음과 같은 한계점이 존재하지만,
    다양한 시뮬레이션과 모델 튜닝을 통해 보완하였습니다.
    """)

    st.subheader("1️⃣ 실무 데이터 사용 불가")
    st.markdown("""
    - 운영 DB 접근 불가로 인해 실제 트랜잭션/쿼리 로그 기반 데이터 수집 제한
    - **보완**: Python 시뮬레이션 및 Oracle 뷰 기반 샘플 데이터를 사용하여 유사 시나리오 생성
    - 시뮬레이션 데이터에 인위적 이상치 삽입으로 모델 학습/평가 가능
    """)

    st.subheader("2️⃣ UI 툴 선택 제한")
    st.markdown("""
    - Streamlit을 사용하여 대시보드를 구현했으나, Grafana/PowerBI 등 상용 UI 툴 직접 활용 불가
    - **보완**: Streamlit 기반으로 기능적 요구사항 대부분 구현
      - KPI 카드, 메인 모니터링 차트, Drill-down, Alert.log 통합 등
    """)

    st.subheader("3️⃣ Alert.log 및 쿼리 관련 데이터 수집 한계")
    st.markdown("""
    - 실제 운영 환경에서는 alert.log와 SQL 성능 로그를 통합 활용 가능하지만 테스트 환경에서는 전체 로그 접근 불가
    - **보완**: 랜덤 이벤트 및 주요 ORA 에러를 시뮬레이션하여 `alert_count` 생성, 이상 상황 재현
    """)

    st.subheader("4️⃣ Statspack/AWR 사용 제한")
    st.markdown("""
    - AWR/Statspack 스냅샷은 라이선스 및 환경 제약으로 직접 수집 불가
    - **보완**: V$ 뷰 기반 시계열 지표 추출 + 시뮬레이션 데이터 병합으로 학습/테스트 데이터 확보
    """)

    st.subheader("5️⃣ 비지도 학습 모델 한계")
    st.markdown("""
    - Isolation Forest, AutoEncoder, One-class SVM 등은 정상 패턴 학습 후 이상치 탐지 가능하지만 특정 패턴 변화에 민감할 수 있음
    - **보완**: 하이퍼파라미터 튜닝, 여러 모델 앙상블, 임계치 조정으로 탐지 성능 개선
    """)

    st.subheader("6️⃣ 시계열 복합 이상 시나리오 미반영")
    st.markdown("""
    - 일부 복합 이벤트(예: CPU 급등 + Lock wait 폭증 + TPS 급증) 시나리오가 실제보다 단순화됨
    - **보완**: 시뮬레이션 단계에서 다변량 이상 패턴 주입 및 테스트, 필요시 LSTM/TCN 등 시계열 모델 적용 가능
    """)

    st.info("핵심 요약: 실무 데이터 접근 제한 및 일부 Oracle 기능 사용 불가가 한계점, 시뮬레이션/뷰 데이터와 모델 튜닝으로 보완 완료")




st.set_page_config(page_title="한계점 및 보완점", layout="wide")

st.title("⚠️ 한계점 및 보완점")

st.markdown("""
이번 프로젝트는 운영 DB 환경 접근과 일부 Oracle 기능 제한으로 인해 다음과 같은 한계점이 존재하지만,
다양한 시뮬레이션과 모델 튜닝을 통해 보완하였습니다.
""")

st.subheader("1️⃣ 실무 데이터 사용 불가")
st.markdown("""
- 운영 DB 접근 불가로 인해 실제 트랜잭션/쿼리 로그 기반 데이터 수집 제한
- **보완**: Python 시뮬레이션 및 Oracle 뷰 기반 샘플 데이터를 사용하여 유사 시나리오 생성
- 시뮬레이션 데이터에 인위적 이상치 삽입으로 모델 학습/평가 가능
""")

st.subheader("2️⃣ UI 툴 선택 제한")
st.markdown("""
- Streamlit을 사용하여 대시보드를 구현했으나, Grafana/PowerBI 등 상용 UI 툴 직접 활용 불가
- **보완**: Streamlit 기반으로 기능적 요구사항 대부분 구현
  - KPI 카드, 메인 모니터링 차트, Drill-down, Alert.log 통합 등
""")

st.subheader("3️⃣ Alert.log 및 쿼리 관련 데이터 수집 한계")
st.markdown("""
- 실제 운영 환경에서는 alert.log와 SQL 성능 로그를 통합 활용 가능하지만 테스트 환경에서는 전체 로그 접근 불가
- **보완**: 랜덤 이벤트 및 주요 ORA 에러를 시뮬레이션하여 `alert_count` 생성, 이상 상황 재현
""")

st.subheader("4️⃣ Statspack/AWR 사용 제한")
st.markdown("""
- AWR/Statspack 스냅샷은 라이선스 및 환경 제약으로 직접 수집 불가
- **보완**: V$ 뷰 기반 시계열 지표 추출 + 시뮬레이션 데이터 병합으로 학습/테스트 데이터 확보
""")

st.subheader("5️⃣ 비지도 학습 모델 한계")
st.markdown("""
- Isolation Forest, AutoEncoder, One-class SVM 등은 정상 패턴 학습 후 이상치 탐지 가능하지만 특정 패턴 변화에 민감할 수 있음
- **보완**: 하이퍼파라미터 튜닝, 여러 모델 앙상블, 임계치 조정으로 탐지 성능 개선
""")

st.subheader("6️⃣ 시계열 복합 이상 시나리오 미반영")
st.markdown("""
- 일부 복합 이벤트(예: CPU 급등 + Lock wait 폭증 + TPS 급증) 시나리오가 실제보다 단순화됨
- **보완**: 시뮬레이션 단계에서 다변량 이상 패턴 주입 및 테스트, 필요시 LSTM/TCN 등 시계열 모델 적용 가능
""")

st.info("핵심 요약: 실무 데이터 접근 제한 및 일부 Oracle 기능 사용 불가가 한계점, 시뮬레이션/뷰 데이터와 모델 튜닝으로 보완 완료")