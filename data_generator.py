import pandas as pd
import numpy as np
import datetime

def generate_sample_data(N=500, anomaly_ratio=0.05):
    np.random.seed(42)
    base_time = datetime.datetime.now()
    ts_index = [base_time + datetime.timedelta(seconds=i) for i in range(N)]

    # 정상 데이터 생성
    data = pd.DataFrame({
        'TIME': ts_index,
        'HOST_CPU_UTIL_PCT': np.random.uniform(10, 80, N),
        'HOST_CPU_USAGE_PER_SEC': np.random.uniform(0, 5, N),
        'DB_CPU_TIME_RATIO': np.random.uniform(0, 0.5, N),
        'DB_CPU_USAGE_PER_SEC': np.random.uniform(0, 5, N),
        'CPU_USAGE_PER_TXN': np.random.uniform(0.01, 0.1, N),
        'BG_CPU_USAGE_PER_SEC': np.random.uniform(0, 2, N),
        'BUFFER_CACHE_HIT_RATIO': np.random.uniform(85, 99, N),
        'SHARED_POOL_FREE_PCT': np.random.uniform(15, 50, N),
        'LIBRARY_CACHE_HIT_RATIO': np.random.uniform(85, 99, N),
        'SESSIONS_TOTAL': np.random.randint(50, 300, N),
        'ACTIVE_SESSIONS': np.random.randint(10, 100, N),
        'LOGONS_PER_SEC': np.random.uniform(0, 2, N),
        'PROCESS_COUNT': np.random.randint(50, 400, N),
        'PHYSICAL_READS_PER_SEC': np.random.uniform(10, 300, N),
        'PHYSICAL_WRITES_PER_SEC': np.random.uniform(10, 300, N),
        'REDO_WRITES_PER_SEC': np.random.uniform(5, 200, N),
        'IO_REQUESTS_PER_SEC': np.random.uniform(20, 1000, N),
        'IO_THROUGHPUT_MB_SEC': np.random.uniform(0.5, 50, N),
        'AVG_READ_LATENCY_MS': np.random.uniform(1, 20, N),
        'AVG_WRITE_LATENCY_MS': np.random.uniform(1, 20, N),
        'DB_TIME_MS': np.random.uniform(50, 1000, N),
        'CPU_TIME_MS': np.random.uniform(10, 500, N),
        'USER_IO_WAIT_MS': np.random.uniform(5, 200, N),
        'SYSTEM_IO_WAIT_MS': np.random.uniform(5, 200, N),
        'LOG_FILE_SYNC_WAIT_MS': np.random.uniform(1, 50, N),
        'CONCURRENCY_WAIT_MS': np.random.uniform(0, 100, N),
        'TXN_PER_SEC': np.random.uniform(0, 50, N),
        'USER_CALLS_PER_SEC': np.random.uniform(0, 100, N),
        'EXECUTIONS_PER_SEC': np.random.uniform(0, 200, N),
        'PARSE_COUNT_PER_SEC': np.random.uniform(0, 50, N),
        'HARD_PARSE_RATIO_PCT': np.random.uniform(0, 20, N),
        'SGA_FREE_MB': np.random.uniform(200, 1000, N),
        'PGA_USED_MB': np.random.uniform(50, 500, N)
    })

    # ========================
    # anomaly_yn 플래그 추가
    # ========================
    data["ANOMALY_YN"] = 0  # 기본값: 정상

    # 랜덤으로 anomaly_ratio 만큼 이상치로 지정
    anomaly_indices = np.random.choice(N, int(N * anomaly_ratio), replace=False)
    data.loc[anomaly_indices, "ANOMALY_YN"] = 1

    # 이상치 데이터는 일부 값을 비정상 범위로 치우치게 함
    data.loc[anomaly_indices, "CPU_TIME_MS"] *= 5
    data.loc[anomaly_indices, "TXN_PER_SEC"] *= 4
    data.loc[anomaly_indices, "BUFFER_CACHE_HIT_RATIO"] = np.random.uniform(50, 70, len(anomaly_indices))

    return data
