"""
* 텔레그램 챗봇 프로그램

*** 참고 ***
*** 파이썬 문서 ***

*** 기타 문서 ***
* json.loads 함수 - JSON 문자열 -> Dictionary 객체 변환 처리
JSON 문자열 (예) '{"name": "홍길동", "birth": "0525", "age": 30}'
Dictionary 객체 (예) {'name': '홍길동', 'birth': '0525', 'age': 30}
참고 URL - https://wikidocs.net/126088

"""

##### 패키지 불러오기 #####
from fastapi import Request, FastAPI   # FastAPI 웹서비스
from utils import openAI_util          # OpenAI 전용 유틸(util)
from typing import Any                 # Type Hints class Any

import urllib3   # URL 처리(HTTP 통신 용도)
import json      # json 데이터 처리

API_KEY = "API_key"
openAI_util.openai.api_key = API_KEY   # OpenAI API 키 입력

BOT_TOKEN = 'Token'   # 텔레그램 챗봇 토큰 번호(HTTP 통신 용도)

###### FastAPI 웹서버 생성 단계 ######

app = FastAPI()   # FastAPI 클래스 객체 생성 (app)

@app.get("/")   # HTTP 통신(get) - 메인 주소("/") 접속
async def root() -> dict[str, Any]:
    """
    Description: 메인 주소("/") 비동기 함수

                 *** 참고 ***
                 비동기 웹서버 
                 로컬 포트(Port) - 8000(default)
                 메인 URL 주소 - "http://localhost:8000/" or "http://127.0.0.1:8000/"

    Parameters: 없음.

    Returns: { "message": "telegramebot" } - 크롬(Chrome) 웹브라우저 화면 URL 주소 접속시 출력 메시지 ("http://localhost:8000/" or "http://127.0.0.1:8000/")
    """

    return { "message": "telegramebot" }


@app.post("/chat")   # HTTP 통신(post) - 메인 주소 하위 주소("/chat/") 접속
async def chat(request: Request) -> dict[str, Any]:
    """
    Description: 텔레그램 서버 연결 비동기 함수
                 사용자 채팅 입력시 챗봇 응답 기능을 실행할 수 있는 비동기 함수이다.

    Parameters: request - 사용자 입력 채팅 정보

    Returns: mainChat(telegram_request) - 챗봇 응답 전용 메인 함수
    """

    telegram_request = await request.json()   # 사용자 입력 채팅 정보 json format 변환 및 telegram_request 변수 저장
    mainChat(telegram_request)   # 챗봇 응답 전용 메인 함수 시작
    return { "message": "telegramebot/chat" }

###### 기능 함수 구현 단계 ######

def sendMessage(chat_id: str, text: str, msg_id: str) -> dict[str, Any]:
    """
    Description: ChatGPT 답변 텔레그램 채팅방 전송

    Parameters: chat_id - ChatGPT 답변 전송할 채팅방 사용자 아이디 
                text - 채팅방으로 전송할 ChatGPT 답변 내용
                msg_id - 사용자가 보낸 채팅 메세지 아이디

    Returns: json.loads(response.data.decode('utf-8')) - 텔레그램 채팅방에 보낸 채팅 메시지 정보
    """

    data = {
        'chat_id': chat_id,
        'text': text,
        'reply_to_message_id': msg_id
    }

    http = urllib3.PoolManager()   # PoolManager 클래스 객체 생성 (http)
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"   # 텔레그램 API sendMessage 메소드 URL 주소 (ChatGPT 답변 텔레그램 채팅방 전송 용도)
    response = http.request('POST', url, fields=data)   # HTTP 통신(post)

    return json.loads(response.data.decode('utf-8'))   # 텔레그램 채팅방에 보낸 채팅 메시지 정보 리턴

def sendPhoto(chat_id: str, image_url: str, msg_id: str) -> dict[str, Any]:
    """
    Description: DALLE.2 생성한 그림 텔레그램 채팅방 전송

    Parameters: chat_id - DALLE.2 생성한 그림 전송할 채팅방 사용자 아이디 
                image_url - DALLE.2 생성한 그림 URL 주소
                msg_id - 사용자가 보낸 채팅 메세지 아이디

    Returns: json.loads(response.data.decode('utf-8')) - 텔레그램 채팅방에 보낸 DALLE.2 생성한 그림 URL 주소 정보
    """

    data = {
        'chat_id': chat_id,
        'photo': image_url,
        'reply_to_message_id': msg_id
    }
    
    http = urllib3.PoolManager()   # PoolManager 클래스 객체 생성 (http)
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"   # 텔레그램 API sendMessage 메소드 URL 주소 (DALLE.2 생성한 그림 텔레그램 채팅방 전송 용도)
    response = http.request('POST', url, fields=data)   # HTTP 통신(post)

    return json.loads(response.data.decode('utf-8'))   # 텔레그램 채팅방에 보낸 DALLE.2 생성한 그림 URL 주소 정보 리턴

###### 메인 함수 구현 단계 ######

def mainChat(telegram_request: dict[str, Any]) -> int:
    """
    Description: 챗봇 응답 전용 메인 함수

    Parameters: telegram_request - 텔레그램 채팅방 실제 채팅 정보

    Returns: 0 - 텔레그램 챗봇 프로그램 에러 없이 정상 종료
    """
    
    if not telegram_request['message']['from']['is_bot']:   # 챗봇이 입력한 메시지가 아닌 경우(즉, 사람이 입력한 메시지인 경우)
        chat_id = str(telegram_request['message']['chat']['id'])   # 채팅방 사용자 아이디
        msg_id = str(int(telegram_request['message']['message_id']))   # 채팅 메세지 아이디

        if '/img' in telegram_request['message']['text']:    # DALLE.2 그림 생성 요청한 경우
            prompt = telegram_request['message']['text'].replace("/img", "")   # 사용자 입력 채팅 메세지(telegram_request['message']['text']) 포함된 "/img" 문자열 공백("") 변경 및 나머지 문자열 prompt 변수 저장
            image_url = openAI_util.image_url_dalle2(prompt)   # DALLE.2 이미지 생성 및 URL 주소 가져오기

            print(sendPhoto(chat_id, image_url, msg_id))   # DALLE.2 생성한 그림 텔레그램 채팅방 전송

        if '/ask' in telegram_request['message']['text']:   # ChatGPT 답변 요청한 경우
            prompt = telegram_request['message']['text'].replace("/ask", "")   # 사용자 입력 채팅 메세지(telegram_request['message']['text']) 포함된 "/ask" 문자열 공백("") 변경 및 나머지 문자열 prompt 변수 저장
            
            # messages_prompt - 시스템 프롬프트와 prompt 변수 합쳐서 구현.
            # 시스템 프롬프트 문자열
            # 넌 훌륭한 도우미고 답변은 25자 내외로 한국어로 해줘.
            # messages_prompt = [{"role": "system", "content": 'You are a thoughtful assistant. Respond to all input in 25 words and answer in korea'}]
            messages_prompt = [{"role": "system", "content": 'You are a thoughtful assistant. Respond to all input in 25 words and answer in korea'}]
            messages_prompt += [{"role": "user", "content": prompt}]
            bot_res = openAI_util.get_response(messages_prompt)   # ChatGPT 텍스트 응답 메시지 가져오기

            print(sendMessage(chat_id, bot_res, msg_id))   # ChatGPT 답변 텔레그램 채팅방 전송
    
    return 0   # 텔레그램 챗봇 프로그램 에러 없이 정상 종료