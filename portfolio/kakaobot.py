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

import threading    # 멀티스레드
import time         # 챗봇 답변 시간 계산
import queue as q   # 자료구조 queue (deque 기반)
import os           # 폴더/파일 처리

def init_tmp_file(file_path: str) -> None:
    """
    Description: 임시 로그 텍스트 파일 초기화

    Parameters: file_path - 임시 로그 텍스트 파일 상대 경로 - (예시) '/tmp/botlog.txt'

    Returns: 없음.
    """

    with open(file_path, 'w') as f:
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

def mainChat(kakao_request: dict[str, Any]):
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
    file_path = cwd + '/botlog.txt'   # kakaobot.py 파이썬 파일과 같은 경로 '/botlog.txt' 임시 로그 텍스트 파일 생성 및 file_path 변수 저장 

    if not os.path.exists(file_path):   # 해당 임시 로그 텍스트 파일 존재하지 않는 경우
        init_tmp_file(file_path)   # 임시 로그 텍스트 파일 초기화

    else: print("File Exists")    # "File Exists" 임시 로그 텍스트 파일 존재 메시지 출력 

    res_queue = q.Queue()   # 챗봇 답변 메시지 포함된 큐
    # 패키지 "threading"을 활용해서 
    # 멀티스레드 작업스레드 객체 request_respond 생성 및 함수 responseOpenAI를 실행한다.
    # 패키지 "threading"을 이용해 request_respond.start() 함수 호출
    # -> 함수 responseOpenAI를 실행하면
    # 해당 함수 responseOpenAI가 끝날 때 까지 기다리지 않고
    # 바로 아래 답변 생성 시간 체크 소스코드 (while (time.time() - start_time < 3.5):)가 실행된다.
    request_respond = threading.Thread(target=responseOpenAI,
                                       args=(kakao_request, res_queue, file_path),
                                       daemon=True)   # 작업 스레드 함수 연결 (daemon=True - 데몬 스레드 생성)
    request_respond.start()

    # 답변 생성 시간 체크
    # 패키지 "threading"을 이용해서 
    # 위에서는 함수 responseOpenAI를 실행하여
    # ChatGPT 답변과 DALLE.2가 그려준 그림을 요청하는 동시에
    # 밑에서는 답변이 오는 시간을 측정할 수 있다.
    # 시작시간(start_time)으로 부터 응답 제한시간 3.5초가 지날 때까지 while문 반복
    # 응답 제한시간(3.5초) = 현재시간(time.time()) - 시작시간(start_time) 
    while (time.time() - start_time < 3.5):
        # 시작시간(start_time)으로 부터 응답 제한시간 3.5초가 지날 때까지
        # 0.1초에 한번씩 큐 자료구조 res_queue에 답변/그림이 담겨 있는지 확인
        # 만약 시작시간(start_time)으로 부터 
        # 응답 제한시간 3.5초내로 답변/그림이 생성된 경우(조건문 if not res_queue.empty(): 만족한 경우(True))
        if not res_queue.empty():
            # 시작시간(start_time)으로 부터 응답 제한시간 3.5초 안에 답변/그림이 완성(생성)되면 바로 값 리턴
            # 자료구조 res_queue에 저장된 답변/그림을 꺼내서 변수 response에 저장  
            response = res_queue.get()
            run_flag= True   # 변수 run_flag 값 True 할당 "답변/그림이 응답 제한시간 3.5초내에 완성" 의미
            break   # while 반복문 종료 
        # 안정적인 구동을 위한 딜레이 타임 설정
        # 아래처럼 time.sleep(0.01) 호출하여 0.01초씩 딜레이 타임을 주지 않으면
        # 너무 빨리 돌아서 카카오 챗봇 프로그램이 가끔 종료되는 현상이 발생한다.
        # 하여 카카오 챗봇 프로그램의 안정적인 구동을 위해서
        # time.sleep(0.01) 함수를 호출한다.
        time.sleep(0.01)  

    # 3.5초 내 답변/그림이 생성되지 않을 경우 
    # (위의 while문의 조건문 if not res_queue.empty(): 만족하지 않은 경우)
    # (조건문 if run_flag== False: 만족한 경우)
    # 시작시간(start_time)으로 부터 응답 제한시간 3.5초 안에 답변이 완성(생성)되지 않은 경우
    if run_flag== False:
        response = timeover()   # 함수 timeover 호출 및 시간 지연 안내메시지 및 버튼 생성하는 json 포맷 데이터 리턴을 해줘서 최종적으로 변수 response에 저장 

    return response   # 카카오톡 서버로 json 형태의 데이터가 담긴 변수 response 리턴

# 답변/그림 요청 및 응답 확인 함수
# 메인함수 mainChat에서 패키지 "threading"을 통해서 사용하고 있는
# 멀티스레드(작업스레드) 함수 responseOpenAI
# 사용자의 채팅을 분석해서 
# ChatGPT에게 답변을 받거나 DALLE.2에게 그림을 받는 기능을 수행한다.
def responseOpenAI(request,res_queue,file_path):
    """
    Description: 답변/그림 요청 및 응답 확인 함수

    Parameters:

    Returns:
    """

    # 사용자가 기다리다가 버튼('생각 다 끝났나요?')을 클릭하여 답변 완성 여부를 다시 봤을 시
    # 사용자가 기다리다가 버튼('생각 다 끝났나요?')을 클릭하면 카카오톡 채팅방에 
    # 마치 사용자가 입력한 것처럼 '생각 다 끝났나요?' 라는 메세지가 출력된다.
    # 해당 메시지 '생각 다 끝났나요?'는 함수 timeover 몸체 안에서 json 형태(Format)
    # 항목 "quickReplies" -> 항목 "messageText"에 "생각 다 끝났나요?"로 작성 했다.
    # request["userRequest"]["utterance"] 의미?
    # 사용자가 카카오톡 채팅방에 사용자의 채팅이 입력됐을 때
    # 카카오톡 서버에서 카카오 챗봇으로 보내주는
    # json 형태(Format)을 보면 이해할 수 있다.
    # json 형태(Format) 항목 "userRequest" -> 항목 "utterance" 안에 
    # 사용자의 채팅 내용이 포함되어 있다.
    # 하여 사용자의 채팅 내용이(request["userRequest"]["utterance"])이 '생각 다 끝났나요?'인 경우 
    # 즉 사용자가 버튼('생각 다 끝났나요?')을 클릭한 경우  
    if '생각 다 끝났나요?' in request["userRequest"]["utterance"]:
        # 텍스트 파일('/botlog.txt') 열기
        # open 함수 호출하여 응답 제한시간(3.5초) 초과한 시점에 저장된 
        # ChatGPT 답변 또는 DALLE.2에서 받은 그림의 URL 주소를 
        # 임시로 저장한 텍스트 파일을 불러와서 (f)
        # 텍스트 파일('/botlog.txt')에 저장된 내용을 꺼내서 .put 메서드 활용해서 큐 자료구조 res_queue에 저장  
        with open(file_path) as f:
            last_update = f.read()  # 해당 텍스트 파일(f)에 저장된 ChatGPT 답변 또는 DALLE.2에서 받은 그림의 URL 주소 읽어오기
        # 텍스트 파일 내 저장된 정보가 있을 경우
        if len(last_update.split())>1:
            kind = last_update.split()[0] 
            # 해당 텍스트 파일('/botlog.txt')에 저장돤 정보(데이터)가 DALLE.2가 생성한 이미지 URL 정보(데이터)인 경우 
            if kind == "img":
                # 변수 prompt는 DALLE.2한테 그림을 그려달라고 요청하는 프롬프트(prompt) 문자열이 저장된 변수이다.
                # 변수 bot_res는 DALLE.2가 생성한 그림 URL 주소 문자열이 저장된 변수이다.
                bot_res, prompt = last_update.split()[1],last_update.split()[2]
                # 함수 imageResponseFormat에 해당 변수 bot_res, prompt에 저장된 값을 인자로 전달하고
                # 해당 함수 imageResponseFormat 실행 결과 리턴된 값을 put 메서드 활용해서 큐 자료구조 res_queue에 저장 
                res_queue.put(imageResponseFormat(bot_res,prompt))
            # 해당 텍스트 파일('/botlog.txt')에 저장된 정보(데이터)가 ChatGPT 답변인 경우 
            else:
                # 변수 bot_res는 ChatGPT 답변 문자열이 저장된 변수이다.
                bot_res = last_update[4:]
                print(bot_res)
                # 함수 textResponseFormat에 해당 변수 bot_res에 저장된 값을 인자로 전달하고 
                # 해당 함수 textResponseFormat 실행 결과 리턴된 값을 put 메서드 활용해서 큐 자료구조 res_queue에 저장 
                res_queue.put(textResponseFormat(bot_res))
            dbReset(file_path)  # 함수 dbReset 실행하여 텍스트 파일('/botlog.txt')에 저장된 ChatGPT 답변 또는 DALLE.2에서 받은 그림의 URL 주소 초기화 

    # 이미지 생성을 요청한 경우
    # 만약 그림 생성을 요청하면
    # 만약 카카오톡 채팅방에 사용자가 입력한 메시지 안에
    # '/img'란 문자열이 포함되어 있으면,  
    # 즉, DALLE.2에게 그림 생성을 요청한 경우 
    elif '/img' in request["userRequest"]["utterance"]:
        dbReset(file_path)   # 함수 dbReset 실행하여 텍스트 파일('/botlog.txt')에 저장된 ChatGPT 답변 또는 DALLE.2에서 받은 그림의 URL 주소 초기화
        # replace 메서드 호출하여 텍스트 메시지 안에 "/img" 란 단어를 
        # 공백("")으로 변경한 나머지 사용자의 질문 내용 프롬프트 문자열을 추출해서 변수 prompt에 저장 
        prompt = request["userRequest"]["utterance"].replace("/img", "")
        # 함수 getImageURLFromDALLE 호출하여 DALLE.2에게 그림 생성 요청을 해서
        # 최종적으로 DALLE.2가 생성한 그림의 URL주소를 변수 bot_res에 저장 
        bot_res = getImageURLFromDALLE(prompt)
        # 함수 imageResponseFormat에 변수 bot_res,prompt를 인자로 전달하여 
        # DALLE.2가 생성한 그림 URL 주소값이 포함되어 카카오톡 서버로 전송할 그림 생성 전용 json 형태(Format)를 작성 및 리턴 
        # put 메서드 호출하여 최종적으로 큐 자료구조 res_queue에 저장함.
        res_queue.put(imageResponseFormat(bot_res,prompt))
        # DALLE.2가 생성한 그림 URL 주소 정보를 텍스트 파일('/botlog.txt') 변수 save_log에 저장함 
        # 변수 save_log에 저장하는 이유는 그림을 그리는게 응답 제한시간 3.5초 내로 완료가 안 됐으면
        # 우선은 DALLE.2가 생성한 그림 URL 주소를 텍스트 파일('/botlog.txt')에 임시로 저장을 해놓기 위해서 
        # 변수 save_log 선언 및 DALLE.2가 생성한 그림 URL 주소 할당 후 
        # 텍스트 파일('/botlog.txt')에 임시로 저장함.
        save_log = "img"+ " " + str(bot_res) + " " + str(prompt)
        with open(file_path, 'w') as f:
            f.write(save_log)

    # ChatGPT 답변을 요청한 경우
    # 만약 chatGPT의 답변을 요청하면
    # 만약 카카오톡 채팅방에 사용자가 입력한 메시지 안에
    # '/ask'란 문자열이 포함되어 있으면,  
    # 즉, ChatGPT에게 답변을 요청한 경우 
    elif '/ask' in request["userRequest"]["utterance"]:
        dbReset(file_path)   # 함수 dbReset 실행하여 텍스트 파일('/botlog.txt')에 저장된 ChatGPT 답변 또는 DALLE.2에서 받은 그림의 URL 주소 초기화
        
        # replace 메서드 호출하여 텍스트 메시지 안에 "/ask" 란 단어를 
        # 공백("")으로 변경한 나머지 사용자의 질문 내용 프롬프트 문자열을 추출해서 변수 prompt에 저장 
        prompt = request["userRequest"]["utterance"].replace("/ask", "")
        # 함수 getTextFromGPT 호출하여 ChatGPT에게 질문 요청을 해서
        # 최종적으로 ChatGPT의 답변을 변수 bot_res에 저장 
        bot_res = getTextFromGPT(prompt)
        # 함수 imageResponseFormat에 변수 bot_res를 인자로 전달하여 
        # ChatGPT의 답변이 포함되어 카카오톡 서버로 전송할 ChatGPT의 답변 전용 json 형태(Format)를 작성 및 리턴 
        # put 메서드 호출하여 최종적으로 큐 자료구조 res_queue에 저장함.
        res_queue.put(textResponseFormat(bot_res))
        print(bot_res)
        # ChatGPT의 답변 정보를 텍스트 파일('/botlog.txt') 변수 save_log에 저장함 
        # 변수 save_log에 저장하는 이유는 ChatGPT의 답변을 얻는데 응답 제한시간 3.5초 내로 완료가 안 됐으면
        # 우선은 ChatGPT의 답변을 텍스트 파일('/botlog.txt')에 임시로 저장을 해놓기 위해서 
        # 변수 save_log 선언 및 ChatGPT의 답변 내용 할당 후 
        # 텍스트 파일('/botlog.txt')에 임시로 저장함.
        save_log = "ask"+ " " + str(bot_res)

        with open(file_path, 'w') as f:
            f.write(save_log)
            
    # 아무 답변 요청이 없는 채팅일 경우
    # 카카오톡 채팅방의 사용자의 입력이 버튼('생각 다 끝났나요?')을 클릭한 경우도 아니고
    # DALLE.2에게 그림 생성 요청한 것도 아니고
    # ChatGPT의 답변을 요청한 것도 아닌 경우 
    else:
        # 기본 response 값
        # 아래처럼 그냥 내용 자체가 없는 깡통 json 형태(Format)의 정보(데이터)를 변수 base_response 에 저장
        base_response = {'version': '2.0', 'template': {'outputs': [], 'quickReplies': []}}
        # json 형태(Format)의 정보(데이터)가 저장된 변수 base_response 를 
        # put 메서드 활용해서 큐 자료구조 res_queue에 저장 
        res_queue.put(base_response) 