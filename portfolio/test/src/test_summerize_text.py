# *** 파이썬 설치 시 주의사항 ***
# 꼭 파이썬 설치 시 3.11 버전 설치 필수! (3.12 버전에서 openai 패키지와 충돌하는 현상 발생.)
# 만약 파이썬 3.12 버전 설치 진행시 가상환경에 아래의 패키지 먼저 설치 필수!
# pip install aiottp==3.9.0b0

# 가상환경 폴더 "portfolio_env" 생성 터미널 명령어
# python -m venv portfolio_env

# 가상환경 폴더 "portfolio_env" 활성화 터미널 명령어
# portfolio_env\Scripts\activate.bat

# 비쥬얼스튜디오 코드(VSCode)
# streamlit 터미널 실행 명령어
# streamlit run test_summerize_text.py

##### 패키지 불러오기 #####
##### (프로그램 개발할 때 패키지 정보 불러와서 정리) #####
##### (때에 따라서는 프로그램에 필요한 다른 API들의 키나 토큰들을 정리) #####
# Streamlit 패키지 추가
import streamlit as st   # streamlit 패키지 -> Elias(앨리아스) st 로 불러오기 
# OpenAI 패키지 추가
import openai   # openai 패키지 불러오기

##### 기능 구현 함수 #####
##### 프로그램 내에서 ChatGPT한테 물어보거나 번역을 지시하거나 하는 
##### 그러한 기능들을 깔끔하게 함수화해서 정리  
# 함수 - 내용 요약
def askGpt(prompt): # ChatGPT한테 질문을 하게 될 프롬프트를 함수 askGpt에 input으로 받기 
    messages_prompt = [{"role": "system", "content": prompt}]   # ChatGPT API에서 요구하는 프롬프트 input 양식으로 변경 및 변경한 input 양식을 변수 messages_prompt에 저장 
    # openai.ChatCompletion.create 함수 파라미터 "messages"에 messages_prompt 저장 
    # 함수 openai.ChatCompletion.create 호출 결과 최종적으로 ChatGPT API를 통해서 받은 응답을
    # response라는 변수에 저장 
    response = openai.ChatCompletion.create(model='gpt-3.5-turbo', messages=messages_prompt)
    # response에서 ChatGPT의 응답 부분만 발췌를 해서(response["choices"][0]["message"]["content"])
    # 변수 gptResponse에 저장 
    gptResponse = response["choices"][0]["message"]["content"]
    return gptResponse   # 변수 gptResponse 리턴 

##### 메인 함수 #####
##### 패키지 streamlit을 활용해서 프로그램의 UI를 작성하고 
##### 기능 구현 함수 "askGpt" 호출해서 프로그램이 동작하게 하는 메인 코드가 작성된 함수 
def main():
    # 패키지 streamlit 함수 set_page_config 사용해서 페이지 제목(page_title="요약 프로그램") 생성
    st.set_page_config(page_title="요약 프로그램")
    # 사이드바 생성 (처음에 Open AI API 키 입력받는 공간이 필요해서 생성)
    # 파이썬 with문 
    # 참고 URL - https://docs.python.org/ko/3/reference/compound_stmts.html#index-16
    # 참고 2 URL - https://velog.io/@hyungraelee/Python-with
    with st.sidebar:
        # 아래는 사이드바 안에 위치하는 기능 이다.
        # Open AI API 키 입력받기
        # 패키지 streamlit 함수 text_input 사용해서 text input을 받는 element를 생성했고
        # type='password' 사용하여 여기에 어떤 text input을 넣어도 text가 노출되지 않도록 text input 화면 생성
        # input 받은 text를 변수 open_apikey에 저장 
        open_apikey = st.text_input(label='OPENAI API 키', placeholder='Enter Your API Key', value='',type='password')    
        # 입력받은 API 키 표시
        # input 받은 text가 존재할 경우 if문 실행 
        # input 안받으면 아무 값이 저장이 안 돼서 if문 동작 안 함.
        if open_apikey:
            openai.api_key = open_apikey   # openai.api_key에 입력받은 open_apikey값을 저장 (이렇게 처음에 API키 지정 한번 해 놓으면 OpenAI의 패키지를 사용하는 코드 안에서는 더이상 따로 API 입력할 필요 없음.)
        st.markdown('---')   # 구분선 추가(--------) - 혹시라도 밑에 다른 엘리멘트들을 추가할 때를 대비해서 구현함.

    #메인공간
    st.header("📃요약 프로그램") # 함수 st.header 사용해서 프로그램 제목 "📃요약 프로그램" 입력(이모지 📃추가 가능)
    st.markdown('---')   # 구분선 추가(--------) 
    
    # text_area 기능 - text input 받기 가능 / 사용자가 직접 text_area 높이 조절 가능 
    text = st.text_area("요약 할 글을 입력하세요") # text_area 엘러먼트 사용해서 Text를 input 받는 엘리먼트 생성 
    if st.button("요약"): # 버튼 "요약" 생성 및 버튼 "요약" Click 이벤트 발생시 if문 실행 
        # 시스템 프롬프트(**Instructions** : ~~~ - ChatGPT에게 요약을 최대한 잘 해달라고 요청하는 시스템 프롬프트를 의미. 일종의 프롬프트 엔지니어링 과정이다.)와 요약을 원하는 글 "text"이 합쳐져서 변수 prompt에 저장 
        # 시스템 프롬프트에서 한국어로 요약 해달라고 2번 강조해야 한국어 요약이 가능함.
        # that summarizes text into **Korean language**.
        # the **text** sentences in **Korean language**
        # 글머리 기호 형식을 사용 설정함
        # - Use the format of a bullet point.
        prompt = f'''
        **Instructions** :
    - You are an expert assistant that summarizes text into **Korean language**.
    - Your task is to summarize the **text** sentences in **Korean language**.
    - Your summaries should include the following :
        - Omit duplicate content, but increase the summary weight of duplicate content.
        - Summarize by emphasizing concepts and arguments rather than case evidence.
        - Summarize in 3 lines.
        - Use the format of a bullet point.
    -text : {text}
    '''
        # 변수 prompt는 앞서 구현한 기능 구현 함수 askGpt에 input(파라미터)으로 들어감.
        st.info(askGpt(prompt))   # 함수 askGpt 통해서 리턴 받은 ChatGPT 답변을 st.info 통해 화면에 예쁜 네모박스로 디스플레이(출력)함. 

if __name__=="__main__":
    main()