"""
*** 참고 ***
*** ChatGPT 문서 ***
* ChatGPT 텍스트 응답 메시지
참고 URL - https://github.com/openai/openai-python

*** 파이썬 문서 ***
* with 문
참고 URL - https://docs.python.org/ko/3/reference/compound_stmts.html#index-16
참고 2 URL - https://velog.io/@hyungraelee/Python-with

* urllib
참고 URL - https://docs.python.org/ko/3.13/library/urllib.html
참고 2 URL - https://docs.python.org/ko/3.13/library/urllib.request.html#module-urllib.request
참고 3 URL - https://docs.python.org/ko/3.13/library/urllib.request.html#legacy-interface

*** 기타 문서 ***
* 인스타그램 오픈 소스 패키지 instagrapi
참고 URL - https://github.com/adw0rd/instagrapi
참고 2 URL - https://github.com/subzeroid/instagrapi

* 구글 번역기 오픈 소스 패키지 googletrans
참고 URL - https://pypi.org/project/googletrans/
"""

# 비쥬얼스튜디오 코드(VSCode)
# streamlit 터미널 실행 명령어
# streamlit run instabot.py

##### 패키지 불러오기 #####
import streamlit as st   # streamlit -> Elias(앨리아스) st
import openai   # OpenAI (ChatGPT, DALLE2 사용 목적)
import urllib   # URL 처리

from googletrans import Translator   # 구글 번역기
from instagrapi import Client   # Instagram
from PIL import Image   # 이미지 처리

##### 기능 구현 함수 #####
def google_trans(prompt: str) -> str:
    """
    Description: 한글 -> 영어 번역 (DALLE2 이미지 생성 용도)

                 현재 DALLE2에서 한글 텍스트 사용시 이미지가 엉망진창으로 생성됨.
                 왜냐면 아직 한글에 대한 학습이 원활하지 않는 것으로 확인.
                 하여 한글 -> 영어 번역한 텍스트 사용해서 DALLE2 이미지 생성함.

    Parameters: prompt - 사용자 작성 내용 (주제, 분위기)

    Returns: result.text - 한글 -> 영어 번역 내용
    """

    google = Translator()
    result = google.translate(prompt, dest="en")   # 한글 -> 영어 번역 (dest="en") 참고: 영어 -> 한글 번역 (dest="ko")

    return result.text   # 한글 -> 영어 번역 내용 리턴

def upload_instagram(description: str) -> None:
    """
    Description: 인스타 사진 이미지 파일 및 포스팅 글 업로드

    Parameters: description - 인스타그램 포스팅 글

    Returns: 없음.
    """

    client = Client()
    client.login(st.session_state["instagram_ID"], st.session_state["instagram_Password"])   # 인스타그램 로그인 처리
    client.photo_upload("insta_image_resize.jpg" , description)   # 인스타그램 사진 이미지("insta_image_resize.jpg") 및 포스팅 글(description) 업로드

def get_descriptionFromGPT(topic: str, mood: str) -> str:
    """
    Description: ChatGPT 텍스트 응답 메시지 가져오기 (인스타그램 포스팅 글)

    Parameters: topic - 주제
                mood - 분위기

    Returns: msg - ChatGPT 텍스트 응답 메시지 (인스타그램 포스팅 글)
    """

    # f'''~~~~~''' - 시스템 프롬프트와 매개변수 topic, mood 합쳐서 구현.
    # 시스템 프롬프트 문자열
    # 1. 이모지 포함(Include emojis)
    # 2. 이목을 끌말한 내용으로 첫번째 caption 문장 작성 (The first caption sentence should hook the readers.)
    # 3. 모든 것은 한국어로 작성 (write all output in korean.)
    prompt = f'''
            Write me the Instagram post description or caption in just a few sentences for the post 
            -topic : {topic}
            -Mood : {mood}
            Format every new sentence with new lines so the text is more readable.
            Include emojis and the best Instagram hashtags for that post.
            The first caption sentence should hook the readers.
            write all output in korean.
            '''
    
    messages_prompt = [{"role": "system", "content": prompt}]
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages_prompt)

    msg = response["choices"][0]["message"]["content"]   # ChatGPT 텍스트 응답 메시지 msg 변수 저장
    return msg

def get_imageURLFromDALLE2(topic: str, mood: str) -> None:
    """
    Description: DALLE.2 이미지 생성 및 URL 주소 가져오기

    Parameters: topic - 주제
                mood - 분위기

    Returns: 없음.
    """

    # 한글 -> 영어 번역
    t_topic = google_trans(topic)   # 주제
    t_mood = google_trans(mood)     # 분위기
    

    # f'~~~~~' - 시스템 프롬프트와 매개변수 t_topic, t_mood 합쳐서 구현.
    # 시스템 프롬프트 문자열
    # 1. 해당 주제에 대해서 그림 그리기 (Draw picture about {t_topic})
    # 2. 그림의 분위기는 다음과 같다. (picture Mood is {t_mood}')
    image_prompt = f'Draw picture about {t_topic}. picture Mood is {t_mood}'
    print(image_prompt)

    response = openai.Image.create(prompt=image_prompt, n=1, size="512x512")   # 이미지 생성 및 response 변수 저장

    image_url = response['data'][0]['url']  # 이미지 URL 주소(response['data'][0]['url']) image_url 변수 저장
    urllib.request.urlretrieve(image_url, "insta_image.jpg")  # 해당 이미지 다운로드 및 "insta_image.jpg" 파일명 저장

##### 메인 함수 #####
def main() -> None:
    """
    Description: 메인 함수

    Parameters: 없음.

    Returns: 없음.
    """

    st.set_page_config(page_title="Instabot", page_icon="?")   # 프로그램 페이지 제목 설정 (page_title="Instabot")
    
    # session state 초기화 코드 - 프로그램에서 어떤 이벤트가 발생해도 정보를 잃지 않고 유지할 session_state 4가지 지정
    if "description" not in st.session_state:   # "description" - 인스타그램 포스팅 글
        st.session_state["description"] = ""

    if "flag" not in st.session_state:   # "flag" - 인스타그램 업로드 사진 이미지 생성 여부 확인
        # st.session_state["flag"] 변수 저장된 값 
        # True - 인스타그램에 업로드할 수 있는 후속 코드 진행 됨.(O)
        # False - 인스타그램에 업로드할 수 있는 후속 코드 진행 안 함.(X)
        st.session_state["flag"] = False

    if "instagram_ID" not in st.session_state:   # "instagram_ID" - 인스타그램 접속 아이디
        st.session_state["instagram_ID"] = ""

    if "instagram_Password" not in st.session_state:   # "instagram_Password" - 인스타그램 접속 비밀번호
        st.session_state["instagram_Password"] = ""

    st.header("인스타그램 포스팅 생성기")   # "인스타그램 포스팅 생성기" 프로그램 제목 화면 출력
    st.markdown('---')   # 구분선 추가('---')

    with st.expander("인스타그램 포스팅 생성기", expanded=True):   # 해당 프로그램 구성 설명 
        st.write(   # st.expander 엘리먼트 컨테이너 안에서 아래 텍스트 출력
        """     
        - 인스타그램 포스팅 생성 UI는 스트림릿을 활용하여 만들었습니다.
        - 이미지는 OpenAI Dall.e 2 활용하여 생성합니다. 
        - 포스팅 글은 OpenAI GPT 모델을 활용하여 생성합니다. 
        - 자동 포스팅은 instagram API 활용합니다.
        """
        )

        st.markdown('')   # st.expander 엘리먼트 컨테이너 안에서 공백 추가('')

    with st.sidebar:   # 파이썬 with 문 사용 및 좌측 사이드바 생성

        # Open AI API 키 입력 받기
        # st.text_input 사용해서 OpenAI API 키 입력 받기
        open_apikey = st.text_input(label='OPENAI API 키', placeholder='Enter Your API Key', value='', type="password")

        # 입력받은 API 키 표시
        # 사용자로 부터 입력받은 OPENAI API 키가 존재하는 경우
        if open_apikey:
            # 입력받은 OpenAI API 키(open_apikey)를 변수 openai.api_key에 저장 
            openai.api_key = open_apikey    
        
        st.markdown('---')   # markdown 사용해서 구분선 생성(st.markdown('---'))

    # st.text_input 앨리먼트 사용해서 생성하고자 하는 인스타그램 포스팅의 주제와 분위기를
    # 따로따로 입력 받아서 각각 변수 topic과 mood에 저장함. 
    topic = st.text_input(label="주제", placeholder="축구, 인공지능...")
    mood = st.text_input(label="분위기 (e.g. 재미있는, 진지한, 우울한)", placeholder="재미있는")

    # st.button 앨리먼트 사용해서 인스타그램 포스팅을 진행하기 위한 생성 버튼 만들기
    # 해당 인스타그램 포스팅 버튼 "생성"이 클릭되고
    # st.session_state["flag"] 값이 false인 경우 (and not st.session_state["flag"])
    # 아래 if절 로직 실행 
    # 주의사항
    # Streamlit 같은 경우에는 새로운 텍스트 input이나 button을 눌렀을 때, 다시 처음부터 코드가 실행된다. 
    # 만약 if 조건절에 st.session_state["flag"] 값이 false인 경우
    # 의미하는 코드(and not st.session_state["flag"])를 넣지 않으면 
    # 이미 포스팅을 다 생성하고 인스타그램 업로드를 하기 위해
    # id와 password를 입력했을 때, 다시 한번 처음부터 코드가 실행되면서
    # 인스타그램 포스팅을 다시 생산하게 된다.
    # 그러면 좀전에 생성했던 이미지와 인스타그램 포스팅 글(description)과는
    # 다른 내용의 포스팅이 이미지로 생성되서 업데이트 되는 오류가 발생한다.
    # 하여 이렇게 포스팅 생성이 중복으로 일어나는 것을 막기 위해
    # if절에 조건절로 st.session_state["flag"] 값이 false인 경우 (and not st.session_state["flag"])를 추가한다.
    if st.button(label="생성",type="secondary") and not st.session_state["flag"]:
        # 인스타그램 포스팅 생성 
        # '생성 중' 대기 처리 화면 출력 
        # 인스타그램 포스팅 생성 완료되면 '생성 중' 대기 처리 화면 종료 
        with st.spinner('생성 중'):
            st.session_state["description"] = get_descriptionFromGPT(topic,mood)
            get_imageURLFromDALLE2(topic,mood)
            # 인스타그램 포스팅 생성 완료되면 st.session_state["flag"] 값을 True 변경
            # 해당 값이 True 변경되면 그 다음에 인스타그램에 업로드하는 버튼을 눌러도 
            # 위의 if 절 안으로 들어와서 인스타그램 포스팅 생성 안하므로 포스팅이 중복해서 생성 안 함.
            st.session_state["flag"] = True

    # 인스타그램 포스팅 생성 완료된 경우 (st.session_state["flag"] = True)
    if st.session_state["flag"]:
        # 함수 get_imageURLFromDALLE2 호출 결과 생성한 이미지 'insta_image.jpg' 불러오기 
        image = Image.open('insta_image.jpg')  
        st.image(image) # 해당 포스팅 생성 완료된 이미지 'insta_image.jpg' 화면 출력 

        # st.markdown(st.session_state["description"])
        # st.text_area 앨리먼트의 속성 value에 위에서 포스팅 생성 완료한 인스타그램 포스팅 글(st.session_state["description"],) 할당
        # st.text_area 앨리먼트의 호출 결과값을 변수 txt에 저장 
        # 변수 txt에 저장한 이유는 ChatGPT에 저장한 포스팅 생성 완료한 인스타그램 포스팅 글(st.session_state["description"])이 마음이 안 들 수도 있다.
        # 인스타그램 포스팅 글(st.session_state["description"])이 마음에 안 들면 st.text_area 앨리먼트 안에서 수정하고 
        # 수정된 결과를 다시 한번 변수 txt에 저장해서 그것을 다시 인스타그램 포스팅 글(st.session_state["description"])에 다시 재할당(덮어쓰기) 처리한다.
        # TODO : 오류 메시지 "streamlit.errors.StreamlitAPIException: Invalid height 50px for st.text_area - must be at least 68 pixels." 출력으로 인하여
        #        아래 st.text_area의 속성 height 값을 (기존) 50 -> (변경) 68 처리함 (2024.01.03 jbh)
        # txt = st.text_area(label = "Edit Description", value = st.session_state["description"], height=50)
        txt = st.text_area(label = "Edit Description", value = st.session_state["description"], height=68)
        st.session_state["description"] = txt

        st.markdown('인스타그램 ID/PW')
        # st.text_input 앨리먼트 사용해서 인스타그램 ID 입력 받기
        st.session_state["instagram_ID"] = st.text_input(label='ID', placeholder='Enter Your ID', value='')
        # st.text_input 앨리먼트 사용해서 인스타그램 비밀번호 입력 받기 
        st.session_state["instagram_Password"] = st.text_input(label='Password', type='password', placeholder='Enter Your Password', value='')

        # '업로드' 버튼 클릭하는 경우
        if st.button(label='업로드'):
            # 인스타그램에 이미지(사진) 및 포스팅 글을 '업로드' 시작
            # 인스타그램에 이미지(사진)를 업로드 하려면 이미지(사진)가 정사각형 모양이어야만 한다.
            # 앞서 생성한 인스타 이미지 파일 "insta_image.jpg" 불러오기 
            image = Image.open("insta_image.jpg")
            image_convert = image.convert("RGB")
            # 불러온 이미지 파일 "insta_image.jpg" 사이즈 "1080 X 1080" 변환하기
            new_image = image_convert.resize((1080, 1080))
            # 사이즈 변환한 이미지 파일을 "insta_image_resize.jpg"로 저장하기  
            new_image.save("insta_image_resize.jpg")
            # 함수 upload_instagram 호출하여 인스타 사진 이미지 파일 및 포스팅 글 업로드 처리
            upload_instagram(st.session_state["description"])
            # st.session_state["flag"]에 값 False 할당하여
            # 새로운 인스타그램 포스팅을 생성할 수 있도록 셋팅 변경 
            st.session_state["flag"] = False

if __name__=="__main__":
    main()   # 메인 함수 실행