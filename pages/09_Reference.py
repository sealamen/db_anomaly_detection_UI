import streamlit as st


st.set_page_config(page_title="References", layout="wide")
st.title("📚 레퍼런스 / 참고 논문")

st.markdown("""
이번 프로젝트에서는 다음 논문과 자료를 참조하여 DB 성능 이상 탐지 및 핵심 지표 선정 기준을 마련했습니다.
""")

st.subheader("1️⃣ Database Performance Analytics Using Anomaly Detection (Roger Cornejo, 2022)")
st.markdown("""
**사례연구: 성능 이상 탐지**
- 정량적 지표 + 동적 기준(Dynamic Threshold) + 패턴 변화 탐지

**핵심 지표 예시**
| 지표 | 설명 | 기준 / 이상 판단 |
| --- | --- | --- |
| HOST_CPU_UTIL_PCT | 호스트 전체 CPU 사용률 | 평균 + 2~3σ 초과 시 이상 |
| DB_CPU_TIME_RATIO | DB CPU 비율 | 평소 평균 대비 30% 이상 증가 → 이상 |
| SESSIONS_TOTAL | 총 세션 수 | 평균 + 2σ 초과 → 세션 폭주 가능성 |
| ACTIVE_SESSIONS | 실제 활성 세션 수 | 예상 범위 벗어나면 경고 |
| LOGONS_PER_SEC | 초당 로그인 수 | 2배 이상 증가 → 트래픽 폭주 판단 |
| TOTAL_TABLE_SCANS_PER_SEC | 초당 테이블 스캔 | 평균 + 2σ 초과 → 쿼리 비효율 가능 |
| CPU_TIME_MS / TXN_PER_SEC | 트랜잭션당 CPU 소모 | 평소 대비 3배 이상 → 특정 트랜잭션 문제 가능 |

**핵심 포인트**
- 동적 임계값 기반 이상 탐지 (시간대별/부하별 적용)
- 패턴 기반 이상 탐지: 급격한 상승, 지속적 고부하, 비정상 감소 관찰
""")

st.subheader(
    "2️⃣ Unsupervised Anomaly Detection on Multivariate Time Series in an Oracle Database (Davide Di Mauro, 2022-2023)")
st.markdown("""
**핵심 지표 선정 과정**
- V$SYSMETRIC 뷰 활용, 155개 지표 → 19개 핵심 지표 선별
- 선정 기준: 운영 경험, 통계적 중요성, 수집 용이성
- 확장 실험: 60개 지표 사용 시 이상 탐지 증가, 원인 분석 용이하지만 성능 저하

**19개 핵심 메트릭 요약**
1. DB Time per Sec – 전체 DB 활동 시간 (종합 지표)
2. CPU Usage per Sec – DB CPU 사용
3. Host CPU Usage per Sec – 호스트 전체 CPU
4. Physical Reads per Sec – 디스크 읽기
5. Physical Writes per Sec – 디스크 쓰기
6. Redo Generated per Sec – Redo 로그
7. User Calls per Sec – 사용자 호출
8. Commits per Sec – Commit 횟수
9. Rollbacks per Sec – Rollback 횟수
10. Executions per Sec – SQL 실행 횟수
11. Hard Parse Count per Sec – Hard Parse 횟수
12. Average Active Sessions – 평균 활성 세션
13. Logons per Sec – 신규 세션 연결
14. Parse Count per Sec – SQL Parse 횟수
15. Transactions per Sec – 트랜잭션 수
16. Enqueue Waits per Sec – Lock 대기
17. Host CPU Utilization (%) – 호스트 CPU %
18. DB CPU Ratio (%) – DB CPU 비율
19. SQL Service Response Time – SQL 평균 응답 시간

**핵심 테마**
- CPU, I/O, 세션/트랜잭션, SQL, 동시성
- 19개 지표로 실시간 이상 탐지, 60개 지표로 사후 분석 가능
""")

st.info("💡 요약: 두 논문 모두 DB 성능 이상 탐지 및 핵심 지표 선정 기준을 제공, 동적 기준과 경험적 지표 중요 강조")