import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


def run():
    # st.title("모델")
    #
    # # 1. 사용 모델 소개
    # st.header("1️⃣ 사용 모델 소개")
    # st.markdown("""
    # 본 프로젝트에서는 **DB 성능 이상 탐지**를 위해 여러 비지도 학습 모델을 사용합니다.
    #
    # - **Isolation Forest**
    #   - 이상치 탐지에 특화된 앙상블 기반 모델
    #   - 데이터 분포를 기반으로 이상치 점수 계산
    # - **AutoEncoder (AE)**
    #   - 입력 데이터 재구성 오류를 기반으로 이상 탐지
    #   - 정상 패턴 학습 후, 재구성 오차가 큰 샘플을 이상치로 판단
    # - **One-class SVM**
    #   - 정상 데이터의 경계 학습 후, 경계 밖 샘플을 이상치로 판단
    #
    # 자세한 내용은 [Wiki 링크](https://www.notion.so/2767eb9760b780d4b7dfd9d7c2bc59c8?pvs=21) 참고
    # """)
    #
    # # 2. 모델 성능 평가 방법
    # st.header("2️⃣ 모델 성능 평가 방법")
    # st.markdown("""
    # - **평가 지표** : Recall 기반 평가
    # - **이상 판단 기준** : 여러 모델 예측 결과의 과반수 이상이 이상치인 경우 최종 이상 판단
    # - **혼동행렬(Confusion Matrix)**를 통해 평가
    #   - True Positive, False Positive, True Negative, False Negative 분석
    # - 자세한 내용은 [Wiki 링크](https://www.notion.so/2777eb9760b780419ccef94f4d13764c?pvs=21) 참고
    # """)
    #
    # # 3. 모델 하이퍼파라미터 튜닝
    # st.header("3️⃣ 모델 하이퍼파라미터 튜닝")
    # st.markdown("""
    # - 각 모델별 주요 하이퍼파라미터 튜닝
    #     - Isolation Forest : n_estimators, max_samples, contamination 등
    #     - AutoEncoder : hidden layer 크기, epoch 수, learning rate 등
    #     - One-class SVM : kernel, nu, gamma 등
    # - 튜닝 방법 및 실험 결과는 [Wiki 링크](https://www.notion.so/2777eb9760b7809f97c5db88c52d4b74?pvs=21) 참고
    # """)
    #
    # st.title("모델")

    # -----------------------------
    # 모델 카드
    # -----------------------------
    st.header("1️⃣ 사용 모델 소개")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Isolation Forest")
        st.markdown("""
        - 이상치 탐지 특화
        - 분포 기반 점수 계산
        - 장점: 빠르고 비지도 학습 가능
        """)

    with col2:
        st.subheader("AutoEncoder")
        st.markdown("""
        - 입력 데이터 재구성 오류 기반 이상치 탐지
        - 정상 패턴 학습 후 재구성 오차로 판단
        """)

    with col3:
        st.subheader("One-class SVM")
        st.markdown("""
        - 정상 데이터 경계 학습 후 경계 밖 샘플 이상치 판단
        - Kernel 기반 유연한 탐지 가능
        """)

    st.markdown("[자세한 내용 Wiki 링크](https://www.notion.so/2767eb9760b780d4b7dfd9d7c2bc59c8?pvs=21)")

    # -----------------------------
    # 모델 성능 표
    # -----------------------------
    st.header("2️⃣ 모델 성능 평가")
    st.markdown("Recall 기반 평가, 이상 판단 기준: 과반수 이상")

    # 예시 데이터
    perf_data = {
        "Model": ["Isolation Forest", "AutoEncoder", "One-class SVM"],
        "Recall": [0.85, 0.92, 0.88],
        "Precision": [0.80, 0.87, 0.83]
    }
    df_perf = pd.DataFrame(perf_data)
    st.table(df_perf)

    # -----------------------------
    # 혼동행렬 시각화
    # -----------------------------
    # st.subheader("혼동행렬 예시 (AutoEncoder)")
    #
    # cm = np.array([[50, 5],
    #                [7, 38]])  # 예시 값: [[TP, FP], [FN, TN]]
    #
    # fig, ax = plt.subplots()
    # sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=["Normal", "Anomaly"], yticklabels=["Normal", "Anomaly"], ax=ax)
    # ax.set_ylabel("Actual")
    # ax.set_xlabel("Predicted")
    # st.pyplot(fig)

    # -----------------------------
    # 하이퍼파라미터 튜닝
    # -----------------------------
    st.header("3️⃣ 하이퍼파라미터 튜닝")
    st.markdown("""
    - Isolation Forest: n_estimators, max_samples, contamination  
    - AutoEncoder: hidden layer 크기, epoch, learning rate  
    - One-class SVM: kernel, nu, gamma  

    [Wiki 링크](https://www.notion.so/2777eb9760b7809f97c5db88c52d4b74?pvs=21) 참고
    """)





# st.title("모델")
#
# # 1. 사용 모델 소개
# st.header("1️⃣ 사용 모델 소개")
# st.markdown("""
# 본 프로젝트에서는 **DB 성능 이상 탐지**를 위해 여러 비지도 학습 모델을 사용합니다.
#
# - **Isolation Forest**
#   - 이상치 탐지에 특화된 앙상블 기반 모델
#   - 데이터 분포를 기반으로 이상치 점수 계산
# - **AutoEncoder (AE)**
#   - 입력 데이터 재구성 오류를 기반으로 이상 탐지
#   - 정상 패턴 학습 후, 재구성 오차가 큰 샘플을 이상치로 판단
# - **One-class SVM**
#   - 정상 데이터의 경계 학습 후, 경계 밖 샘플을 이상치로 판단
#
# 자세한 내용은 [Wiki 링크](https://www.notion.so/2767eb9760b780d4b7dfd9d7c2bc59c8?pvs=21) 참고
# """)
#
# # 2. 모델 성능 평가 방법
# st.header("2️⃣ 모델 성능 평가 방법")
# st.markdown("""
# - **평가 지표** : Recall 기반 평가
# - **이상 판단 기준** : 여러 모델 예측 결과의 과반수 이상이 이상치인 경우 최종 이상 판단
# - **혼동행렬(Confusion Matrix)**를 통해 평가
#   - True Positive, False Positive, True Negative, False Negative 분석
# - 자세한 내용은 [Wiki 링크](https://www.notion.so/2777eb9760b780419ccef94f4d13764c?pvs=21) 참고
# """)
#
# # 3. 모델 하이퍼파라미터 튜닝
# st.header("3️⃣ 모델 하이퍼파라미터 튜닝")
# st.markdown("""
# - 각 모델별 주요 하이퍼파라미터 튜닝
#     - Isolation Forest : n_estimators, max_samples, contamination 등
#     - AutoEncoder : hidden layer 크기, epoch 수, learning rate 등
#     - One-class SVM : kernel, nu, gamma 등
# - 튜닝 방법 및 실험 결과는 [Wiki 링크](https://www.notion.so/2777eb9760b7809f97c5db88c52d4b74?pvs=21) 참고
# """)
#
# st.title("모델")

# -----------------------------
# 모델 카드
# -----------------------------
st.header("1️⃣ 사용 모델 소개")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Isolation Forest")
    st.markdown("""
    - 이상치 탐지 특화
    - 분포 기반 점수 계산
    - 장점: 빠르고 비지도 학습 가능
    """)

with col2:
    st.subheader("AutoEncoder")
    st.markdown("""
    - 입력 데이터 재구성 오류 기반 이상치 탐지
    - 정상 패턴 학습 후 재구성 오차로 판단
    """)

with col3:
    st.subheader("One-class SVM")
    st.markdown("""
    - 정상 데이터 경계 학습 후 경계 밖 샘플 이상치 판단
    - Kernel 기반 유연한 탐지 가능
    """)

st.markdown("[자세한 내용 Wiki 링크](https://www.notion.so/2767eb9760b780d4b7dfd9d7c2bc59c8?pvs=21)")

# -----------------------------
# 모델 성능 표
# -----------------------------
st.header("2️⃣ 모델 성능 평가")
st.markdown("Recall 기반 평가, 이상 판단 기준: 과반수 이상")

# 예시 데이터
perf_data = {
    "Model": ["Isolation Forest", "AutoEncoder", "One-class SVM"],
    "Recall": [0.85, 0.92, 0.88],
    "Precision": [0.80, 0.87, 0.83]
}
df_perf = pd.DataFrame(perf_data)
st.table(df_perf)

# -----------------------------
# 혼동행렬 시각화
# -----------------------------
# st.subheader("혼동행렬 예시 (AutoEncoder)")
#
# cm = np.array([[50, 5],
#                [7, 38]])  # 예시 값: [[TP, FP], [FN, TN]]
#
# fig, ax = plt.subplots()
# sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=["Normal", "Anomaly"], yticklabels=["Normal", "Anomaly"], ax=ax)
# ax.set_ylabel("Actual")
# ax.set_xlabel("Predicted")
# st.pyplot(fig)

# -----------------------------
# 하이퍼파라미터 튜닝
# -----------------------------
st.header("3️⃣ 하이퍼파라미터 튜닝")
st.markdown("""
- Isolation Forest: n_estimators, max_samples, contamination  
- AutoEncoder: hidden layer 크기, epoch, learning rate  
- One-class SVM: kernel, nu, gamma  

[Wiki 링크](https://www.notion.so/2777eb9760b7809f97c5db88c52d4b74?pvs=21) 참고
""")