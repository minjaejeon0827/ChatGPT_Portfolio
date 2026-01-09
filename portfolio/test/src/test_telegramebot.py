# *** 파이썬 설치 시 주의사항 ***
# 꼭 파이썬 설치 시 3.11 버전 설치 필수! (3.12 버전에서 openai 패키지와 충돌하는 현상 발생.)
# 만약 파이썬 3.12 버전 설치 진행시 가상환경에 아래의 패키지 먼저 설치 필수!
# pip install aiottp==3.9.0b0

# 가상환경 폴더 "portfolio_env" 생성 터미널 명령어
# python -m venv portfolio_env

# 가상환경 폴더 "portfolio_env" 활성화 터미널 명령어
# portfolio_env\Scripts\activate.bat

# 주의사항 
# 비동기(async - await) 웹서버 생성하는 유비콘 패키지 "uvicorn[standard]"를 사용하는 파이썬 파일의 경우 
# 일반 파이썬 파일을 터미널에서 실행하는 명령어(python test_telegramebot.py)를 
# 그대로 쓰면 파일 안에 있는 FastAPI 서버(FastAPI 클래스 객체 app)가 생성 불가하다.
# 하여 비동기(async - await) 웹서버 생성하는 유비콘 패키지 "uvicorn[standard]"를 사용하는 파이썬 파일은
# 아래와 같은 명령어를 입력 해야만 해당 파일 안에 있는 FastAPI 서버(FastAPI 클래스 객체 app)가 생성된다.
# uvicorn test_telegramebot:app --reload

##### 패키지 불러오기 #####
import urllib3   # HTTP 통신을 하기위해 파이썬 기본 내장 패키지(함수) urllib3 불러오기 - 아마존 웹서비스(AWS)에서 사용하기 용이하다.
import json   # 텔레그램 서버로부터 받은 json 데이터 처리하기 위해 패키지 json 불러오기 
import openai  # OPENAI 패키지 openai 불러오기 
# FastAPI 패키지 "fastapi" 불러오기
# Request 패키지 불러오기 
from fastapi import Request, FastAPI

# OpenAI API KEY
# 테스트용 텔레그램 챗봇 채팅방에서 
# ChatGPT와 통신하기 위해 OpenAI API 키 입력
API_KEY = "API_key"
openai.api_key = API_KEY

# Telegram Token
# 테스트용 텔레그램 챗봇 채팅방에서 
# HTTP 통신하기 위한 고유 토큰 번호 문자열을 변수 BOT_TOKEN에 할당 
# BOT_TOKEN = 'Token'
# BOT_TOKEN = "Token"
BOT_TOKEN = '7717605195:AAHJGNKRR_aK_dG0HELQUBu1WeEsclERRb0'

###### FastAPI 웹서버 생성 단계 ######

app = FastAPI()   # FastAPI 클래스 객체 app 생성 

# 위에서 생성한 객체 app 이라는 웹서버에 
# HTTP 통신 get() 메소드에 인자 "/" 전달 후 
# -> get() 메소드 호출시 메인 주소("/")로 접속 진행
# -> root 함수 실행 
@app.get("/")
async def root():
    # 크롬(Chrome) 웹브라우저 상에서 
    # URL 주소 "http://127.0.0.1:8000/"로 접속을 했을 때, 
    # 웹브라우저상에서 아래와 같은 메시지({"message": "TelegramChatbot"}) 출력
    return {"message": "TelegramChatbot"}

# 위에서 생성한 객체 app 이라는 웹서버에 
# HTTP 통신 post() 메소드에 인자 "/chat" 전달 후 
# -> post() 메소드 호출시 메인 주소 하위 주소("/chat")로 접속 진행
# -> chat 함수 실행 -> 텔레그램 웹훅과 연결 진행
# 주의사항 - 일반 HTTP 통신 GET 방식으로 구글 크롬 웹브라우저 URL 접속하면 
#           (URL 주소 "http://127.0.0.1:8000/chat) 아래와 같은 오류 메시지 출력
#           "405 Method Not Allowed"
#           왜냐면 post() 메소드로 호출하기 때문에 
#           구글 크롬 웹브라우저 URL 접속시에는 GET 방식이 아닌
#           POST 방식으로 접근해야 하기 때문이다.
#           하여 해당 오류를 해결하려면 ngrok와 텔레그램 API를 활용해서
#           아래 post() 메소드로 정보(데이터)를 주고 받을 수 있도록 해야한다.
@app.post("/chat")
# 텔레그램 채팅방에 사용자가 채팅을 새로 입력했을 때
# 챗봇의 모든 기능을 실행할 수 있는 함수 chat
# 사용자가 채팅을 새로 입력했을 때 새로운 입력에 대한 정보를
# 매개변수 request로 인자를 전달 받는다.
async def chat(request: Request):
    # 텔레그램 채팅방에서 사용자가 채팅 입력 
    # -> 해당 채팅에 대한 정보가 텔레그램 API webhook 메소드 사용해서 
    # 텔레그램 서버 -> ngrok 프로그램을 지나서 -> 해당 FastAPI 웹서버 URL 주소 "/chat"로 넘어오고 ->
    # 함수 chat 실행 -> print 함수 호출 -> 텔레그램 채팅 정보가 터미널창에 출력
    # 쉽게 말해서 텔레그램 채팅방에 채팅이 입력될 때마다
    # 해당 chat 함수 실행되서 
    # 텔레그램 챗봇의 모든 기능 실행할 수 있는 메인함수 chatBot이 실행된다.
    # 메인함수 chatBot이 실행될 때는 텔레그램 채팅방에
    # 방금 전에 사용자가 입력한 채팅의 정보가 넘어오면서 메인함수 chatBot이 실행된다.

    # 텔레그램 채팅에서 날라온 채팅 정보를 json 데이터 형태로 정리(request.json())해서 변수 telegramrequest에 저장  
    telegramrequest = await request.json()
    # 텔레그램 챗봇의 모든 기능 실행할 수 있는 메인함수 chatBot에
    # 위의 변수 telegramrequest를 인자로 전달 
    chatBot(telegramrequest)   
    return {"message": "TelegramChatbot/chat"}

###### 기능 함수 구현 단계 ######

# 메세지 전송
# 텔레그램 채팅방에 ChatGPT의 답변을 채팅 메시지로 보내기
# ChatGPT의 답변을 아래 sendMessage 함수를 호출하여
# 텔레그램 채팅방에 채팅 메시지 보내는 것도 가능함.
def sendMessage(chat_id, text,msg_id):
    # 변수 data에 채팅방에 전송할 채팅 메시지가 담긴
    # JSON 포맷 데이터 저장 
    # 'chat_id' - 텍스트 전송할 채팅방 아이디 
    # 'text' - 채팅방으로 전송할 채팅 메시지 내용
    # 'reply_to_message_id' - 사용자가 보낸 메세지 아이디
    data = {
        'chat_id': chat_id,
        'text': text,
        'reply_to_message_id': msg_id
    }
    # 라이브러리(패키지) urllib3의 PoolManager 클래스 객체 http 생성
    http = urllib3.PoolManager()
    # 텔레그램 채팅방에 채팅 메시지 보내기 위해
    # 텔레그램 API의 sendMessage 메소드 활용한 HTTP 통신 요청 문자열 사용
    # "https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    # 텔레그램 채팅방에 채팅 메시지 보내기 위한 
    # 용도이기 때문에 HTTP Request(요청) - POST 방식 으로 진행 
    # HTTP POST 요청하여 채팅방에 전송할 채팅 메시지가 담긴 변수(data)를 추가로 저장 
    # http.request 함수 호출시 'POST', url, fields=data 3가지 인자 전달 
    response = http.request('POST',url ,fields=data)
    # 텔레그램 채팅방에 보낸 채팅 메시지 정보 아래처럼 리턴 
    # json.loads 함수 호출 하여 JSON 문자열 -> Dictionary 객체 변환 처리 
    # JSON 문자열 (예) '{"name": "홍길동", "birth": "0525", "age": 30}'
    # Dictionary 객체 (예) {'name': '홍길동', 'birth': '0525', 'age': 30}
    # 참고 URL - https://wikidocs.net/126088 
    return json.loads(response.data.decode('utf-8'))

# 사진 전송
# 텔레그램 채팅방에 ChatGPT - DALL.E 2가 생성한 이미지 보내기
# 아래 sendPhoto 함수 호출시
# ChatGPT - DALL.E 2가 그려주고 최종 생성된 이미지 URL 주소를 
# 인자로 전달하여 텔레그램 채팅방에 이미지 보내는 것도 가능함.
def sendPhoto(chat_id, image_url,msg_id):
    # 변수 data에 채팅방에 전송할 이미지 URL 주소가 담긴
    # JSON 포맷 데이터 저장 
    # 'chat_id' - 이미지 전송할 채팅방 아이디 
    # 'text' - 채팅방으로 전송할 이미지 URL 주소
    # 'reply_to_message_id' - 사용자가 보낸 메세지 아이디
    data = {
        'chat_id': chat_id,
        'photo': image_url,
        'reply_to_message_id': msg_id
    }
    # 라이브러리(패키지) urllib3의 PoolManager 클래스 객체 http 생성
    http = urllib3.PoolManager()
    # 텔레그램 채팅방에 이미지 보내기 위해
    # 텔레그램 API의 sendPhoto 메소드 활용한 HTTP 통신 요청 문자열 사용
    # "https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    # 텔레그램 채팅방에 이미지 보내기 위한 
    # 용도이기 때문에 HTTP Request(요청) - POST 방식 으로 진행 
    # HTTP POST 요청하여 채팅방에 전송할 이미지 URL 주소가 담긴 변수(data)를 추가로 저장 
    # http.request 함수 호출시 'POST', url, fields=data 3가지 인자 전달 
    response = http.request('POST', url, fields=data)
    # 텔레그램 채팅방에 전송한 이미지 정보 및 
    # 텔레그램 서버에서 채팅방으로 이미지를 잘 전송했다고 
    # 이미지를 전송한 행위에 대한 정보 아래처럼 리턴 
    # json.loads 함수 호출 하여 JSON 문자열 -> Dictionary 객체 변환 처리 
    # JSON 문자열 (예) '{"name": "홍길동", "birth": "0525", "age": 30}'
    # Dictionary 객체 (예) {'name': '홍길동', 'birth': '0525', 'age': 30}
    # 참고 URL - https://wikidocs.net/126088 
    return json.loads(response.data.decode('utf-8'))

# OpenAI API 사용해서 사용자가 ChatGPT에게 질문하고
# ChatGPT로 부터 답변받기
# 텔레그램 채팅방 안에서 사용자가 텔레그램 챗봇(ChatGPT)에게 질문을 하면
# 질문의 내용이 변수 messages로 input돼서 해당 함수 getTextFromGPT 실행
def getTextFromGPT(messages):   # ChatGPT한테 질문을 하게 될 프롬프트(messages)를 함수 getTextFromGPT에 input으로 받기 
    # 텔레그램 챗봇(ChatGPT)에게 질문을 할때는 
    # 아래와 같은 시스템 프롬프트(System Prompt - [{"role": "system", "content": 'You are a thoughtful assistant. Respond to all input in 25 words and answer in korea'}])와 함께 질문
    # 시스템 프롬프트의 내용("content": 'You are a thoughtful assistant. Respond to all input in 25 words and answer in korea')이 
    # 의미하는 뜻은 "넌 훌륭한 도우미고 답변은 25자 내외로 한국어로 해줘." 이다.
    # 이렇듯 텔레그램 챗봇(ChatGPT)의 답변의 뉘앙스(응답 스타일)를 변경하고 싶은 경우 
    # 시스템 프롬프트의 내용("content": 'You are a thoughtful assistant. Respond to all input in 25 words and answer in korea')을
    # 개발자의 요구사항에 맞게 변경하면 된다.
    # ChatGPT API에서 요구하는 프롬프트(messages) input 양식으로 변경 및 변경한 input 양식을 변수 messages_prompt에 저장 
    # messages_prompt = [{"role": "system", "content": 'You are a thoughtful assistant. Respond to all input in 25 words and answer in korea'}]
    messages_prompt = [{"role": "system", "content": 'You are a thoughtful assistant. Respond to all input in 100 words and answer in korea'}]
    messages_prompt += [{"role": "user", "content": messages}]  

    # openai.ChatCompletion.create 함수 파라미터 "messages"에 messages_prompt 저장 
    # 함수 openai.ChatCompletion.create 호출 결과 최종적으로 ChatGPT API를 통해서 받은 응답을
    # response라는 변수에 저장 
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages_prompt)
    # response에서 ChatGPT의 응답 메시지 부분만 발췌를 해서(response["choices"][0]["message"])
    # 변수 system_message에 저장
    system_message = response["choices"][0]["message"]
    return system_message["content"]   # ChatGPT의 응답 메시지에 속한 답변 내용 부분(system_message["content"])만 발췌 및 리턴

# OpenAI API 사용해서 사용자가 DALLE.2에게 그림 생성을 요청하고
# 생성된 그림의 URL 주소 받기
# 텔레그램 채팅방 안에서 사용자가 텔레그램 챗봇(ChatGPT)에게 그림 생성을 요청하면
# 요청한 내용이 변수 messages로 input돼서 해당 함수 getImageURLFromDALLE 실행
# DALLE.2 주의사항 
# 1. 특정 유명인 (예) 도널드 트럼프, 바이든 등등… 을 그림 그려달라고 요청 시 오류 발생 
#    참고 URL - https://community.openai.com/t/your-request-was-rejected-as-a-result-of-our-safety-system-your-prompt-may-contain-text-that-is-not-allowed-by-our-safety-system/285641
#    1번 오류 발생시 위의 ChatGPT로 부터 답변받기 함수 "getTextFromGPT" 몸체 안 변수 "messages_prompt"에 할당되는 시스템 프롬프트 문자열(항목 "content") 아래처럼 변경 후 컴파일 빌드 다시 실행 필요 
# (변경 전) messages_prompt = [{"role": "system", "content": 'You are a thoughtful assistant. Respond to all input in 25 words and answer in korea'}]
# (변경 후) messages_prompt = [{"role": "system", "content": 'You are a thoughtful assistant. Respond to all input in 100 words and answer in korea'}]
# 2. 영어가 아닌 한글로 그림 그려달라고 요청 시 요청사항과 전혀 다른 그림으로 그려줌.
# 3. 사용자가 그림 그려달라고 요청시 시간이 소요됨 (간단한 그림은 몇초 단위 / 복잡한 그림은 그 이상 시간 소요)
def getImageURLFromDALLE(messages):
    # 사용자가 DALLE.2에게 그림 생성을 요청한 내용이 
    # 문자열로 저장된 변수 messages를 
    # 함수 openai.Image.create 에 전달하여 이미지 생성
    # 생성한 이미지에 대한 정보를 변수 response에 저장 
    # DALLE.2로 생성한 이미지의 사이즈(size)를 "512x512"로 설정
    response = openai.Image.create(prompt=messages,n=1,size="512x512")
    # 이미지를 다운받을 수 있는 이미지 URL 주소(response['data'][0]['url'])를
    # 변수 image_url에 저장 
    image_url = response['data'][0]['url']
    return image_url   # 이미지를 다운받을 수 있는 이미지 URL 주소 리턴 

###### 메인 함수 구현 단계 ######
# 텔레그램 챗봇의 모든 기능 실행 
# 상황에 맞는 기능함수 호출
# 1) 사용자가 입력한 질문 내용을 분석해서 ChatGPT에게 답변 요청
# 2) 사용자가 입력한 그림 생성을 요청한 내용 분석해서 DALLE.2에게 그림 생성을 요청
# 매개변수 telegramrequest는 텔레그램을 통해 입력받은 채팅 정보를 인자로 전달 받음.
def chatBot(telegramrequest):
    
    # 텔레그램을 통해 입력받은 채팅 정보가 담긴 변수 telegramrequest를
    # result 변수에 저장
    result = telegramrequest

    # 텔레그램을 통해 입력받은 채팅 정보(메시지)가
    # 챗봇(['from']['is_bot'])이 입력한 메시지가 아닌 경우 
    # 즉, 사람이 입력한 메시지인 경우 의미
    if not result['message']['from']['is_bot']:

        # 메세지를 보낸 사람의 chat ID 
        # 텔레그램 채팅방에서 채팅 메시지를 입력한 사용자에게
        # 회신을 하기 위해서 사용자의 아이디(['message']['chat']['id'])를 변수 chat_id에 저장 
        chat_id = str(result['message']['chat']['id'])

        # 해당 메세지의 ID
        # 텔레그램 채팅방에서 채팅 메시지를 입력한 사용자에게
        # 회신을 하기 위해서 채팅 메세지의 아이디(['message']['message_id']))를 변수 msg_id에 저장 
        # 변수 msg_id에 채팅 메세지의 아이디를 저장하는 이유는
        # 사용자가 텔레그램 챗봇이 미처 답변을 하기 전에 
        # 다른 질문을 연달아 넣을 수도 있기 때문이다.
        # 그럴 경우 각각의 채팅 메시지에 회신을 하기 위해서
        # 해당 채팅 메시지의 아이디(['message']['message_id']))를 
        # 아래와 같이 저장을 해야한다.
        msg_id = str(int(result['message']['message_id']))

        # 만약 그림 생성을 요청하면
        # 만약 텔레그램 채팅방에 사용자가 입력한 메시지 안에
        # '/img'란 문자열이 포함되어 있으면,  
        # 즉, DALLE.2에게 그림 생성을 요청한 경우 
        if '/img' in result['message']['text']:
            # "/img"란 문자열만 공백("")으로 변환(replace) 처리 하고 
            # DALLE.2에게 그림 생성을 요청한 프롬프트(Prompt) 내용만 발췌하여 변수 prompt에 저장
            prompt = result['message']['text'].replace("/img", "")
            # DALL.E 2로부터 생성한 이미지 URL 주소 받기
            # getImageURLFromDALLE 함수 호출시 위의 변수 prompt 인자로 전달하여
            # DALL.E 2에게 그림 생성 요청 및 생성한 이미지 URL 주소 받기
            # DALL.E 2가 생성한 이미지의 URL 주소를 변수 bot_response에 저장하기 
            bot_response = getImageURLFromDALLE(prompt)
            # 이미지 텔레그램 방에 보내기
            # sendPhoto 함수 호출시 위의 변수 3가지
            # chat_id, bot_response, msg_id 인자로 전달하여
            # 텔레그램 채팅방에 DALL.E 2가 생성한 이미지 전송 처리
            # 이 때 위에 있는 변수 chat_id, msg_id를 활용해서
            # 채팅 메시지를 입력한 사용자와 해당 메시지에게
            # 직접 이미지 전송 처리함.
            print(sendPhoto(chat_id,bot_response, msg_id))
        # 만약 chatGPT의 답변을 요청하면
        # 만약 텔레그램 채팅방에 사용자가 입력한 메시지 안에
        # '/ask'란 문자열이 포함되어 있으면,  
        # 즉, ChatGPT에게 답변을 요청한 경우 
        if '/ask' in result['message']['text']:
            # "/ask"란 문자열만 공백("")으로 변환(replace) 처리 하고 
            # ChatGPT에게 질문한 프롬프트(Prompt) 내용만 발췌하여 변수 prompt에 저장
            prompt = result['message']['text'].replace("/ask", "")
            # ChatGPT로부터 답변 받기
            # getTextFromGPT 함수 호출시 위의 변수 prompt 인자로 전달하여
            # ChatGPT에게 질문을 하고 답변 받기
            # ChatGPT에게 받은 답변을 변수 bot_response에 저장하기 
            bot_response = getTextFromGPT(prompt)
            # 답변 텔레그램 방에 보내기
            # sendMessage 함수 호출시 위의 변수 3가지
            # chat_id, bot_response, msg_id 인자로 전달하여
            # 텔레그램 채팅방에 ChatGPT에게 받은 답변 전송 처리
            # 이 때 위에 있는 변수 chat_id, msg_id를 활용해서
            # 채팅 메시지를 입력한 사용자와 해당 메시지에게
            # 직접 ChatGPT에게 받은 답변 전송 처리함.
            print(sendMessage(chat_id, bot_response,msg_id))
    
    return 0