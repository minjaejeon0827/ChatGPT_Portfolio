"""
* 번역 플랫폼 비교하기 프로그램

*** 참고 ***
*** 파이썬 문서 ***
* with 문
참고 URL - https://docs.python.org/ko/3/reference/compound_stmts.html#index-16
참고 2 URL - https://velog.io/@hyungraelee/Python-with

*** 기타 문서 ***

"""

# 비쥬얼스튜디오 코드(VSCode)
# streamlit 터미널 실행 명령어
# streamlit run translate.py

##### 패키지 불러오기 #####
from utils import openAI_util   # OpenAI 전용 유틸(util)
from utils import google_util   # Google 전용 유틸(util)
from utils import deepl_util    # Deepl 전용 유틸(util)
# from utils import papago_util   # PAPAGO 전용 유틸(util) / PAPAGO API 서비스 종료로 인해 해당 유틸(util) 사용 안 함.

import streamlit as st   # streamlit -> Elias(앨리아스) st

##### 메인 함수 #####
def main():
    """
    Description: 메인 함수

    Parameters: 없음.

    Returns: 없음.
    """

    st.set_page_config(page_title="번역 플랫폼 모음", layout="wide")   # 프로그램 페이지 제목 설정 (page_title="번역 플랫폼 모음"), 메인 공간 레이아웃 설정 (layout="wide")

    # st.session_state 초기화 코드 - 프로그램에서 어떤 이벤트가 발생해도 정보를 잃지 않고 유지할 session_state 4가지 지정
    if "OPENAI_API" not in st.session_state:   # "OPENAI_API" - OPENAI API 키
        st.session_state["OPENAI_API"] = ""

    # PAPAGO API 서비스 종료로 인해 아래 로직 사용 안 함.
    # if "PAPAGO_ID" not in st.session_state:   # "PAPAGO_ID" - PAPAGO API ID
    #     st.session_state["PAPAGO_ID"] = ""

    # if "PAPAGO_PW" not in st.session_state:   # "PAPAGO_PW" - PAPAGO API PASSWORD
    #     st.session_state["PAPAGO_PW"] = ""

    if "Deepl_API" not in st.session_state:   # "Deepl_API" - Deepl API 키
        st.session_state["Deepl_API"] = ""

    with st.sidebar:   # 파이썬 with 문 사용 및 좌측 사이드바 생성 (OpenAI/Deepl API 키 입력 받는 용도)
        # OpenAI API 키 입력 받기 및 해당 키 값 st.session_state["OPENAI_API"] 변수 저장 (type='password' 사용하여 OpenAI API 키 값 노출 안 되도록 마스킹 처리)
        st.session_state["OPENAI_API"] = st.text_input(label='OPENAI API 키', placeholder='Enter Your OpenAI API Key', value='', type='password')

        st.markdown('---')   # 구분선 추가('---')

        # PAPAGO API 서비스 종료로 인해 아래 로직 사용 안 함.
        # PAPAGO API ID/PW 입력 받기 및 해당 ID/PW st.session_state["PAPAGO_ID"], st.session_state["PAPAGO_PW"] 변수 저장 (type='password' 사용하여 PAPAGO API PW 값 노출 안 되도록 마스킹 처리)
        # st.session_state["PAPAGO_ID"] = st.text_input(label='PAPAGO API ID', placeholder='Enter PAPAGO ID', value='')
        # st.session_state["PAPAGO_PW"] = st.text_input(label='PAPAGO API PW', placeholder='Enter PAPAGO PW', value='', type='password')

        # st.markdown('---')   # 구분선 추가('---')

        # Deepl API 키 입력 받기 및 해당 키 값 st.session_state["Deepl_API"] 변수 저장 (type='password' 사용하여 Deepl API 키 값 노출 안 되도록 마스킹 처리)
        st.session_state["Deepl_API"] = st.text_input(label='Deepl API 키', placeholder='Enter Your Deepl API Key', value='', type='password')
    
        st.markdown('---')   # 구분선 추가('---')

    # 메인 공간
    st.header("번역 플랫폼 비교하기 프로그램")   # "번역 플랫폼 비교하기 프로그램" 프로그램 제목 화면 출력
    st.markdown('---')   # 구분선 추가('---')

    st.subheader("번역 하고자 하는 텍스트 입력하세요")   # "번역 하고자 하는 텍스트 입력하세요" 프로그램 소제목 화면 출력
    messages = st.text_area(label="", placeholder="input English..", height=200)   # 번역 할 텍스트 내용 입력 받기 및 해당 글 내용 값 messages 변수 저장
    st.markdown('---')   # 구분선 추가('---')

    st.subheader("ChatGPT 번역 결과")   # "ChatGPT 번역 결과" 프로그램 소제목 화면 출력
    st.text("https://openai.com/blog/chatgpt")   # ChatGPT URL 주소 프로그램 화면 출력

    # None or Empty String Check
    # 참고 URL - https://stackoverflow.com/questions/9573244/how-to-check-if-the-string-is-empty-in-python
    # 참고 2 URL - https://hello-bryan.tistory.com/131
    # 참고 3 URL - https://jino-dev-diary.tistory.com/42
    # 참고 4 URL - https://claude.ai/chat/eaf7856e-1b5e-4c26-992e-de1683005638
    if st.session_state["OPENAI_API"] and messages:   # st.session_state["OPENAI_API"] / messages 변수 할당된 값이 None 또는 공백("")이 아닌 경우 (None or Empty String Check)
        openAI_util.openai.api_key = st.session_state["OPENAI_API"]   # openAI_util.openai.api_key 변수에 입력 받은 st.session_state["OPENAI_API"] 값을 저장 (이렇게 처음에 OpenAI API 키 지정 한번 해 놓으면 OpenAI 패키지를 사용하는 코드 안에서는 더이상 따로 API 입력할 필요 없음.)
        
        # f'~~~~~' - 시스템 프롬프트와 messages 변수 합쳐서 구현.
        # 시스템 프롬프트 문자열
        # 영어 -> 한국어 번역 (번역 할 텍스트 내용 - {messages})
        messages_prompt = [{"role": "system", "content": f'Translate the following english text into Korean. Text to translate: {messages}'}]
        st.info(openAI_util.get_response(messages_prompt))   # get_response 함수 호출 및 프로그램 화면 영어 -> 한글 번역된 ChatGPT 텍스트 응답 메시지 출력.
    else:
        st.info("API 키 넣으세요")   # 텍스트 추가("API 키 넣으세요")
    st.markdown('---')   # 구분선 추가('---')

    # PAPAGO API 서비스 종료로 인해 아래 로직 사용 안 함.
    # st.subheader("PAPAGO 번역 결과")   # "PAPAGO 번역 결과" 프로그램 소제목 화면 출력
    # st.text("https://papago.naver.com/")   # PAPAGO URL 주소 프로그램 화면 출력
    # if st.session_state["PAPAGO_ID"] and st.session_state["PAPAGO_PW"] and messages:   # st.session_state["PAPAGO_ID"] / messages 변수 할당된 값이 None 또는 공백("")이 아닌 경우 (None or Empty String Check)
    #     st.info(papago_util.translate(messages, st.session_state["PAPAGO_ID"], st.session_state["PAPAGO_PW"], "ko"))   # papago_util.translate 함수 호출 및 프로그램 화면 영어 -> 한글 번역된 PAPAGO 텍스트 응답 메시지 출력.
    # else:
    #     st.info("PAPAGO API ID, PW 넣으세요")   # 텍스트 추가("PAPAGO API ID, PW 넣으세요")
    # st.markdown('---')   # 구분선 추가('---')

    st.subheader("Deepl 번역 결과")   # "Deepl 번역 결과" 프로그램 소제목 화면 출력
    st.text("https://www.deepl.com/translator")   # Deepl URL 주소 프로그램 화면 출력
    if st.session_state["Deepl_API"] and messages:   # st.session_state["Deepl_API"] / messages 변수 할당된 값이 None 또는 공백("")이 아닌 경우 (None or Empty String Check)
        st.info(deepl_util.translate(messages, st.session_state["Deepl_API"], "KO"))   # deepl_util.translate 함수 호출 및 프로그램 화면 영어 -> 한글 번역된 Deepl 텍스트 응답 메시지 출력.
    else:
        st.info("API 키 넣으세요")   # 텍스트 추가("API 키 넣으세요")
    st.markdown('---')   # 구분선 추가('---')

    st.subheader("Google 번역 결과")   # "Google 번역 결과" 프로그램 소제목 화면 출력
    st.text("https://translate.google.co.kr/")   # Google URL 주소 프로그램 화면 출력

    if messages:   # messages 변수 할당된 값이 None 또는 공백("")이 아닌 경우 (None or Empty String Check)
        st.info(google_util.translate(messages, "ko"))   # google_util.translate 함수 호출 및 프로그램 화면 영어 -> 한글 번역된 Google 텍스트 응답 메시지 출력.
    else:
        st.info("API 키 필요 없습니다")   # 텍스트 추가("API 키 필요 없습니다")
    st.markdown('---')   # 구분선 추가('---')

if __name__=="__main__":
    main()   # 메인 함수 실행
