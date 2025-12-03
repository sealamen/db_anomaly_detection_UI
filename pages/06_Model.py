import streamlit as st
import pandas as pd

st.set_page_config(page_title="모델 설명", layout="wide")

st.title("⚛ 모델 ")
st.markdown("\n")
st.markdown("\n")

# --- 탭 생성 ---
tab1, tab2, tab3 = st.tabs(["1. 학습 모델 설명", "2. 평가 기준", "3. 하이퍼파라미터 튜닝"])

with tab1:
    st.markdown("\n")
    st.markdown("""
    ### 1. 이상치 탐지 모델 

    """)

    option = st.segmented_control(
        "모델 선택",
        ["Isolation Forest", "One-class SVM", "AutoEncoder"]
    )

    if option == "One-class SVM":
        st.subheader("One-class SVM")
        st.image("assets/ONE_CLASS_SVM.PNG", caption="One-class SVM", use_container_width=True)
        st.markdown("""
        - 장점 : 이론적 안정성(수학적 기초가 탄탄)
        - 단점 : 고차원 + 대규모 데이터에 느림, 스케일/파라미터에 민감
        """)

    elif option == "AutoEncoder":
        st.subheader("AutoEncoder")
        st.image("assets/AUTOENCODER.PNG", caption="AutoEncoder", use_container_width=True)
        st.image("assets/AUTOENCODER2.PNG", caption="AutoEncoder", use_container_width=True)
        st.markdown("""
        - 장점 : 딥러닝 특성 덕분에 고차원, 시계열, 이미지 등 복잡한 데이터셋에서 효과적.
        - 단점 : 학습 속도 느림
        """)


    else:
        st.subheader("Isolation Forest")
        st.image("assets/DECISION_TREE.PNG", caption="Decision Tree", use_container_width=True)
        st.image("assets/ISOLATION_FOREST.PNG", caption="Isolation Forest", use_container_width=True)
        st.markdown("""
        - 장점 : 빠름, 고차원 가능
        - 단점 : 복잡한 경계 표현 한계 
        """)

with tab2:
    st.markdown("\n")
    st.markdown("""
    ### 2. 평가 기준 
    """)
    st.markdown("\n")

    st.markdown("""
    ##### 이상치 판단 기준
    - 세 모델의 과반수 투표를 통해 이상치 판단
    - ex :  IF → 1 , OCSVM → 0, AE → 0
        - Final Alert: 0
    """)

    st.markdown("\n")
    st.markdown("""
    ##### 모델 평가 기준 : 분류 성능 평가지표 사용 
    - 이상 탐지 모델 특성 상 학습 데이터에 라벨이 없음 
    - 정답을 맞추는 환경을 구현하기 위해, 이상치 데이터에 ANOMALY 여부를 추가해서 평가
    - 운영 환경에서는 **Recall(재현율)을 우선**, 그다음 Precision 확인, 최종적으로 F1-score를 지표로 삼는 게 가장 합리적
        - Recall : 실제 이상 중에서 얼마나 많이 잡았는가
        - **DB 이상탐지는 실제 이상을 놓치는 것이 더욱 위험하므로, FN 을 최소화하는 것이 중요**
        - FP(정상인데 이상으로 판단)이 많아지는 것이 단점이겠지만, DB 모니터링에서 FP 는 보통 로그/알람으로 끝나기 때문에, 조금 많은 FP 는 감수 가능
    """)

with tab3:
    st.markdown("\n")
    st.markdown("""
    ### 3. 하이퍼파라미터 튜닝 
    튜닝 내용 
    - GridSearch 를 통한 하이퍼파라미터 최적화
    - 학습 데이터 증가(2만건 → 20만건)
    - 이상치에 변화를 주어 2%, 5%, 50%, 98% 테스트도 진행 (모델의 강건성과 적용 범위 검증)
        - AutoEncoder 제외 크게 수치가 흔들리는 모델은 없었음
        - DB 이상탐지 특성 상, 이상치가 크게 벗어날 경우가 없긴함
    """)

    st.markdown("\n")
    st.markdown("\n")
    # 데이터프레임 생성
    data = {
        "Anomaly %": ["2%", "", "",
                      "", "", "",
                      "", "", "",
                      "", "", ""],
        "Model": ["One-class SVM", "", "",
                  "Isolation Forest", "", "",
                  "AutoEncoder", "", "",
                  "Final Alert", "", ""],
        "Condition": ["튜닝 전 (20K)", "하이퍼파라미터튜닝", "학습 데이터 증가 (200K)",
                      "튜닝 전 (20K)", "하이퍼파라미터튜닝", "학습 데이터 증가 (200K)",
                      "튜닝 전 (20K)", "하이퍼파라미터튜닝", "학습 데이터 증가 (200K)",
                      "튜닝 전 (20K)", "하이퍼파라미터튜닝", "학습 데이터 증가 (200K)"],
        "Accuracy": ["0.9876", "0.9878 ▲0.0003", "0.9514 ▼0.0362",
                     "0.9741", "0.9464 ▼0.0278", "0.9585 ▼0.0157",
                     "0.9952", "0.9966 ▲0.0014", "0.9969 ▲0.0018",
                     "0.9902", "0.9883 ▼0.0019", "0.9924 ▲0.0022"],
        "Precision": ["0.6205", "0.6258 ▲0.0053", "0.2886 ▼0.3319",
                      "0.3413", "0.2674 ▼0.0739", "0.3219 ▼0.0194",
                      "1.0000", "1.0000 ≈0.0000", "1.0000 ≈0.0000",
                      "0.7409", "0.6371 ▼0.1038", "0.7349 ▼0.0060"],
        "Recall": ["0.9745", "0.9757 ▲0.0012", "0.9745 ≈0.0000",
                   "0.3148", "0.9664 ▲0.6516", "0.9734 ▲0.6586",
                   "0.7581", "0.8287 ▲0.0706", "0.8472 ▲0.0891",
                   "0.7813", "0.9653 ▲0.1840", "0.9722 ▲0.1909"],
        "F1": ["0.7582", "0.7626 ▲0.0043", "0.4453 ▼0.3129",
               "0.3275", "0.4189 ▲0.0914", "0.4838 ▲0.1563",
               "0.8624", "0.9063 ▲0.0439", "0.9173 ▲0.0549",
               "0.7606", "0.7676 ▲0.0070", "0.8371 ▲0.0765"],
        "Color": ["", "red", "blue",
                  "", "blue", "blue",
                  "", "red", "red",
                  "", "blue", "red"]
    }

    # 데이터프레임 생성
    df = pd.DataFrame(data)
    color_info = df["Color"]
    df = df.drop(columns=["Color"])


    # 첫 번째 행 모델명을 굵게 표시하기 위한 함수
    def make_bold(val, row_idx):
        if row_idx % 3 == 0:
            return f'<b>{val}</b>'
        return val


    # 색상과 증감 표시를 위한 함수
    # def color_cell(val, row_idx, col_name):
    #     if col_name in ["Accuracy", "Precision", "Recall", "F1"] and row_idx > 0:
    #         if "▲" in val and "red" in color_info[row_idx]:
    #             return f'<span style="color:red">{val}</span>'
    #         elif "▼" in val and "blue" in color_info[row_idx]:
    #             return f'<span style="color:blue">{val}</span>'
    #         elif "≈" in val:
    #             return f'<span style="color:black">{val}</span>'
    #     return val


    def color_cell(val, row_idx, col_name):
        if col_name in ["Accuracy", "Precision", "Recall", "F1"] and row_idx > 0:
            if "▲" in val:
                if color_info[row_idx] == "red":
                    return f'<span style="color:red">{val}</span>'
            elif "▼" in val:
                if color_info[row_idx] == "blue":
                    return f'<span style="color:blue">{val}</span>'
            elif "≈" in val:
                return f'<span style="color:black">{val}</span>'
        return val


    # 스타일이 적용된 데이터프레임 생성
    styled_df = pd.DataFrame()
    for col in df.columns:
        styled_df[col] = [color_cell(val, i, col) for i, val in enumerate(df[col])]

    # HTML로 표시
    st.write("##### 이상탐지 모델 성능 비교 결과")
    st.markdown(styled_df.to_html(escape=False, index=False), unsafe_allow_html=True)

    # 모델별 요약 정보
    st.markdown("""
    - **Isolation Forest**: 튜닝 및 데이터 확대 효과가 매우 큼 (특히 Recall 폭발적 상승)
    - **AutoEncoder**: 소량 이상치 환경에서 안정적으로 Recall 개선
    - **Final Alert**: 튜닝+데이터 확대 시 최고 성능으로 수렴
    """)

    # Recall이 가장 중요한 지표임을 강조
    st.info("운영 환경에서는 Recall(재현율)을 우선적으로 확인해야 합니다. DB 이상탐지는 실제 이상을 놓치는 것이 더욱 위험하므로, FN을 최소화하는 것이 중요합니다.")
