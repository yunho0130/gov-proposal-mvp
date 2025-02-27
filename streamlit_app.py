import streamlit as st
from openai import OpenAI

# 제목과 설명 표시
st.title("🏢 정부지원과제 사업계획서 작성기")
st.write(
    "정부지원과제 공고문을 입력하고 회사 정보를 제공하면 AI가 사업계획서를 작성해드립니다! "
    "이 앱을 사용하려면 OpenAI API 키가 필요합니다."
)

# OpenAI API 키 입력 받기
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("OpenAI API 키를 입력해주세요.", icon="🗝️")
else:
    # OpenAI 클라이언트 생성
    client = OpenAI(api_key=openai_api_key)
    
    # GPT 모델 선택
    available_models = ["gpt-4-turbo-preview", "gpt-4", "gpt-3.5-turbo"]
    selected_model = st.selectbox(
        "사용할 API 모델을 선택하세요",
        options=available_models
    )

    # 공고문 입력 받기
    announcement = st.text_area(
        "정부지원과제 공고문을 입력하세요",
        height=200,
        placeholder="공고 내용을 여기에 붙여넣기 해주세요..."
    )

    # 회사 정보 입력 받기
    st.subheader("회사 정보")
    company_name = st.text_input("회사명")
    company_description = st.text_area("회사 소개", height=100)
    business_area = st.text_input("주요 사업분야")
    company_size = st.number_input("직원 수", min_value=1)
    annual_revenue = st.number_input("연간 매출액(백만원)", min_value=0)
    
    if st.button("사업계획서 생성") and announcement and company_name:
        # 입력 정보 구성
        prompt = f"""
        정부지원과제 공고문: {announcement}
        
        회사 정보:
        - 회사명: {company_name}
        - 회사 소개: {company_description}
        - 주요 사업분야: {business_area}
        - 직원 수: {company_size}명
        - 연간 매출액: {annual_revenue}백만원
        
        위 정보를 바탕으로 30페이지 분량의 상세한 사업계획서를 작성해주세요.
        다음 항목들을 포함해야 합니다:
        1. 사업 개요
        2. 기술성 분석
        3. 시장성 분석
        4. 사업화 계획
        5. 재무 계획
        6. 기대 효과
        """

        # OpenAI API를 사용하여 사업계획서 생성
        with st.spinner('사업계획서를 생성하고 있습니다...'):
            response = client.chat.completions.create(
                model=selected_model,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )
            
            # 생성된 결과 표시
            st.write(response.choices[0].message.content)
