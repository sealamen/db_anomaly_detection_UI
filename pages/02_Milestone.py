import streamlit as st

st.title("프로젝트 마일스톤")

# 이미지 표시
st.image("assets/MILESTONE.PNG", caption="Milestone Roadmap", use_container_width=True)

# 설명 텍스트
st.markdown("""
- **DAY1~3 : 서비스 아키텍처 구축**
- **DAY4~6 : 서비스 고도화, 클라우드 전환, 실시간 탐지 구현**
- 서비스 테스트 및 수정 과정에서 시간이 많이 소요되어, OCI 전환은 진행 X 

""")