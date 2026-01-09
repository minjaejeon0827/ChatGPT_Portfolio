# *** 파이썬 설치 시 주의사항 ***
# 꼭 파이썬 설치 시 3.11 버전 설치 필수! (3.12 버전에서 openai 패키지와 충돌하는 현상 발생.)
# 만약 파이썬 3.12 버전 설치 진행시 가상환경에 아래의 패키지 먼저 설치 필수!
# pip install aiottp==3.9.0b0

# 카카오톡 챗봇 채널 웹사이트
# 참고 URL - https://pf.kakao.com/_sNBsn

# 가상환경 폴더 "portfolio_env" 생성 터미널 명령어
# python -m venv portfolio_env

# 가상환경 폴더 "portfolio_env" 활성화 터미널 명령어
# portfolio_env\Scripts\activate.bat

# 주의사항 
# 비동기(async - await) 웹서버 생성하는 유비콘 패키지 "uvicorn[standard]"를 사용하는 파이썬 파일의 경우 
# 일반 파이썬 파일을 터미널에서 실행하는 명령어(python test_kakaobot.py)를 
# 그대로 쓰면 파일 안에 있는 FastAPI 서버(FastAPI 클래스 객체 app)가 생성 불가하다.
# 하여 비동기(async - await) 웹서버 생성하는 유비콘 패키지 "uvicorn[standard]"를 사용하는 파이썬 파일은
# 아래와 같은 명령어를 입력 해야만 해당 파일 안에 있는 FastAPI 서버(FastAPI 클래스 객체 app)가 생성된다.
# uvicorn test_kakaobot:app --reload


# ngrok 역할?
# 외부에서 개발자 로컬 PC로 접속할 수 있는 URL 주소가 필요하다.
# ngrok는 개발자 로컬 PC에서 생성한 서버 개발 환경을
# 외부 서버에서도(전세계 어디 서버에서도) 접속할 수 있도록 공유해주는 서비스이다.
# 즉, 외부에서 개발자 로컬 PC로 접속할 수 있는 URL 주소를 발급해준다.
# 또한 서로 다른 네트워크(텔레그램 서버와 개발자 PC에서 실행시키는 FastAPI 로컬 서버)를
# 연결 해주는 통로의 역할을 하는 게이트웨이와 비슷한 역할이다.
# ngrok 웹사이트
# 참고 URL - https://ngrok.com/ 

# 게이트웨이 용어 설명
# 참고 URL - https://ko.wikipedia.org/wiki/%EA%B2%8C%EC%9D%B4%ED%8A%B8%EC%9B%A8%EC%9D%B4

# ngrok 응용 프로그램 실행 방법
# 1) 비쥬얼스튜디오코드(VSCode) 실행 
#    -> 유비콘 패키지 "uvicorn[standard]"를 사용하는 파이썬 파일 "test_kakaobot.py" 또는 "test_telegramebot.py" 열기
#    -> OpenAI API 키 값 입력 
#    -> 터미널창 열어서 명령어 "uvicorn test_kakaobot:app --reload" 입력 및 엔터 
#    -> FastAPI 서버(FastAPI 클래스 객체 app)가 정상적으로 생성 완료

# 2) 텔레그램 응용 프로그램 실행 

# 3) PC 바탕 화면 -> ngrok 바로가기 아이콘 더블 클릭
# ngrok 바로가기 아이콘 존재하지 않으면 아래 파일경로 들어가서 ngrok 응용 프로그램 실행
# 파일 경로 - "C:\Users\bhjeon\Desktop\회사_업무_및_공부_자료\상상진화 회사 업무\AI 챗봇_개발\텔레그램_카카오_챗봇_ngrok_실행_프로그램" -> 응용 프로그램 ngrok

# 4) ngrok 전용 터미널창 출력 
#    -> 아래 명령어 "ngrok authtoken 2sZKZBZ9stzdWgsAPcHt9JtrNzN_5QpYosiEkadfnfffAvsvn" 입력 및 엔터 
# (명령어 형식) ngrok authtoken <Your token>
# (명령어 예시) ngrok authtoken 2sZKZBZ9stzdWgsAPcHt9JtrNzN_5QpYosiEkadfnfffAvsvn

# 5) 4)번의 토큰 번호 입력이 잘 되었을 경우 터미널창에 아래와 같은 메시지 출력
# Authtoken saved to configuration file: C:\Users\bhjeon\AppData\Local/ngrok/ngrok.yml

# 6) ngrok 응용 프로그램 터미널창에 명령어 "ngrok http 8000" 입력 및 엔터 
#    -> 외부 서버에서도 개발자 로컬 PC로 접속할 수 있는 URL 주소 생성 
# 참고사항 
# - 위에 명령어 중 "8000"이 뜻하는 바는 개발자 로컬 PC안에 포트(Port) 번호를 의미함.
# - 파이썬 파일 "test_kakaobot.py"을 유비콘 패키지 "uvicorn[standard]"를 사용하여 FastAPI 웹서버를 생성해 놓은 상태이다.
#   FastAPI 서버 로컬 PC URL 주소는 "http://127.0.0.1:8000" 이다.
#   해당 URL 주소 중 "http://127.0.0.1"은 개발자의 로컬 PC를 의미하며,
#   "8000"은 개발자의 로컬 PC 안에서 몇동 몇호, 즉 예를들어 105동 105호가 "8000"을 뜻한다.
#   하여 개발자의 로컬 PC 안에 "8000"이라는 포트(Port) 번호 안에 
#   새로 생성한 FastAPI 웹서버를 오픈한 것을 의미한다.
#   즉, ngrok 응용 프로그램 터미널창에서 명령어 "ngrok http 8000" 입력 및 엔터를 치면
#   외부 서버에서도 개발자 로컬 PC에 있는 포트(Port) 번호 "8000"에 있는
#   새로 생성한 FastAPI 웹서버에 접속할 수 있는 URL 주소를 생성해준다.

# 7) ngrok 응용 프로그램 터미널창에 아래와 같은 메시지가 출력되면
#    이제 외부 서버에서도 개발자 로컬 PC로 접속할 수 있는 FastAPI 웹서버 URL 주소 생성 완료.
#    아래에 출력된 메시지 중 외부 서버에서도 개발자 로컬 PC로 접속할 수 있는 
#    FastAPI 웹서버 URL 주소 (예) "https://c84e-14-52-67-173.ngrok-free.app" 
#    로 외부 서버에서 접속을 하면 
#    개발자 로컬 PC에 포트(Port) 번호 "8000"로 접속이 가능("http://localhost:8000")하다는 것을 의미한다.
# 주의사항 - ngrok 응용 프로그램 터미널창에 URL 주소 "https://c84e-14-52-67-173.ngrok-free.app" 
#           복사하려고 단축키 Ctrl + C 키를 누르면 ngrok 응용 프로그램이 종료된다.(Ctrl+C to quit)
#           하여 절대 단축키 Ctrl + C 키를 누르지 말고 마우스로 해당 URL 주소를 드래그 한 후 
#           키보드 단축키 Ctrl + Insert 키를 눌러서 해당 URL 주소를 복사 및 메모장에 저장한다.
# (예) 터미널창에 출력되는 메시지 예시
# ngrok    (Ctrl+C to quit)                                                                                                                                                                                   
# Sign up to try new private endpoints https://ngrok.com/new-features-update?ref=private                                                                                                                                                                                                                                                                                
# Session Status                online                                                                                                                                               
# Account                       minjaejeon0827@gmail.com (Plan: Free)                                                                                                                
# Version                       3.19.1                                                                                                                                               
# Region                        Japan (jp)                                                                                                                                           
# Latency                       37ms                                                                                                                                                 
# Web Interface                 http://127.0.0.1:4040                                                                                                                                
# Forwarding                    https://c84e-14-52-67-173.ngrok-free.app -> http://localhost:8000                                                                                                                                                                                                                                                                       
# Connections                   ttl     opn     rt1     rt5     p50     p90                                                                                                                                        
#                               0       0       0.00    0.00    0.00    0.00     


# 8) "카카오비즈니스" 홈페이지 이동(참고 URL - https://business.kakao.com/) 
#    -> 카카오 계정 로그인 -> "카카오비즈니스" 화면 좌측 상단 탭 "채널" 클릭 -> 버튼 "챗봇" 클릭
#    -> 화면 "내 챗봇1" 이동 -> 항목 "봇이름" 밑에 2)번에서 생성한 챗봇 이름 "TestImbuChatBot" 클릭 
#    -> 새로 생성한 "TestImbuChatBot" 챗봇 관리자 센터 화면 이동 
#    -> 챗봇 관리자 센터 화면 좌측 탭 "스킬" 클릭 -> "스킬 목록" 클릭
#    -> "스킬 목록" 화면 이동 -> 버튼 "생성" 클릭

# 9) "스킬명을 입력해주세요" 화면 이동 -> 화면 상단 "스킬명을 입력해주세요"에 스킬명을 "test_kakaobot" 입력
#    -> 항목 "설명"에 내용 작성 생략 -> 항목 "URL"에 7)번에서 ngrok 응용 프로그램으로 생성한 
#       외부 서버에서도 개발자 로컬 PC로 접속할 수 있는 
#       FastAPI 웹서버 URL 주소(https://c84e-14-52-67-173.ngrok-free.app) 뒤에 "/chat/" 붙인 
#       URL 주소(https://c84e-14-52-67-173.ngrok-free.app/chat/)를 항목 "URL"에 입력하기
#    -> "스킬명을 입력해주세요" 화면 우측 상단 "기본 스킬로 설정" 체크
#    -> 버튼 "저장" 클릭 -> 해당 화면 마우스 스크롤 아래로 내려서 항목 "스킬 테스트" 이동 
#    -> 해당 "스킬 테스트" 항목은 카카오톡 서버와 연결이 잘 됐는지 확인할 수 있는 기능 "JSON"이 있다.
#    -> 해당 "JSON" 에서 작성된 양식은 카카오톡 서버 -> 개발자 로컬 PC FastAPI 서버로 
#       채팅 정보를 줄 때 전송하는 JSON 데이터 양식과 동일하다. 
#    -> 하여 해당 "JSON" 데이터를 가지고 디버깅 하면서 스킬 테스트를 진행할 수 있다.
#       해당 "JSON" 우측 하단 버튼 "스킬서버로 전송" 클릭
#    -> "스킬서버로 전송" 기능이 잘 실행되었는지 확인하려면
#       비쥬얼 스튜디오 코드 돌아와서 FastAPI 개발자 로컬 PC 비동기 웹서버 파이썬 파일(test_kakaobot.py)
#       @app.post("/chat/") 메서드 호출 -> async def chat(request: Request): 함수 실행 
#       -> 코드 kakaorequest = await request.json() 실행 ->  
#       print(kakaorequest) 함수 호출하여 터미널창에서 아래와 같은 결과가 출력되면 
#       "스킬서버로 전송" 기능이 잘 실행되었다는 것을 확인할 수 있다.
#       하여 해당 결과를 통하여 카카오톡 챗봇(카카오톡 서버)과 
#       FastAPI 개발자 로컬 PC 비동기 웹서버 파이썬 파일(test_kakaobot.py)이
#       연결이 아주 잘 되는 것을 확인할 수 있다.   
# {'intent': {
#             'id': 'qj4nick9o33seydhqobmj65t', 
#             'name': '블록 이름'
#            }, 
#  'userRequest': {'timezone': 'Asia/Seoul', 'params': {'ignoreMe': 'true'}, 
#  'block': {'id': 'qj4nick9o33seydhqobmj65t', 'name': '블록 이름'}, 
#  'utterance': '발화 내용', 
#  'lang': None, 
#  'user': {'id': '662293', 'type': 'accountId', 'properties': {}}}, 
#  'bot': {'id': '67a961ce1e098a447d574fe7', 
#  'name': '봇 이름'}, 
#  'action': {'name': 'vkjjc0ckza', 'clientExtra': None, 'params': {}, 
#  'id': 'o4yb2t6sg90zxh7qmnc8l85y', 'detailParams': {}}
# }       
# INFO: 219.249.231.42:0 - "POST /chat/ HTTP/1.1" 200 OK

# 10) "챗봇 관리자센터" 화면 좌측 상단 버튼 "시나리오" 클릭 
#     -> "시나리오" 화면 이동 -> 버튼 "+ 시나리오" 클릭 -> "시나리오" 화면 좌측 탭 "기본 시나리오" 하단 버튼 "폴백 블록" 클릭
#     -> "블록 이름을 입력해주세요" 출력 -> 항목 "파라미터 설정" 우측 체크 박스 "스킬 검색/선택" 클릭 -> 위에서 생성했던 스킬인 "test_kakaobot" 클릭
#     -> "시나리오" 화면 마우스 스크롤 아래로 내려서 항목 "봇 응답" 아래 
#        말풍선 형태 항목 "첫번째 응답 -텍스트형"의 
#        하위 항목 "+ 응답 추가 (0/3)" 아래에 있는 버튼 "스킬데이터" 클릭
#     -> 항목 "봇 응답" 아래에 있던 말풍선 형태 항목 "첫번째 응답 -텍스트형"이 사라지고 
#        항목 "봇 응답" 아래에 "스킬데이터 사용"만 출력되면 -> 버튼 "저장" 클릭
#     -> "스킬데이터" 저장 완료
#     "스킬데이터" 저장 완료되었다는 의미는 카카오톡 챗봇에서의 모든 기능을 방금 생성한 카카오봇 스킬
#     즉 카카오봇 스킬은 FastAPI 개발자 로컬 PC서버와 연결이 되어있다.
#     오직 FastAPI 개발자 로컬 PC서버 통해서만 카카오 챗봇이 모든 답변을 하겠다는 뜻으로 이해하면 된다.

# 11) 10)번까지 생성한(스킬데이터 저장 포함) 카카오 챗봇을 카카오톡 채널에 지정하려면 아래와 같이 한다.
#     -> "챗봇 관리자센터" 화면 좌측 버튼 "설정" 클릭 
#     -> "설정" 화면 이동 -> 항목 "기본 정보" 하단 하위 항목 "카카오톡 채널 연결" 옆에 버튼 "운영 채널 선택하기" 클릭 
#     -> 팝업화면 "운영 채널 연결" 출력 -> 맨 처음 단계에서 생성한 카카오톡 채널명 "Test_ImagineBuilder" 클릭
#     -> "설정" 화면 우측 상단 버튼 "저장" 클릭
#     -> 팝업화면 "배포를 진행하시겠습니까?" 출력 -> 버튼 "이동" 클릭

# 12) "배포" 화면 이동 -> "배포" 화면 우측 상단 "배포" 클릭
#     -> 팝업화면 "배포를 진행하시겠습니까?" 출력 -> 버튼 "배포" 클릭 
#     -> 처음 단계부터 지금까지 카카오 챗봇에 설정한 모든 사항들이 이제서야
#        외부 사용자들이 카카오 챗봇을 사용할 수 있도록 최종 배포 완료

# 13) 12)번에서 최종 배포 완료되었다면 최종 배포한 카카오 챗봇이 있는 대화창을 열어보려면 
#     "챗봇 관리자센터" 화면 좌측 상단 버튼 "kakao business" 클릭 
#     -> "카카오비즈니스 센터 대시보드" 화면 이동 
#     -> 항목 "자산 목록" 하단에 새로 생성했던 카카오톡 채널 "Test_ImagineBuilder" 클릭
#     -> "채널 관리자센터" 화면 이동 -> 해당 화면 좌측 탭 "친구 모으기" 클릭 -> 버튼 "채널 홍보" 클릭
#     -> "홍보하기" 화면 이동 -> 리본탭 "채널홈" 하단 하위 항목 "링크 복사하기" 하단 
#        URL 주소 "http://pf.kakao.com/_sNBsn" 옆에 버튼 "복사하기" 클릭 
#     -> 복사한 URL 주소 "http://pf.kakao.com/_sNBsn"를 구글 크롬(Chrome) 웹브라우저에 붙여넣기 및 엔터
#     -> 새로 생성한 카카오톡 채널 "Test_ImagineBuilder"이 화면상에 출력 
#     -> 해당 화면 우측 상단 버튼 "로봇모양 이모지콘" 클릭 
#     -> 카카오 (모바일/PC) 어플의 해당 카카오톡 채널 "Test_ImagineBuilder"의
#        카카오 챗봇 채팅방으로 이동 및 카카오 챗봇 안내 메시지 "안녕하세요. 무엇을 도와드릴까요?" 출력
#     -> 이제 맨 처음 단계에서 생성한 
#     카카오톡 채널 "Test_ImagineBuilder"에 외부 사용자가 채팅 입력을 하면 
#     그거에 대한 챗봇은 무조건 "TestImbuChatBot"이 대응하여 
#     외부 사용자의 채팅 입력에 대한 답변을 해준다.


##### 패키지 불러오기 #####
# FastAPI 패키지 "fastapi" 불러오기
# Request 패키지 불러오기 
from fastapi import Request, FastAPI # 개발자 로컬 PC 비동기 웹서버 구현시 필요
import openai   # OPENAI 패키지 openai 불러오기 (ChatGPT, DALLE.2 사용)
import threading  # 프로그램 안에서 동시에 작업하는 멀티스레드 구현하기 위해 패키지 "threading" 불러오기
import time   # ChatGPT 답변 시간 계산하기 위해 패키지 "time" 불러오기
import queue as q   # 자료구조 queue(deque 기반) 이용하기 위해 패키지 "queue" 불러오기
import os   # 답변 결과를 테스트 파일로 저장할 때 경로 생성해야 해서 패키지 "os" 불러오기

# OpenAI API KEY
# 테스트용 카카오톡 챗봇 채팅방에서 
# ChatGPT와 통신하기 위해 OpenAI API 키 입력
API_KEY = "API_key"
openai.api_key = API_KEY

###### 기능 구현 단계 #######
# 카카오톡 챗봇 프로그램을 구동하는데 필요한 모든 기능 함수화 해서
# 아래 2가지 함수에서 사용할 수 있도록 정리 
# 메인 함수 "mainChat", 답변/그림 요청 및 응답 확인 함수 "responseOpenAI"
# 메인 함수 

# 메세지 전송 (카카오톡 서버로 텍스트 전송)
# ChatGPT의 답변을 카카오톡 서버로 답변 전송 전용 JSON 형태(Format)의 데이터로 전달하기 위한 함수
# 카카오톡 채팅방에 보낼 메시지를 매개변수 bot_response에 input으로 받기(인자로 전달)
def textResponseFormat(bot_response):
    # 카카오톡 채팅방에 보낼 메시지가 저장된 매개변수 bot_response를
    # 아래 json 형태(Format)에서 항목 'outputs' -> 항목 "simpleText" -> "text"안에 매개변수 bot_response을 넣어서
    # 변수 responsedp 저장하기 
    response = {'version': '2.0', 
                'template': {
                    'outputs': [{"simpleText": {"text": bot_response}}], 
                    'quickReplies': []
                }
               }
    return response  # 카카오톡 서버로 답변 전송하기 위해 답변 전송 전용 JSON 형태(Format)의 데이터가 저장된 변수 response 리턴  

# 그림 전송 (카카오톡 서버로 그림 전송)
# DALLE.2가 생성한 그림 URL 주소를 카카오톡 서버로 이미지 전송 전용 JSON 형태(Format)의 데이터로 전달하기 위한 함수
# 카카오톡 채팅방에 보낼 DALLE.2가 생성한 그림 URL 주소를 
# 매개변수 bot_response에 input으로 받기(인자로 전달)
# DALLE.2가 그림을 생성할 때 input으로 넣은 프롬프트 문자열을 
# 매개변수 prompt에 input으로 받기(인자로 전달)
def imageResponseFormat(bot_response,prompt):
    output_text = prompt+"내용에 관한 이미지 입니다"
    # 카카오톡 채팅방에 보낼 DALLE.2가 생성한 그림 URL 주소가 저장된 매개변수 bot_response를
    # 아래 json 형태(Format)에서 항목 'outputs' -> 항목 "simpleImage" -> "imageUrl"안에 매개변수 bot_response을 넣어서
    # 변수 response에 저장하기 
    response = {'version': '2.0', 'template': {
    'outputs': [{"simpleImage": {"imageUrl": bot_response,"altText":output_text}}], 'quickReplies': []}}
    return response   # 카카오톡 서버로 DALLE.2가 생성한 그림 URL 주소 전송하기 위해  이미지 전송 전용 JSON 형태(Format)의 데이터가 저장된 변수 response 리턴  

# ChatGPT또는 DALLE.2의 답변(응답)이 3.5초 초과시 
# 지연 안내 메세지 + 버튼 생성
# 답변 시간이 지연되면 지연 안내 메시지를 보내고
# 답변을 다시 요청하기 위해서 FastAPI 비동기 웹서버에서 버튼 생성 요청하여 카카오톡 서버로 전달
# 카카오톡 서버에 버튼 생성 요청하기 위하여 버튼 생성 전용 JSON 형태(Format)의 데이터로 전달
def timeover():
    # 카카오톡 채팅방에 보낼 안내메시지는 
    # 아래 json 형태(Format)에서 항목 "outputs" -> 항목 "simpleText" -> 항목 "text" 안에 안내메시지 텍스트 "아직 제가 생각이 끝나지 않았어요🙏🙏\n잠시후 아래 말풍선을 눌러주세요👆" 저장
    # 카카오톡 채팅방에 보낼 생성할 버튼은
    # 아래 json 형태(Format)에서 항목 "quickReplies" 
    # -> 항목 "action"에 "message" 작성 
    # -> 항목 "label"에 "생각 다 끝났나요?🙋" 작성 (버튼 안에 들어가는 label)
    # -> 항목 "messageText"에 "생각 다 끝났나요?" 작성 (사용자가 이 버튼을 클릭했을 때 카카오톡 채팅방에 출력되는 입력 메시지)
    
    # 카카오톡 채팅방에 보낼 안내메시지, 생성할 버튼을 
    # 전용 json 형태(Format)의 데이터를 변수 response에 저장 
    response = {"version":"2.0","template":{
      "outputs":[
         {
            "simpleText":{
               "text":"아직 제가 생각이 끝나지 않았어요🙏🙏\n잠시후 아래 말풍선을 눌러주세요👆"
            }
         }
      ],
      "quickReplies":[
         {
            "action":"message",
            "label":"생각 다 끝났나요?🙋",
            "messageText":"생각 다 끝났나요?"
         }]}}
    return response   # 카카오톡 서버로 지연 안내메시지 + 생성할 버튼 전송하기 위해 JSON 형태(Format)의 데이터가 저장된 변수 response 리턴  

# ChatGPT에게 질문/답변 받기
# OpenAI API 사용해서 사용자가 ChatGPT에게 질문하고
# ChatGPT로 부터 답변받기
# 카카오톡 채팅방 안에서 사용자가 카카오톡 챗봇(ChatGPT)에게 질문을 하면
# 질문의 내용이 변수 prompt로 input돼서 해당 함수 getTextFromGPT 실행
def getTextFromGPT(prompt):   # ChatGPT한테 질문을 하게 될 프롬프트(prompt)를 함수 getTextFromGPT에 input으로 받기 
    # 카카오톡 챗봇(ChatGPT)에게 질문을 할때는 
    # 아래와 같은 시스템 프롬프트(System Prompt - [{"role": "system", "content": 'You are a thoughtful assistant. Respond to all input in 25 words and answer in korea'}])와 함께 질문
    # 시스템 프롬프트의 내용("content": 'You are a thoughtful assistant. Respond to all input in 25 words and answer in korea')이 
    # 의미하는 뜻은 "넌 훌륭한 도우미고 답변은 25자 내외로 한국어로 해줘." 이다.
    # 이렇듯 카카오톡 챗봇(ChatGPT)의 답변의 뉘앙스(응답 스타일)를 변경하고 싶은 경우 
    # 시스템 프롬프트의 내용("content": 'You are a thoughtful assistant. Respond to all input in 25 words and answer in korea')을
    # 개발자의 요구사항에 맞게 변경하면 된다.
    # ChatGPT API에서 요구하는 프롬프트(prompt) input 양식으로 변경 및 변경한 input 양식을 변수 messages_prompt에 저장 
    # messages_prompt = [{"role": "system", "content": 'You are a thoughtful assistant. Respond to all input in 25 words and answer in korea'}]
    messages_prompt = [{"role": "system", "content": 'You are a thoughtful assistant. Respond to all input in 25 words and answer in korea'}]
    messages_prompt += [{"role": "user", "content": prompt}]
    
    # openai.ChatCompletion.create 함수 파라미터 "messages"에 messages_prompt 저장
    # 함수 openai.ChatCompletion.create 호출 결과 최종적으로 ChatGPT API를 통해서 받은 응답을
    # response라는 변수에 저장 
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages_prompt)
    # response에서 ChatGPT의 응답 메시지 부분만 발췌를 해서(response["choices"][0]["message"])
    # 변수 system_message에 저장
    message = response["choices"][0]["message"]["content"]
    return message   # ChatGPT의 응답 메시지에 속한 답변 내용 부분(system_message["content"])만 발췌 및 리턴

# DALLE.2에게 질문/그림 URL 받기
# 생성된 그림의 URL 주소 받기
# 카카오톡 채팅방 안에서 사용자가 카카오톡 챗봇(ChatGPT)에게 그림 생성을 요청하면
# 요청한 내용이 변수 messages로 input돼서 해당 함수 getImageURLFromDALLE 실행
# DALLE.2 주의사항 
# 1. 특정 유명인 (예) 도널드 트럼프, 바이든 등등… 을 그림 그려달라고 요청 시 오류 발생 
#    참고 URL - https://community.openai.com/t/your-request-was-rejected-as-a-result-of-our-safety-system-your-prompt-may-contain-text-that-is-not-allowed-by-our-safety-system/285641
#    1번 오류 발생시 위의 ChatGPT로 부터 답변받기 함수 "getTextFromGPT" 몸체 안 변수 "messages_prompt"에 할당되는 시스템 프롬프트 문자열(항목 "content") 아래처럼 변경 후 컴파일 빌드 다시 실행 필요 
# (변경 전) messages_prompt = [{"role": "system", "content": 'You are a thoughtful assistant. Respond to all input in 25 words and answer in korea'}]
# (변경 후) messages_prompt = [{"role": "system", "content": 'You are a thoughtful assistant. Respond to all input in 100 words and answer in korea'}]
# 2. 영어가 아닌 한글로 그림 그려달라고 요청 시 요청사항과 전혀 다른 그림으로 그려줌.
# 3. 사용자가 그림 그려달라고 요청시 시간이 소요됨 (간단한 그림은 몇초 단위 / 복잡한 그림은 그 이상 시간 소요)
def getImageURLFromDALLE(prompt):
    # 사용자가 DALLE.2에게 그림 생성을 요청한 내용이 
    # 문자열로 저장된 변수 messages를 
    # 함수 openai.Image.create 에 전달하여 이미지 생성
    # 생성한 이미지에 대한 정보를 변수 response에 저장 
    # DALLE.2로 생성한 이미지의 사이즈(size)를 "512x512"로 설정
    response = openai.Image.create(prompt=prompt,n=1,size="512x512")
    # 이미지를 다운받을 수 있는 이미지 URL 주소(response['data'][0]['url'])를
    # 변수 image_url에 저장 
    image_url = response['data'][0]['url']
    return image_url   # 이미지를 다운받을 수 있는 이미지 URL 주소 리턴

# 텍스트파일 초기화
# 메인 함수 "mainChat", 답변/그림 요청 및 응답 확인 함수 "responseOpenAI"
# 해당 2가지 함수에서 3.5초 이후에 생성된 답변 및 그림 URL 주소를 
# 임시로 텍스트 파일에 저장 -> 해당 텍스트 파일에 저장된 정보는
# 추후에 사용자가 버튼("생각 다 끝났나요?🙋")을 클릭해서 
# 답변 및 그림 URL 주소를 요청하면
# 해당 답변 및 그림 URL 주소를 전송한 후에는 해당 텍스트 파일은 필요가 없다.
# 이 때 해당 함수 dbReset를 호출하여 저장된 텍스트 파일를 초기화 해준다.
def dbReset(filename):
    with open(filename, 'w') as f:
        f.write("")

###### 서버 생성 단계 #######
----- app = FastAPI()   # FastAPI 클래스 객체 app 생성 

# 위에서 생성한 객체 app 이라는 웹서버에 
# HTTP 통신 get() 메소드에 인자 "/" 전달 후 
# -> get() 메소드 호출시 메인 주소("/")로 접속 진행
# -> root 함수 실행 
# HTTP 통신 GET 메서드 형태(@app.get("/"))로 
# 개발자 FastAPI 로컬 비동기 웹서버에 메인주소("/")로 접속하면
# 아래 비동기 함수 root 실행
# 개발자 FastAPI 로컬 비동기 웹서버의 로컬 포트(Port)는 8000번으로 디폴트(default)로 설정
# 구글 크롬(Chrome) 웹브라우저에서 URL 주소 "http://localhost:8000/" 접속시
# 아래 비동기 함수 root 실행
@app.get("/")
async def root():
    # 크롬(Chrome) 웹브라우저 상에서 
    # URL 주소 "http://127.0.0.1:8000/"로 접속을 했을 때, 
    # 웹브라우저상에서 아래와 같은 메시지({"message": "kakaoTest"}) 출력
    return {"message": "kakaoTest"}

# 위에서 생성한 객체 app 이라는 웹서버에
# HTTP 통신 post() 메소드에 인자 "/chat/" 전달 후 
# -> post() 메소드 호출시 메인 주소 하위 주소("/chat/")로 접속 진행
# -> chat 함수 실행 -> 카카오톡 서버와 연결 진행
# 주의사항 - 일반 HTTP 통신 GET 방식으로 구글 크롬 웹브라우저 URL 접속하면 
#           (URL 주소 "http://127.0.0.1:8000/chat/) 아래와 같은 오류 메시지 출력
#           "405 Method Not Allowed"
#           왜냐면 post() 메소드로 호출하기 때문에 
#           구글 크롬 웹브라우저 URL 접속시에는 GET 방식이 아닌
#           POST 방식으로 접근해야 하기 때문이다.
#           하여 해당 오류를 해결하려면 카카오 API를 활용해서
#           아래 post() 메소드로 정보(데이터)를 주고 받을 수 있도록 해야한다.
# HTTP 통신 POST 메서드 형태(@app.post("/chat/"))로 
# 개발자 FastAPI 로컬 비동기 웹서버에 메인주소 + /chat/ 주소("/chat/")로 접속하면
# 아래 비동기 함수 chat 실행
# 개발자 FastAPI 로컬 비동기 웹서버의 로컬 포트(Port)는 8000번으로 디폴트(default)로 설정
# 구글 크롬(Chrome) 웹브라우저에서 URL 주소 "http://localhost:8000/chat/" 접속시
# 아래 비동기 함수 chat 실행
@app.post("/chat/")
# 카카오톡 채팅방에 사용자가 채팅을 새로 입력했을 때
# 챗봇의 모든 기능을 실행할 수 있는 함수 chat
# 사용자가 채팅을 새로 입력했을 때 새로운 입력에 대한 정보를
# 매개변수 request로 인자를 전달 받는다.
async def chat(request: Request):
    # 카카오톡 채팅방에서 사용자가 채팅 입력 
    # -> 해당 채팅에 대한 정보가 카카오톡 서버 -> ngrok 프로그램을 지나서 
    # -> 해당 FastAPI 웹서버 URL 주소 "/chat"로 넘어오고 
    # -> 함수 chat 실행 -> print 함수 호출 -> 카카오톡 채팅 정보가 터미널창에 출력
    # 쉽게 말해서 카카오톡 채팅방에 채팅이 입력될 때마다
    # 해당 chat 함수 실행되서 
    # 카카오톡 챗봇의 모든 기능 실행할 수 있는 메인함수 mainChat이 실행된다.
    # 메인함수 mainChat이 실행될 때는 카카오톡 채팅방에
    # 방금 전에 사용자가 입력한 채팅의 정보가 넘어오면서 메인함수 mainChat이 실행된다.

    # 카카오톡 채팅에서 날라온 채팅 정보를 json 데이터 형태(Format)로 정리(request.json())해서 변수 kakaorequest에 저장
    kakaorequest = await request.json()
    # 사용자의 요청에 맞는 카카오톡 챗봇의 모든 기능 실행할 수 있는 메인함수 mainChat에
    # 위의 변수 kakaorequest를 인자로 전달 
    # 해당 mainChat 함수는 최종적으로 사용자의 요청에 맞는 json 데이터를 반환해서 리턴해준다.
    # 해당 mainChat 함수 실행 결과 리턴된 jsom 데이터가 
    # 비동기 함수 chat에서 또 리턴이 돼서
    # 최종적으로는 카카오톡 서버로 답변 및 DALLE.2가 그려준 그림 URL 주소를 전송해줌.
    return mainChat(kakaorequest)

###### 메인 함수 단계 #######

# 멀티스레드 작업 처리를 해야해서 아래 2가지 함수 구현
# 메인 함수 "mainChat", 답변/그림 요청 및 응답 확인 함수 "responseOpenAI"

# 메인 함수
# 카카오 챗봇의 중심이 되는 함수로 
# 간략하게 설명하자면 답변/그림 요청 및 응답 확인 함수 "responseOpenAI"의 응답시간을
# 측정해서 바로 답변을 할 것인지 버튼을 생성해서 재요청 할 것인지를 판단하는 기능을 수행한다.
# 답변/그림 요청 및 응답 확인 함수 "responseOpenAI"로 부터 제한시간 3.5초 내에 답변이 오면
# 카카오톡 서버로 바로 답변/사진을 전달하고 
# 만약에 응답 제한시간 3.5초 초과하면 위에서 구현한 timeover 함수가 호출되서
# 카카오톡 채팅방으로 버튼을 생성하고 안내메시지를 보내주게 된다.
def mainChat(kakaorequest):

    # 답변/그림 응답 제한시간 3.5초내에 답변/그림이 완성이 됐는지 여부를 저장하기 위한 변수 run_flag 선언 및 초기화
    # 변수 run_flag 값이 True면 "답변/그림이 응답 제한시간 3.5초내에 완성" 의미
    # 변수 run_flag 값이 False면  "답변/그림이 응답 제한시간 3.5초 초과 및 미완성" 의미
    run_flag = False  
    start_time = time.time()   # 답변/그림 응답시간 계산하기 위해 답변/그림을 시작하는 시간을 변수 start_time에 저장 

    # 응답 결과를 저장하기 위한 텍스트 파일 생성
    # ChatGPT의 답변 결과와 DALLE.2의 이미지 URL 주소를
    # 잠시 저장하기 위한 텍스트 파일(.txt)을 파이썬 파일(test_kakaobot.py)과 같은 경로 안에
    # 텍스트 파일(.txt) "botlog.txt" 파일 이름으로 생성함.
    cwd = os.getcwd() # 파이썬 파일(test_kakaobot.py) 경로를 변수 cwd에 저장  
    filename = cwd + '/botlog.txt'  # 파이썬 파일(test_kakaobot.py) 경로에 '/botlog.txt' 파일 이름 생성하여 변수 filename에 저장 

    # 만약에 해당 텍스트 파일 (/botlog.txt)이 
    # 파이썬 파일(test_kakaobot.py) 경로에 없다면  
    if not os.path.exists(filename):
        # open 함수 사용하여 해당 텍스트 파일 (/botlog.txt) 쓰기모드("w")로 생성 
        with open(filename, "w") as f:
            f.write("")   # 처음에는 아무 것도 없는 값으로 해당 텍스트 파일 (/botlog.txt) 초기화 
    # 만약에 해당 텍스트 파일 (/botlog.txt)이 
    # 파이썬 파일(test_kakaobot.py) 경로에 있다면  
    else:
        print("File Exists") # print 함수 호출하여 지금 현재 파일이 있다고 메시지 "File Exists" 출력 

    # 답변 생성 함수 실행
    # ChatGPT 답변과 DALLE.2가 그려준 그림의 URL 주소를 
    # 변수 response_queue에 저장하고 해당 변수에 저장된 값을
    # 카카오톡 채팅방에 답변으로 전송할 때마다 .get() 메서드를 활용해서 
    # 자료(데이터)를 꺼내서 사용한다.
    # 큐 자료구조 클래스 q.Queue를 객체 response_queue 생성 및 초기화
    # 여기서 자료구조 큐는 리스트와 비슷하게 여러 자료(데이터)를 쌓을 수 있는 자료 구조 형태이다.
    # 자료구조 큐에서 알아야 할 메서드는 2가지가 있다.
    # .put() 메서드 - 큐에 자료(데이터)를 차곡차곡 저장하는 기능
    # .get() 메서드 - 큐에 가장 먼저 저장된 자료부터 하나씩 꺼낼 수 있는 기능
    #                .get() 메서드 사용해서 저장된 자료(데이터)를 꺼내면 해당 자료(데이터)는 큐에서 자동으로 삭제 처리 
    response_queue = q.Queue()   #.put(), .get()
    # 패키지 "threading"을 활용해서 
    # 멀티스레드 작업스레드 객체 request_respond 생성 및 함수 responseOpenAI를 실행한다.
    # 패키지 "threading"을 이용해 request_respond.start() 함수 호출
    # -> 함수 responseOpenAI를 실행하면
    # 해당 함수 responseOpenAI가 끝날 때 까지 기다리지 않고
    # 바로 아래 답변 생성 시간 체크 소스코드 (while (time.time() - start_time < 3.5):)가 실행된다.
    request_respond = threading.Thread(target=responseOpenAI,
                                        args=(kakaorequest, response_queue,filename))
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
        # 0.1초에 한번씩 큐 자료구조 response_queue에 답변/그림이 담겨 있는지 확인
        # 만약 시작시간(start_time)으로 부터 
        # 응답 제한시간 3.5초내로 답변/그림이 생성된 경우(조건문 if not response_queue.empty(): 만족한 경우(True))
        if not response_queue.empty():
            # 시작시간(start_time)으로 부터 응답 제한시간 3.5초 안에 답변/그림이 완성(생성)되면 바로 값 리턴
            # 자료구조 response_queue에 저장된 답변/그림을 꺼내서 변수 response에 저장  
            response = response_queue.get()
            run_flag= True   # 변수 run_flag 값 True 할당 "답변/그림이 응답 제한시간 3.5초내에 완성" 의미
            break   # while 반복문 종료 
        # 안정적인 구동을 위한 딜레이 타임 설정
        # 아래처럼 time.sleep(0.01) 호출하여 0.01초씩 딜레이 타임을 주지 않으면
        # 너무 빨리 돌아서 카카오 챗봇 프로그램이 가끔 종료되는 현상이 발생한다.
        # 하여 카카오 챗봇 프로그램의 안정적인 구동을 위해서
        # time.sleep(0.01) 함수를 호출한다.
        time.sleep(0.01)  

    # 3.5초 내 답변/그림이 생성되지 않을 경우 
    # (위의 while문의 조건문 if not response_queue.empty(): 만족하지 않은 경우)
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
def responseOpenAI(request,response_queue,filename):
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
        # 텍스트 파일('/botlog.txt')에 저장된 내용을 꺼내서 .put 메서드 활용해서 큐 자료구조 response_queue에 저장  
        with open(filename) as f:
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
                # 해당 함수 imageResponseFormat 실행 결과 리턴된 값을 put 메서드 활용해서 큐 자료구조 response_queue에 저장 
                response_queue.put(imageResponseFormat(bot_res,prompt))
            # 해당 텍스트 파일('/botlog.txt')에 저장된 정보(데이터)가 ChatGPT 답변인 경우 
            else:
                # 변수 bot_res는 ChatGPT 답변 문자열이 저장된 변수이다.
                bot_res = last_update[4:]
                print(bot_res)
                # 함수 textResponseFormat에 해당 변수 bot_res에 저장된 값을 인자로 전달하고 
                # 해당 함수 textResponseFormat 실행 결과 리턴된 값을 put 메서드 활용해서 큐 자료구조 response_queue에 저장 
                response_queue.put(textResponseFormat(bot_res))
            dbReset(filename)  # 함수 dbReset 실행하여 텍스트 파일('/botlog.txt')에 저장된 ChatGPT 답변 또는 DALLE.2에서 받은 그림의 URL 주소 초기화 

    # 이미지 생성을 요청한 경우
    # 만약 그림 생성을 요청하면
    # 만약 카카오톡 채팅방에 사용자가 입력한 메시지 안에
    # '/img'란 문자열이 포함되어 있으면,  
    # 즉, DALLE.2에게 그림 생성을 요청한 경우 
    elif '/img' in request["userRequest"]["utterance"]:
        dbReset(filename)   # 함수 dbReset 실행하여 텍스트 파일('/botlog.txt')에 저장된 ChatGPT 답변 또는 DALLE.2에서 받은 그림의 URL 주소 초기화
        # replace 메서드 호출하여 텍스트 메시지 안에 "/img" 란 단어를 
        # 공백("")으로 변경한 나머지 사용자의 질문 내용 프롬프트 문자열을 추출해서 변수 prompt에 저장 
        prompt = request["userRequest"]["utterance"].replace("/img", "")
        # 함수 getImageURLFromDALLE 호출하여 DALLE.2에게 그림 생성 요청을 해서
        # 최종적으로 DALLE.2가 생성한 그림의 URL주소를 변수 bot_res에 저장 
        bot_res = getImageURLFromDALLE(prompt)
        # 함수 imageResponseFormat에 변수 bot_res,prompt를 인자로 전달하여 
        # DALLE.2가 생성한 그림 URL 주소값이 포함되어 카카오톡 서버로 전송할 그림 생성 전용 json 형태(Format)를 작성 및 리턴 
        # put 메서드 호출하여 최종적으로 큐 자료구조 response_queue에 저장함.
        response_queue.put(imageResponseFormat(bot_res,prompt))
        # DALLE.2가 생성한 그림 URL 주소 정보를 텍스트 파일('/botlog.txt') 변수 save_log에 저장함 
        # 변수 save_log에 저장하는 이유는 그림을 그리는게 응답 제한시간 3.5초 내로 완료가 안 됐으면
        # 우선은 DALLE.2가 생성한 그림 URL 주소를 텍스트 파일('/botlog.txt')에 임시로 저장을 해놓기 위해서 
        # 변수 save_log 선언 및 DALLE.2가 생성한 그림 URL 주소 할당 후 
        # 텍스트 파일('/botlog.txt')에 임시로 저장함.
        save_log = "img"+ " " + str(bot_res) + " " + str(prompt)
        with open(filename, 'w') as f:
            f.write(save_log)

    # ChatGPT 답변을 요청한 경우
    # 만약 chatGPT의 답변을 요청하면
    # 만약 카카오톡 채팅방에 사용자가 입력한 메시지 안에
    # '/ask'란 문자열이 포함되어 있으면,  
    # 즉, ChatGPT에게 답변을 요청한 경우 
    elif '/ask' in request["userRequest"]["utterance"]:
        dbReset(filename)   # 함수 dbReset 실행하여 텍스트 파일('/botlog.txt')에 저장된 ChatGPT 답변 또는 DALLE.2에서 받은 그림의 URL 주소 초기화
        
        # replace 메서드 호출하여 텍스트 메시지 안에 "/ask" 란 단어를 
        # 공백("")으로 변경한 나머지 사용자의 질문 내용 프롬프트 문자열을 추출해서 변수 prompt에 저장 
        prompt = request["userRequest"]["utterance"].replace("/ask", "")
        # 함수 getTextFromGPT 호출하여 ChatGPT에게 질문 요청을 해서
        # 최종적으로 ChatGPT의 답변을 변수 bot_res에 저장 
        bot_res = getTextFromGPT(prompt)
        # 함수 imageResponseFormat에 변수 bot_res를 인자로 전달하여 
        # ChatGPT의 답변이 포함되어 카카오톡 서버로 전송할 ChatGPT의 답변 전용 json 형태(Format)를 작성 및 리턴 
        # put 메서드 호출하여 최종적으로 큐 자료구조 response_queue에 저장함.
        response_queue.put(textResponseFormat(bot_res))
        print(bot_res)
        # ChatGPT의 답변 정보를 텍스트 파일('/botlog.txt') 변수 save_log에 저장함 
        # 변수 save_log에 저장하는 이유는 ChatGPT의 답변을 얻는데 응답 제한시간 3.5초 내로 완료가 안 됐으면
        # 우선은 ChatGPT의 답변을 텍스트 파일('/botlog.txt')에 임시로 저장을 해놓기 위해서 
        # 변수 save_log 선언 및 ChatGPT의 답변 내용 할당 후 
        # 텍스트 파일('/botlog.txt')에 임시로 저장함.
        save_log = "ask"+ " " + str(bot_res)

        with open(filename, 'w') as f:
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
        # put 메서드 활용해서 큐 자료구조 response_queue에 저장 
        response_queue.put(base_response) 