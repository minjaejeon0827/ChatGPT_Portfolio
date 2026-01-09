# *** 파이썬 설치 시 주의사항 ***
# 꼭 파이썬 설치 시 3.11 버전 설치 필수! (3.12 버전에서 openai 패키지와 충돌하는 현상 발생.)
# 만약 파이썬 3.12 버전 설치 진행시 가상환경에 아래의 패키지 먼저 설치 필수!
# pip install aiottp==3.9.0b0

# 가상환경 폴더 "portfolio_env" 생성 터미널 명령어
# python -m venv portfolio_env

# 가상환경 폴더 "portfolio_env" 활성화 터미널 명령어
# portfolio_env\Scripts\activate.bat

# Python 기반 웹 애플리케이션 UI 프레임워크 오픈 소스 패키지 streamlit
# 터미널 설치 명령어
# pip install streamlit

# OpenAI 오픈 소스 패키지 openai
# 터미널 설치 명령어
# pip install openai==0.28.1
# 만약 이미 1.0.0 이상의 버전을 설치 할 경우 먼저 아래 명령어로 패키지 삭제 후 다시 설치 진행 필수!
# OpenAI 패키지 삭제 명령어
# pip uninstall openai

# 구글 번역기 오픈 소스 패키지 googletrans
# 터미널 설치 명령어
# pip install googletrans==3.1.0a0
# 구글 번역기 오픈 소스 패키지 googletrans 의 경우 따로 API 키 발급이 필요 없다.
# from googletrans import Translator # 패키지 googletrans에서 Translator 클래스 가져오기

# TODO: DeepL API 신용카드 등록 오류로 인하여 DeepL API 키 발급 실패함. (2025.01.02 minjae)
# DeepL 오픈 소스 패키지 deepl 
# 터미널 설치 명령어
# pip install deepl==1.15.0

##### 패키지 불러오기 #####
import streamlit as st   # Streamlit 패키지 추가 (streamlit 패키지를 st 앨리아스로 명칭 변경)
import openai   # OpenAI 패키지 추가
from googletrans import Translator   # 구글 번역 패키지 추가
import deepl   # Deepl 번역 패키지 추가
import requests   # 파파고 API요청을 위한 Requests 패키지 추가


##### 기능 구현 함수 #####
# ChatGPT 번역
def gpt_translate(messages):
    # 다음에 오는 영어 텍스트를 한글로 번역해달라고 아래처럼 시스템 프롬프트 작성하기
    # Text to translate 옆에 영어 -> 한글로 번역할 텍스트 변수 {messages} 추가 구현하기     
    # f'Translate the following english text into Korean. Text to translate
    messages_prompt = [{"role": "system", "content": f'Translate the following english text into Korean. Text to translate: {messages}'}]
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages_prompt)

    system_message = response["choices"][0]["message"]

    # ChatGPT 최종 답변(system_message["content"]) 리턴 
    return system_message["content"]

# 파파고 번역 (파파고 API 서비스 종료로 인해 실제로 사용하지 않는 함수이다.)
def papago_translate(text, papago_id, papago_pw):
    data = {'text' : text,
            'source' : 'en',
            'target': 'ko'}

    url = "https://openapi.naver.com/v1/papago/n2mt"

    header = {"X-Naver-Client-Id": papago_id,
              "X-Naver-Client-Secret": papago_pw}

    response = requests.post(url, headers=header, data=data)
    rescode = response.status_code

    if 200 == rescode:
        send_data = response.json()
        trans_data = (send_data['message']['result']['translatedText'])
        return trans_data
    else:
        print("Error Code:" , rescode)

# 구글 번역
def google_trans(messages):
    google = Translator()
    result = google.translate(messages, dest="ko")

    return result.text

# 디플(DeepL) 번역 
# DeepL API 신용카드 등록 오류로 인하여 DeepL API 키 발급 실패해서 실제로 사용하지 않는 함수이다.
def deepl_translate(text, deeplAPI):
    translator = deepl.Translator(deeplAPI)
    result = translator.translate_text(text, target_lang="KO")
    return result.text


##### 메인 함수 #####
def main():
    # 기본 설정
    # 프로그램 제목(page_title="번역 플랫폼 모음") 정하기 
    st.set_page_config(
        page_title="번역 플랫폼 모음",
        layout="wide")

    # session state 초기화
    # 프로그램에서 어떤 이벤트가 발생해도 정보를 잃지 않고 유지할 4가지 session_state 지정하기 
    # session_state 초기화 코드 
    # "OPENAI_API" - OPENAI API 키를 의미
    if "OPENAI_API" not in st.session_state:
        st.session_state["OPENAI_API"] = ""

    # "PAPAGO_ID" - PAPAGO ID를 의미
    if "PAPAGO_ID" not in st.session_state:
        st.session_state["PAPAGO_ID"] = ""

    # "PAPAGO_PW" - PAPAGO PASSWORD를 의미
    if "PAPAGO_PW" not in st.session_state:
        st.session_state["PAPAGO_PW"] = ""

    # "DeeplAPI" - DeeplAPI 키를 의미
    if "DeeplAPI" not in st.session_state:
        st.session_state["DeeplAPI"] = ""


    # 사이드바 생성
    with st.sidebar:

        # Open AI API 키 입력받기
        # st.text_input 사용해서 OpenAI API 키 입력받기
        st.session_state["OPENAI_API"] = st.text_input(label='OPENAI API 키', placeholder='Enter Your OpenAI API Key', value='', type='password')

        st.markdown('---')

        # PAPAGO API ID/PW 입력받기
        st.session_state["PAPAGO_ID"] = st.text_input(label='PAPAGO API ID', placeholder='Enter PAPAGO ID', value='')
        st.session_state["PAPAGO_PW"] = st.text_input(label='PAPAGO API PW', placeholder='Enter PAPAGO PW', value='', type='password')

        st.markdown('---')

        # Deepl API ID/PW 입력받기
        st.session_state["DeeplAPI"] = st.text_input(label='Deepl API 키', placeholder='Enter Your Deepl API Key', value='', type='password')
    
        st.markdown('---')

    # 제목
    # st.header 사용해서 "번역 플랫폼 비교하기 프로그램" 화면 출력
    st.header('번역 플랫폼 비교하기 프로그램')
    # 구분선
    st.markdown('---')   # markdown 사용해서 구분선 생성(st.markdown('---'))
    st.subheader("번역을 하고자 하는 텍스트를 입력하세요")
    # 긴 글을 입력받기 위해 st.text_input 함수 사용 안 하고 
    # st.text_area 함수 사용함. 해당 긴글은 변수 txt에 저장 
    txt = st.text_area(label="", placeholder="input English..", height=200)
    st.markdown('---')

    st.subheader("ChatGPT 번역 결과")
    st.text("https://openai.com/blog/chatgpt")
    # OpenAI API 키(st.session_state["OPENAI_API"]) 값이 존재하고 
    # 변수 txt값이 존재하면(사용자로 부터 긴글 입력받았을 때) 해당 if절 안의 코드 실행
    if st.session_state["OPENAI_API"] and txt:
        # 입력 받은 OpenAI API 키(st.session_state["OPENAI_API"])를 변수 openai.api_key에 저장 
        openai.api_key = st.session_state["OPENAI_API"]
        result = gpt_translate(txt) # 변수 txt값을 함수 gpt_translate의 인자로 전달하여 영어 -> 한글로 번역된 결과값을 변수 result에 할당  
        st.info(result) # 함수 st.info 사용해서 영어 -> 한글로 번역된 결과 화면에 출력(데이터 시각화)
    else:
        st.info('API 키를 넣으세요')
    st.markdown('---')

    st.subheader("파파고 번역 결과")
    st.text("https://papago.naver.com/")
    if st.session_state["PAPAGO_ID"] and st.session_state["PAPAGO_PW"] and txt:
        result = papago_translate(txt, st.session_state["PAPAGO_ID"], st.session_state["PAPAGO_PW"])
        st.info(result)
    else:
        st.info('파파고 API ID, PW를 넣으세요')
    st.markdown('---')

    st.subheader("Deepl 번역 결과")
    st.text("https://www.deepl.com/translator")
    if st.session_state["DeeplAPI"] and txt:
        result = deepl_translate(txt, st.session_state["DeeplAPI"])
        st.info(result)
    else:
        st.info('API 키를 넣으세요')

    st.subheader("구글 번역 결과")
    st.text("https://translate.google.co.kr/")
    if txt:
        result = google_trans(txt)
        st.info(result)
    else:
        st.info("API키가 필요 없습니다")
    st.markdown('---')

if __name__=="__main__":
    main()
