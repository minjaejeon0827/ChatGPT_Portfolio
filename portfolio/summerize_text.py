"""
* 요약 프로그램

*** 참고 ***
*** 파이썬 문서 ***
* with 문
참고 URL - https://docs.python.org/ko/3/reference/compound_stmts.html#index-16
참고 2 URL - https://velog.io/@hyungraelee/Python-with

*** 기타 문서 ***

"""

# 비쥬얼스튜디오 코드(VSCode)
# streamlit 터미널 실행 명령어
# streamlit run summerize_text.py

##### 패키지 불러오기 #####
from utils import openAI_util   # OpenAI 전용 유틸(util)

import streamlit as st   # streamlit -> Elias(앨리아스) st 

##### 메인 함수 #####
##### streamlit 패키지 활용해서 프로그램 UI 작성 및 기능 구현 함수 "get_response" 호출해서 프로그램 동작하게 하는 메인 코드 작성된 함수
def main():
    """
    Description: 메인 함수

    Parameters: 없음.

    Returns: 없음.
    """

    st.set_page_config(page_title="요약 프로그램")   # 프로그램 페이지 제목 설정 (page_title="요약 프로그램")

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
    st.header("📃요약 프로그램")   # "📃요약 프로그램" 프로그램 제목 화면 출력 (이모지 📃추가 가능)
    st.markdown('---')   # 구분선 추가('---')
    
    text = st.text_area("요약 할 글을 입력하세요")   # 요약 할 글 내용 입력 받기 및 해당 글 내용 값 text 변수 저장
    
    if st.button("요약"):   # "요약" 버튼 화면 출력 및 해당 버튼 Click 이벤트 발생시 if 문 실행
        # f'''~~~~~''' - 시스템 프롬프트와 text 변수 합쳐서 구현.
        # 시스템 프롬프트 문자열
        # 1. 시스템 프롬프트 문자열에 한국어로 요약 해달라고 2번 강조해서 작성해야 한국어 요약 가능
        #    - that summarizes text into **Korean language**.
        #    - the **text** sentences in **Korean language**.

        # 2. 글 내용 요약시 아래 4가지 사항 포함
        #    - 중복되는 내용 삭제하되, 중복되는 내용이 있는 경우 요약 비중 높이기
        #    - 사례 증거 보다는 개념과 주장 강조 및 요약
        #    - 3줄 이내 요약
        #    - 글머리 기호 형식 사용 (•)
        prompt = f'''
                  **Instructions** :
                  - You are an expert assistant that summarizes text into **Korean language**.
                  - Your task is to summarize the **text** sentences in **Korean language**.
                  - Your summaries should include the following :
                    - Omit duplicate content, but increase the summary weight of duplicate content.
                    - Summarize by emphasizing concepts and arguments rather than case evidence.
                    - Summarize in 3 lines.
                    - Use the format of a bullet point.
                  - text : {text}
                  '''
        
        messages_prompt = [{"role": "system", "content": prompt}]   # ChatGPT API에게 개발자가 요구하는 prompt input 양식 변경 및 해당 input 양식을 messages_prompt 변수 저장
        st.info(openAI_util.get_response(messages_prompt))   # get_response 함수 호출 및 프로그램 화면 "요약" 버튼 하단 ChatGPT 텍스트 응답 메시지 출력.

if __name__=="__main__":
    main()   # 메인 함수 실행