"""
* 카카오톡 챗봇 프로그램

*** 참고 ***
*** 파이썬 문서 ***
* with 문
참고 URL - https://docs.python.org/ko/3/reference/compound_stmts.html#index-16
참고 2 URL - https://velog.io/@hyungraelee/Python-with

* threading.Thread
참고 URL - https://docs.python.org/ko/3/library/threading.html#thread-objects
참고 2 URL - https://mechacave.tistory.com/2
참고 3 URL - https://pybi.tistory.com/19

* 데몬 스레드 (daemon=True)
참고 URL - https://wikidocs.net/82581

* os
참고 URL - https://docs.python.org/3/library/os.html

*** 기타 문서 ***

"""

##### 패키지 불러오기 #####
from fastapi import Request, FastAPI   # FastAPI 웹서비스
from utils import openAI_util          # OpenAI 전용 유틸(util)
from utils import kakao_util           # KAKAO 전용 유틸(util)
from typing import Any                 # Type Hints class Any
from queue import Queue                # 자료구조 queue (deque 기반)

import threading    # 멀티스레드
import time         # 챗봇 답변 시간 계산
import os           # 폴더/파일 처리

API_KEY = "API_key"
openAI_util.openai.api_key = API_KEY   # OpenAI API 키 입력

def init_tmp_file(file_path: str) -> None:
    """
    Description: 임시 로그 텍스트 파일 초기화

    Parameters: file_path - 임시 로그 텍스트 파일 상대 경로 - (예시) '/tmp/chatbot.txt'

    Returns: 없음.
    """

    with open(file_path, 'w') as f:   # 임시 로그 텍스트 파일 열기
        f.write("")

###### 서버 생성 단계 #######
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

    Returns: { "message": "kakaobot" } - 크롬(Chrome) 웹브라우저 화면 URL 주소 접속시 출력 메시지 ("http://localhost:8000/" or "http://127.0.0.1:8000/")
    """

    return { "message": "kakaobot" }

@app.post("/chat/")   # HTTP 통신(post) - 메인 주소 하위 주소("/chat/") 접속
async def chat(request: Request) -> dict[str, Any]:
    """
    Description: 카카오톡 서버 연결 비동기 함수
                 사용자 채팅 입력시 챗봇 응답 기능을 실행할 수 있는 비동기 함수이다.

                 *** 참고 ***
                 비동기 웹서버 
                 로컬 포트(Port) - 8000(default)
                 카카오톡 서버 연결 URL 주소 - "http://localhost:8000/chat/" or "http://127.0.0.1:8000/chat/"

    Parameters: request - 사용자 입력 채팅 정보

    Returns: mainChat(kakao_request) - 챗봇 응답 전용 메인 함수
    """

    kakao_request = await request.json()   # 사용자 입력 채팅 정보 json format 변환 및 kakao_request 변수 저장
    return mainChat(kakao_request)   # 챗봇 응답 전용 메인 함수 시작

###### 메인 함수 단계 #######

def mainChat(kakao_request: dict[str, Any]) -> dict[str, Any]:
    """
    Description: 챗봇 응답 전용 메인 함수

    Parameters: kakao_request - 카카오톡 채팅방 실제 채팅 정보

    Returns: response - 챗봇 답변 메시지 (페이로드)
    """

    # run_flag 변수 값
    # True - 답변/그림 응답 제한시간 3.5초 내로 완성
    # False - 답변/그림 응답 제한시간 3.5초 초과 및 미완성
    run_flag = False   # 답변/그림 응답 제한시간 초과 여부 초기화
    start_time = time.time()   # 챗봇 응답 전용 메인 함수 (mainChat) 시작 시간 - 챗봇 응답 시간 계산 용도

    cwd = os.getcwd()   # kakaobot.py 파이썬 파일 경로 cwd 변수 저장
    file_path = cwd + '/chatbot.txt'   # kakaobot.py 파이썬 파일과 같은 경로 '/chatbot.txt' 임시 로그 텍스트 파일 생성 및 file_path 변수 저장 

    if not os.path.exists(file_path):   # 해당 임시 로그 텍스트 파일 존재하지 않는 경우
        init_tmp_file(file_path)   # 임시 로그 텍스트 파일 초기화

    else: print("File Exists")    # "File Exists" 임시 로그 텍스트 파일 존재 메시지 출력 

    res_queue = Queue()   # 챗봇 답변 메시지 포함된 큐

    request_respond = threading.Thread(target=responseOpenAI,   # 작업 스레드 실행 대상 함수
                                       args=(kakao_request, res_queue, file_path),   # responseOpenAI 함수 실행시 필요 인자
                                       daemon=True)   # 작업 스레드 함수 연결 (daemon=True - 데몬 스레드 생성)
    request_respond.start()   # 작업 스레드 시작

    while (time.time() - start_time < 3.5):   # 챗봇 응답 시간 3.5초 이내인 경우
        if not res_queue.empty():   # 응답 제한시간 3.5초 내로 답변/그림 생성된 경우
            response = res_queue.get()   # 응답 큐 아이템 가져오기 (답변/그림)
            run_flag = True
            break   # while 반복문 종료 
        time.sleep(0.01)   # 딜레이 타임 0.01초 (챗봇 프로그램 안정적인 구동하기 위해 설정)

    if False == run_flag:   # 응답 제한시간 3.5초 초과 및 답변/그림 생성되지 않은 경우
        response = kakao_util.timeOver_quickReplies()   # 챗봇 응답 시간 5초 초과시 응답 재요청 메세지 카카오톡 채팅방 전송

    return response   # 카카오톡 서버로 챗봇 답변 메시지 (페이로드) 리턴

def responseOpenAI(kakao_request: dict[str, Any], res_queue: Queue, file_path: str) -> None:
    """
    Description: 답변/그림 요청 및 응답 확인 함수

    Parameters: kakao_request - 카카오톡 채팅방 실제 채팅 정보
                res_queue - 챗봇 답변 메시지 포함된 큐
                file_path - 아마존 웹서비스 람다 함수 (AWS Lambda Function) -> 임시 로그 텍스트 파일 상대 경로 - (예시) '/tmp/chatbot.txt'

                *** 참고 ***
                /tmp 임시 폴더 (스토리지) - 아마존 웹서비스 람다 함수 (AWS Lambda Function)에서 파일을 저장할 수 있는 임시 로컬 스토리지 영역
                실행 결과 (Execution results)는 람다 함수 (Lambda Function) 콘솔 "테스트" 탭에서 함수 실행 성공 여부, 실행 결과, 임시 로그 확인 가능
                참고 URL - https://docs.aws.amazon.com/ko_kr/lambda/latest/dg/configuration-ephemeral-storage.html#configuration-ephemeral-storage-use-cases
                참고 2 URL - https://inpa.tistory.com/entry/AWS-%F0%9F%93%9A-%EB%9E%8C%EB%8B%A4-tmp-%EC%9E%84%EC%8B%9C-%EC%8A%A4%ED%86%A0%EB%A6%AC%EC%A7%80-%EC%82%AC%EC%9A%A9-%EB%B0%A9%EB%B2%95

    Returns: 없음.
    """

    if '생각 다 끝났나요?' in kakao_request["userRequest"]["utterance"]:   # 시간 5초 초과시 응답 재요청
        with open(file_path) as f:   # 임시 로그 텍스트 파일 열기
            last_update = f.read()   # 해당 텍스트 파일(f) 저장된 ChatGPT 답변 또는 DALLE.2 생성한 그림 URL 주소 읽어오기

        if len(last_update.split())>1:   # 해당 텍스트 파일(f) 읽어온 정보 있을 경우
            kind = last_update.split()[0] 
            
            if "img" == kind:   # 해당 텍스트 파일(f) 읽어온 정보가 DALLE.2 생성한 그림 URL 주소인 경우
                # last_update.split()[1] - DALLE.2 생성한 그림 URL 주소 문자열 저장된 변수
                # last_update.split()[2] - DALLE.2 그림 생성 요청하는 프롬프트 문자열 (prompt)
                image_url, prompt = last_update.split()[1], last_update.split()[2]
                res_queue.put(kakao_util.simple_image(prompt, image_url))   # DALLE2 이미지 (image_url) 카카오톡 채팅방 전송

            else:   # 해당 텍스트 파일(f) 읽어온 정보가 ChatGPT 답변인 경우
                bot_res = last_update[4:]   # last_update[4:] - ChatGPT 답변 문자열 저장된 변수
                print(bot_res)
                res_queue.put(kakao_util.simple_text(bot_res))   # 텍스트 메시지 카카오톡 채팅방 전송
            init_tmp_file(file_path)  # 임시 로그 텍스트 파일 초기화

    elif '/img' in kakao_request["userRequest"]["utterance"]:   # DALLE.2 그림 생성 요청한 경우
        init_tmp_file(file_path)   # 임시 로그 텍스트 파일 초기화

        prompt = kakao_request["userRequest"]["utterance"].replace("/img", "")   # 사용자 입력 채팅 메세지(kakao_request["userRequest"]["utterance"]) 포함된 "/img" 문자열 공백("") 변경 및 나머지 문자열 prompt 변수 저장
        image_url = openAI_util.image_url_dalle2(prompt)   # DALLE.2 이미지 생성 및 URL 주소 가져오기
        res_queue.put(kakao_util.simple_image(prompt, image_url))   # DALLE2 이미지 (image_url) 카카오톡 채팅방 전송

        save_log = "img" + " " + str(image_url) + " " + str(prompt)
        with open(file_path, 'w') as f:   # DALLE.2 생성한 그림 URL 주소 포함된 정보(save_log) 임시 로그 텍스트 파일(f) 작성
            f.write(save_log)

    elif '/ask' in kakao_request["userRequest"]["utterance"]:   # ChatGPT 답변 요청한 경우
        init_tmp_file(file_path)   # 임시 로그 텍스트 파일 초기화
        
        prompt = kakao_request["userRequest"]["utterance"].replace("/ask", "")   # 사용자 입력 채팅 메세지(kakao_request["userRequest"]["utterance"]) 포함된 "/ask" 문자열 공백("") 변경 및 나머지 문자열 prompt 변수 저장
        
        # messages_prompt - 시스템 프롬프트와 prompt 변수 합쳐서 구현.
        # 시스템 프롬프트 문자열
        # 넌 훌륭한 도우미고 답변은 25자 내외로 한국어로 해줘.
        # messages_prompt = [{"role": "system", "content": 'You are a thoughtful assistant. Respond to all input in 25 words and answer in korea'}]
        messages_prompt = [{"role": "system", "content": 'You are a thoughtful assistant. Respond to all input in 25 words and answer in korea'}]
        messages_prompt += [{"role": "user", "content": prompt}]

        bot_res = openAI_util.get_response(messages_prompt)   # ChatGPT 텍스트 응답 메시지 가져오기
        res_queue.put(kakao_util.simple_text(bot_res))   # 텍스트 메시지 (text) 카카오톡 채팅방 전송
        print(bot_res)

        save_log = "ask" + " " + str(bot_res)
        with open(file_path, 'w') as f:   # ChatGPT 텍스트 응답 메시지 포함된 정보(save_log) 임시 로그 텍스트 파일(f) 작성
            f.write(save_log)
            
    else:   # 그 외 나머지 일반 채팅일 경우
        res_queue.put(kakao_util.empty_response()) 