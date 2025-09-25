import pandas as pd
import numpy as np
import datetime

def generate_sample_data(N=500, anomaly_ratio=0.05):
    np.random.seed(42)
    base_time = datetime.datetime.now()
    ts_index = [base_time + datetime.timedelta(seconds=i*10) for i in range(N)]

    # 정상 데이터 생성
    data = pd.DataFrame({
        'TIME': ts_index,
        'CPU_USAGE_PER_SEC': np.random.uniform(0, 80, N),
        'HOST_CPU_USAGE_PER_SEC': np.random.uniform(0, 5, N),
        'PHYSICAL_READS_PER_SEC': np.random.uniform(10, 300, N),
        'PHYSICAL_WRITES_PER_SEC': np.random.uniform(10, 300, N),
        'IO_MB_PER_SEC': np.random.uniform(0.5, 50, N),
        'REDO_GENERATED_PER_SEC': np.random.uniform(5, 200, N),
        'DB_BLOCK_CHANGES_PER_SEC': np.random.uniform(10, 300, N),
        'CONSISTENT_READ_GETS_PER_SEC': np.random.uniform(10, 1000, N),
        'LOGICAL_READS_PER_SEC': np.random.uniform(10, 1000, N),
        'DBWR_CHECKPOINTS_PER_SEC': np.random.uniform(0, 50, N),
        'EXECUTIONS_PER_SEC': np.random.uniform(0, 200, N),
        'HARD_PARSE_COUNT_PER_SEC': np.random.uniform(0, 50, N),
        'DB_TIME_PER_SEC': np.random.uniform(50, 1000, N),
        'AVG_ACTIVE_SESSIONS': np.random.randint(1, 100, N),
        'LOGONS_PER_SEC': np.random.uniform(0, 2, N),
        'USER_CALLS_PER_SEC': np.random.uniform(0, 100, N),
        'USER_COMMITS_PER_SEC': np.random.uniform(0, 50, N),
        'USER_ROLLBACKS_PER_SEC': np.random.uniform(0, 20, N),
        'ENQUEUE_WAITS_PER_SEC': np.random.uniform(0, 10, N)
    })

    # ========================
    # anomaly_yn 플래그 추가
    # ========================
    data["ANOMALY_YN"] = 0  # 기본값: 정상

    # 랜덤으로 anomaly_ratio 만큼 이상치로 지정
    anomaly_indices = np.random.choice(N, int(N * anomaly_ratio), replace=False)
    data.loc[anomaly_indices, "ANOMALY_YN"] = 1

    # 이상치 데이터는 일부 값을 비정상 범위로 치우치게 함
    data.loc[anomaly_indices, "CPU_USAGE_PER_SEC"] *= 2
    data.loc[anomaly_indices, "DB_TIME_PER_SEC"] *= 3
    data.loc[anomaly_indices, "PHYSICAL_READS_PER_SEC"] *= 3
    data.loc[anomaly_indices, "IO_MB_PER_SEC"] *= 2

    return data
