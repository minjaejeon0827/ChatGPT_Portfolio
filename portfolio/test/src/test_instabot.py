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
# streamlit run test_instabot.py

##### 패키지 불러오기 #####
# streamlit 패키지 추가 
import streamlit as st
# OpenAI 패키지 추가 (ChatGPT, DALLE2 사용하기 위해서)
import openai
# 인스타그램 패키지 추가
from instagrapi import Client
# 이미지 처리
from PIL import Image
import urllib

# 구글 번역기 파이썬 오픈소스 패키지 googletrans
# 참고 URL - https://pypi.org/project/googletrans/

# 구글 번역기 파이썬 오픈소스 패키지 googletrans
# 터미널 설치 명령어
# pip install googletrans==3.1.0a0
# 구글 번역기 파이썬 오픈소스 패키지 googletrans 의 경우 따로 API 키 발급이 필요 없다.
# 구글 번역
from googletrans import Translator

##### 기능 구현 함수 #####
# 영어로 번역
# 해당 함수 google_trans 사용하는 이유?
# 현재 DALLE2에서 st.text_input 함수 사용해서 사용자로 부터 입력받는 텍스트가 한글인 경우 
# 이미지 생성이 엉망진창으로 생성된다.
# 왜냐면 DALLE2에서는 아직 한글에 대한 학습이 되지 않기 때문이다.
# DALLE2로 이미지를 생성하려면 사용자로 부터 입력받는 텍스트가 영어여야 한다.
# 하여 인스타로 이미지를 업로드하기 위해서 
# 주제나 분위기를 사용자가 넣을 때는 한글로 입력하고 
# 이미지 업로드시에는 해당 한글을 영어로 번역을 필수적으로 해야하므로
# 해당 google_trans 함수를 사용해야 한다. 
def google_trans(messages):
    google = Translator()   # Translator 클래스 인스턴스 google 생성
    # 함수 google.translate 사용해서 번역하고자 하는 메시지(messages)를
    # 해당 함수의 첫번째 파라미터로 전달하고
    # 번역을 하고 싶은 언어를 해당 함수의 두번째 파라미터로 전달 
    # 영어 -> 한글로 번역하고자 하면 dest="ko" 라고 두번째 파라미터로 전달한다.
    # 한글 -> 영어로 번역하고자 하면 dest="en" 라고 두번째 파라미터로 전달한다.
    result = google.translate(messages, dest="en")

    # 영어 -> 한글로 번역한 결과 result.text 리턴
    return result.text

# 인스타 사진 이미지 파일 및 포스팅 글 업로드
def uploadinstagram(description):
    cl = Client() # Client 클래스 객체 cl 생성 
    # 인스타그램에 로그인 처리 
    cl.login(st.session_state["instagram_ID"], st.session_state["instagram_Password"])
    # 인스타그램에 사진 이미지("instaimg_resize.jpg") 및 텍스트(description) 업로드
    # 해당 텍스트(description)는 사용자로 부터 질문받은 ChatGPT가 답변하는 
    # 인스타그램 포스팅 글을 매개변수 description로 인자를 전달 받아서 
    # 아래 함수 cl.photo_upload에 인자로 전달해준다.
    # 사진 이미지 파일 이름은 "instaimg_resize.jpg" 고정 
    cl.photo_upload("instaimg_resize.jpg" , description)

# ChatGPT에게 질문/답변받기
# ChatGPT에게 인스타그램 포스팅 글을 작성 요청하는 함수이다.
# 사용자가 입력한 주제와 분위기는 매개변수 topic, mood로 인자 전달 
def getdescriptionFromGPT(topic, mood):
    # f'''~~~~~''' 안에는 시스템 프롬프트와 매개변수 topic, mood가 합쳐서 구현한다.
    # 시스템 프롬프트 안에는 
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
write all output in korean.'''
    messages_prompt = [{"role": "system", "content": prompt}]
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages_prompt)

    system_message = response["choices"][0]["message"]
    return system_message["content"]

# DALLE.2에게 질문/그림 URL 받기
# DALLE.2로 그림 생성하기 
def getImageURLFromDALLE(topic,mood):
    # 사용자가 입력하는 주제와 분위기를 매개변수 topic,mood로 인자를 전달받아서
    # 매개변수 topic,mood 안에 할당된 문자열을 각각 영어로 번역해서
    # 영어로 번역된 문자열을 변수 t_topic, t_mood에 각각 저장
    t_topic = google_trans(topic)   # 함수 google_trans 호출시 변수 topic을 인자로 전달
    t_mood = google_trans(mood)     # 함수 google_trans 호출시 변수 mood를 인자로 전달
    
    # 해당 주제에 대해서 그림을 그려주고 (Draw picture about {t_topic})
    # 그림의 분위기는 다음과 같다. (picture Mood is {t_mood}')
    # 고 지정하는 프롬프트 문자열을 변수 prompt_에 저장 
    prompt_ = f'Draw picture about {t_topic}. picture Mood is {t_mood}'
    print(prompt_)
    # 프롬프트 문자열이 저장된 변수 prompt_를 
    # 함수 openai.Image.create 에 전달하여 이미지 생성
    # 생성한 이미지에 대한 정보를 변수 response에 저장
    response = openai.Image.create(prompt=prompt_,n=1,size="512x512")

    # 이미지를 다운받을 수 있는 이미지 URL 주소(response['data'][0]['url'])를
    # 변수 image_url에 저장 
    image_url = response['data'][0]['url']
    # 함수 urllib.request.urlretrieve 사용해서 
    # 해당 이미지 다운받을 수 있는 URL 주소에 있는 사진을 다운받아서
    # 파일명 "instaimg.jpg"으로 저장
    urllib.request.urlretrieve(image_url, "instaimg.jpg")

##### 메인 함수 #####
def main():

    # 기본 설정
    # 페이지 제목(page_title="Instabot") 설정 
    st.set_page_config(page_title="Instabot", page_icon="?")
    
    # session state 초기화
    # 프로그램에서 어떤 이벤트가 발생해도 정보를 잃지 않고 유지할 4가지 session_state 지정하기 
    # session_state 초기화 코드 
    # "description" - 인스타그램에 업로드할 포스팅 글 의미
    if "description" not in st.session_state:
        st.session_state["description"] = ""

    # "flag" - 인스타그램에 업로드하기 위한 사진 이미지가 생성되었는지를 확인하는 변수 의미 
    if "flag" not in st.session_state:
        # 변수 st.session_state["flag"]에 저장된 값이 True면 인스타그램에 업로드할 수 있는 후속 코드가 진행됨(O).
        # 변수 st.session_state["flag"]에 저장된 값이 False면 인스타그램에 업로드할 수 있는 후속 코드가 진행 안함(X).
        st.session_state["flag"] = False

    # "instagram_ID" - 접속하려고 하는 인스타그램 아이디를 의미
    if "instagram_ID" not in st.session_state:
        st.session_state["instagram_ID"] = ""
    # "instagram_Password" - 접속하려고 하는 인스타그램 비밀번호를 의미
    if "instagram_Password" not in st.session_state:
        st.session_state["instagram_Password"] = ""

    # 제목
    # st.header 사용해서 "인스타그램 포스팅 생성기" 텍스트 화면 출력
    st.header('인스타그램 포스팅 생성기')
    # 구분선
    st.markdown('---')   # markdown 사용해서 구분선 생성(st.markdown('---'))

    # 기본 설명
    # st.expander 엘리먼트 사용해서 해당 프로그램의 구성에 대해 설명 진행 
    with st.expander("인스타그램 포스팅 생성기", expanded=True):
        # 아래 st.write 함수는 st.expander 엘리먼트 컨테이너 안에서 작성되는 효과가 있다.
        st.write(
        """     
        - 인스타그램 포스팅 생성 UI는 스트림릿을 활용하여 만들었습니다.
        - 이미지는 OpenAI의 Dall.e 2를 활용하여 생성합니다. 
        - 포스팅 글은 OpenAI의 GPT 모델을 활용하여 생성합니다. 
        - 자동 포스팅은 instagram API를 활용합니다.
        """
        )

        # 아래 st.markdown 함수는 st.expander 엘리먼트 컨테이너 안에서 작성되는 효과가 있다.
        st.markdown("")   # markdown 사용해서 공백 생성(st.markdown(""))

    # 사이드바 생성
    with st.sidebar:

        # Open AI API 키 입력 받기
        # st.text_input 사용해서 OpenAI API 키 입력 받기
        open_apikey = st.text_input(label='OPENAI API 키', 
                                    placeholder='Enter Your API Key',
                                    value='',
                                    type="password")

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
            st.session_state["description"] = getdescriptionFromGPT(topic,mood)
            getImageURLFromDALLE(topic,mood)
            # 인스타그램 포스팅 생성 완료되면 st.session_state["flag"] 값을 True 변경
            # 해당 값이 True 변경되면 그 다음에 인스타그램에 업로드하는 버튼을 눌러도 
            # 위의 if 절 안으로 들어와서 인스타그램 포스팅 생성 안하므로 포스팅이 중복해서 생성 안 함.
            st.session_state["flag"] = True

    # 인스타그램 포스팅 생성 완료된 경우 (st.session_state["flag"] = True)
    if st.session_state["flag"]:
        # 함수 getImageURLFromDALLE 호출 결과 생성한 이미지 'instaimg.jpg' 불러오기 
        image = Image.open('instaimg.jpg')  
        st.image(image) # 해당 포스팅 생성 완료된 이미지 'instaimg.jpg' 화면 출력 

        # st.markdown(st.session_state["description"])
        # st.text_area 앨리먼트의 속성 value에 위에서 포스팅 생성 완료한 인스타그램 포스팅 글(st.session_state["description"],) 할당
        # st.text_area 앨리먼트의 호출 결과값을 변수 txt에 저장 
        # 변수 txt에 저장한 이유는 ChatGPT에 저장한 포스팅 생성 완료한 인스타그램 포스팅 글(st.session_state["description"])이 마음이 안 들 수도 있다.
        # 인스타그램 포스팅 글(st.session_state["description"])이 마음에 안 들면 st.text_area 앨리먼트 안에서 수정하고 
        # 수정된 결과를 다시 한번 변수 txt에 저장해서 그것을 다시 인스타그램 포스팅 글(st.session_state["description"])에 다시 재할당(덮어쓰기) 처리한다.
        # TODO : 오류 메시지 "streamlit.errors.StreamlitAPIException: Invalid height 50px for st.text_area - must be at least 68 pixels." 출력으로 인하여
        #        아래 st.text_area의 속성 height 값을 (기존) 50 -> (변경) 68 처리함 (2024.01.03 minjae)
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
            # 앞서 생성한 인스타 이미지 파일 "instaimg.jpg" 불러오기 
            image = Image.open("instaimg.jpg")
            image_convert = image.convert("RGB")
            # 불러온 이미지 파일 "instaimg.jpg" 사이즈 "1080 X 1080" 변환하기
            new_image = image_convert.resize((1080, 1080))
            # 사이즈 변환한 이미지 파일을 "instaimg_resize.jpg"로 저장하기  
            new_image.save("instaimg_resize.jpg")
            # 함수 uploadinstagram 호출하여 인스타 사진 이미지 파일 및 포스팅 글 업로드 처리
            uploadinstagram(st.session_state["description"])
            # st.session_state["flag"]에 값 False 할당하여
            # 새로운 인스타그램 포스팅을 생성할 수 있도록 셋팅 변경 
            st.session_state["flag"] = False

if __name__=="__main__":
    main()