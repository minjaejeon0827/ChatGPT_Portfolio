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
# streamlit run test_generate_ads.py

##### 패키지 불러오기 #####
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
    # 패키지 streamlit 함수 set_page_config 사용해서 페이지 제목(page_title="광고 문구 생성 프로그램") 생성
    st.set_page_config(page_title="광고 문구 생성 프로그램")
    # 사이드바 생성 (처음에 OpenAI API 키 입력받는 공간이 필요해서 생성)
    # 파이썬 with문 
    # 참고 URL - https://docs.python.org/ko/3/reference/compound_stmts.html#index-16
    # 참고 2 URL - https://velog.io/@hyungraelee/Python-with
    with st.sidebar:
        # 아래는 사이드바 안에 위치하는 기능 이다.
        # OpenAI API 키 입력받기
        # 패키지 streamlit 함수 text_input 사용해서 text input을 받는 element를 생성했고 
        # type='password' 사용하여 여기에 어떤 text input을 넣어도 text가 노출되지 않도록 text input 화면 생성
        # input 받은 text를 변수 open_apikey에 저장
        open_apikey = st.text_input(label='OpenAI API 키', placeholder='Enter Your API Key', value='', type='password')
        # 입력받은 API 키 표시
        # input 받은 text가 존재할 경우 if문 실행 
        # input 안 받으면 아무 값이 저장이 안 돼서 if문 동작 안 함.
        if open_apikey:
            openai.api_key = open_apikey   # openai.api_key에 입력받은 open_apikey값을 저장 (이렇게 처음에 API키 지정 한번 해 놓으면 OpenAI의 패키지를 사용하는 코드 안에서는 더이상 따로 API 입력할 필요 없음.) 
        st.markdown('---')   # 구분선 추가('---') - 혹시라도 밑에 다른 엘리멘트들을 추가할 때를 대비해서 구현함.

    # 메인공간
    st.header("🎸광고 문구 생성 프로그램") # 함수 st.header 사용해서 프로그램 제목 "🎸광고 문구 생성 프로그램" 입력(이모지 🎸추가 가능)
    st.markdown('---')   # 구분선 추가('---')

    # 세로로 공간 나누기
    # 웹브라우저 화면 우측 메인공간 2등분해서 작성 및 각각의 2등분한 위치에 엘리먼트들을 작성 가능 
    # 메인공간 2등분한 각각의 공간 이름을 왼쪽공간 col1, 오른쪽공간 col2로 지정 
    col1, col2 = st.columns(2)

    with col1:  # 왼쪽공간 col1에 name, strength, keyword 작성(추가) -> 웹브라우저 화면에 데이터 시각화
        # 패키지 streamlit 함수 text_input 사용해서 text input을 받는 element를 생성했고
        # input 받은 text를 변수 name, strength, keyword에 저장 
        name = st.text_input("제품명", placeholder=" ")
        strength = st.text_input("제품 특징", placeholder=" ")
        keyword = st.text_input("필수 포함 키워드", placeholder=" ")
    with col2:  # 오른쪽공간 col2에 com_name, tone_manner, value 작성(추가) -> 웹브라우저 화면에 데이터 시각화
        # 패키지 streamlit 함수 text_input 사용해서 text input을 받는 element를 생성했고
        # input 받은 text를 변수 com_name, tone_manner, value에 저장 
        # 속성 placeholder 사용하여 해당 placeholder 속성에 문자열 입력 후
        # 프로그램 실행시 -> 웹브라우저 화면에서 실행된 프로그램 화면에서 사용자가 텍스트를 입력하기 전에 해당 공간에는 어떤 텍스트를 입력해야 되는지 예시글을 옅은 글씨로 표시 가능
        com_name = st.text_input("브랜드 명", placeholder="Apple, 올리브영...")
        tone_manner = st.text_input("톤엔 메너", placeholder="발랄하게, 유머러스하게, 감성적으로...")
        value = st.text_input("브랜드 핵심 가치", placeholder="필요 시 입력")

    if st.button("광고 문구 생성"):   # "광고 문구 생성" 버튼 생성 및 해당 버튼 Click 이벤트 발생시 if문 실행 
        prompt = f'''
        아래 내용을 참고해서 1~2줄짜리 광고 문구 5개 작성해줘
        - 제품명: {name}
        - 브렌드 명: {com_name}
        - 브렌드 핵심 가치: {value}
        - 제품 특징: {strength}
        - 톤엔 매너: {tone_manner}
        - 필수 포함 키워드: {keyword}
        '''
        # 변수 prompt는 앞서 구현한 기능 구현 함수 askGpt에 input(파라미터)으로 들어감.
        st.info(askGpt(prompt))   # 함수 askGpt 통해서 리턴 받은 ChatGPT 답변을 st.info 통해 화면에 예쁜 네모박스로 디스플레이(출력)함. 

if __name__=='__main__':
    main()