"""
*** 참고 ***
*** ChatGPT 문서 ***
* ChatGPT 텍스트 응답 메시지
참고 URL - https://github.com/openai/openai-python

*** 파이썬 문서 ***
* with 문
참고 URL - https://docs.python.org/ko/3/reference/compound_stmts.html#index-16
참고 2 URL - https://velog.io/@hyungraelee/Python-with

*** 기타 문서 ***

"""

# 비쥬얼스튜디오 코드(VSCode)
# streamlit 터미널 실행 명령어
# streamlit run generate_ads.py

##### 패키지 불러오기 #####
from utils import openAI_util   # OpenAI 전용 유틸 (util)

import streamlit as st   # streamlit -> Elias(앨리아스) st 

##### 메인 함수 #####
##### streamlit 패키지 활용해서 프로그램 UI 작성 및 기능 구현 함수 "ask_gpt" 호출해서 프로그램 동작하게 하는 메인 코드 작성된 함수
def main() -> None:
    """
    Description: 메인 함수

    Parameters: 없음.

    Returns: 없음.
    """

    st.set_page_config(page_title="광고 문구 생성 프로그램")   # 프로그램 페이지 제목 설정 (page_title="광고 문구 생성 프로그램")

    with st.sidebar:   # 파이썬 with 문 사용 및 좌측 사이드바 생성 (OpenAI API 키 입력 받는 용도)
        open_api_key = st.text_input(label='OpenAI API 키', placeholder='Enter Your API Key', value='', type='password')   # OpenAI API 키 입력 받기 및 해당 키 값 open_api_key 변수 저장 (type='password' 사용하여 OpenAI API 키 값 노출 안 되도록 마스킹 처리)
        
        # None or Empty String Check
        # 참고 URL - https://stackoverflow.com/questions/9573244/how-to-check-if-the-string-is-empty-in-python
        # 참고 2 URL - https://hello-bryan.tistory.com/131
        # 참고 3 URL - https://jino-dev-diary.tistory.com/42
        # 참고 4 URL - https://claude.ai/chat/eaf7856e-1b5e-4c26-992e-de1683005638
        if open_api_key:   # open_api_key 변수 할당된 값이 None 또는 공백("")이 아닌 경우 (None or Empty String Check)
            openAI_util.openai.api_key = open_api_key   # openai.api_key 변수에 입력 받은 open_api_key 값을 저장 (이렇게 처음에 OpenAI API 키 지정 한번 해 놓으면 OpenAI 패키지를 사용하는 코드 안에서는 더이상 따로 API 입력할 필요 없음.)
        st.markdown('---')   # 구분선 추가('---') - 혹시 밑에 다른 엘리멘트들을 추가할 때 대비해서 구현.

    # 메인 공간
    st.header("🎸광고 문구 생성 프로그램")   # "🎸광고 문구 생성 프로그램" 프로그램 제목 화면 출력 (이모지 🎸추가 가능)
    st.markdown('---')   # 구분선 추가('---')

    # 세로 공간 나누기
    col1, col2 = st.columns(2)   # 웹브라우저 화면 사이드바 우측 메인 공간 2등분 및 2등분 한 각각의 공간 이름 왼쪽 공간 col1, 오른쪽 공간 col2 지정

    with col1:  # 메인 공간의 왼쪽 공간 col1에 name, product_strength, keyword 작성(추가) -> 웹브라우저 화면 왼쪽 공간 col1 데이터 시각화
        product_name = st.text_input("제품명", placeholder=" ")
        product_strength = st.text_input("제품 특징", placeholder=" ")
        keyword = st.text_input("필수 포함 키워드", placeholder=" ")

    with col2:  # 메인 공간의 오른쪽 공간 col2에 brand_name, tone_manner, value 작성(추가) -> 웹브라우저 화면 오른쪽 공간 col2 데이터 시각화
        brand_name = st.text_input("브랜드 명", placeholder="Apple, 올리브영...")
        tone_manner = st.text_input("톤엔 메너", placeholder="발랄하게, 유머러스하게, 감성적으로...")
        brand_value = st.text_input("브랜드 핵심 가치", placeholder="필요 시 입력")

    if st.button("광고 문구 생성"):   # "광고 문구 생성" 버튼 화면 출력 및 해당 버튼 Click 이벤트 발생시 if 문 실행
        prompt = f'''
                  아래 내용 참고해서 1~2줄 짜리 광고 문구 8개 작성해줘
                  - 제품명: {product_name}
                  - 브랜드 명: {brand_name}
                  - 브랜드 핵심 가치: {brand_value}
                  - 제품 특징: {product_strength}
                  - 톤엔 매너: {tone_manner}
                  - 필수 포함 키워드: {keyword}
                  '''
        
        st.info(openAI_util.ask_gpt(prompt))   # 함수 ask_gpt 호출 및 웹브라우저 화면 "광고 문구 생성" 버튼 하단 ChatGPT 텍스트 응답 메시지 출력.

if __name__=='__main__':
    main()   # 메인 함수 실행