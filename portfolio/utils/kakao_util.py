"""
* KAKAO 전용 유틸(util)

*** 참고 ***
* 챗봇 응답 타입별 json 포맷
참고 URL - https://kakaobusiness.gitbook.io/main/tool/chatbot/skill_guide/answer_json_format

* 카카오 응답 json 포맷 "buttons" VS "quickReplies" 차이점
- "quickReplies"의 경우 "action": "webLink" 기능 실행 불가.

*** 파이썬 문서 ***
* Type Hints
참고 URL - https://docs.python.org/ko/3.14/library/typing.html
참고 2 URL - https://peps.python.org/pep-0484/
참고 3 URL - https://devpouch.tistory.com/189
참고 4 URL - https://supermemi.tistory.com/entry/Python-3-%ED%8C%8C%EC%9D%B4%EC%8D%AC%EC%97%90%EC%84%9C-%EC%9D%98%EB%AF%B8%EB%8A%94-%EB%AC%B4%EC%97%87%EC%9D%BC%EA%B9%8C-%EC%A3%BC%EC%84%9D

* Type Hints class Any
참고 URL - https://docs.python.org/ko/3.9/library/typing.html#the-any-type

"""

from typing import Any   # Type Hints class

def skillResponse_format(outputs: list[dict], quickReplies: list[dict] | None = None) -> dict[str, Any]:
    """
    Description: 스킬 응답 json 포맷

    Parameters: outputs - 출력 그룹 리스트
                quickReplies - 바로가기 그룹 버튼 리스트 (label + messageText)

    Returns: 스킬 응답 json 포맷
    """
    
    if None is quickReplies: quickReplies = []

    return {
        "version": "2.0",
        "template": {
            "outputs": outputs,
            "quickReplies": quickReplies
        },
        # TODO: 아래 주석친 코드 필요시 참고 (2025.11.24 minjae)
        # "context": {
        #     "values": []
        # },
        # "data": {
        #     "msg": "안녕하세요.",
        #     "name": "상진",
        #     "position": "Autodesk 기술지원 챗봇"
        # }
    }

def simple_text(text: str | None = None) -> dict[str, Any]:
    """
    Description: 텍스트 메시지 (text) 카카오톡 채팅방 전송

    Parameters: text - 챗봇 답변 메시지

    Returns: skillResponse_format(outputs) - 텍스트 메시지 json 포맷
    """

    outputs = []

    if text:   # text에 할당된 값이 None 또는 공백("")이 아닌 경우 (None or Empty String Check)
        outputs.append({
            "simpleText": {
                "text": text
            }
        })
            
    return skillResponse_format(outputs)

    
def simple_image(prompt: str, image_url: str | None = None) -> dict[str, Any]:
    """
    Description: DALLE2 이미지 (image_url) 카카오톡 채팅방 전송

    Parameters: prompt - 사용자가 카카오톡 채팅방에 그려 달라고 요청한 이미지 설명
                image_url - DALLE2 이미지 URL 주소
        
    Returns: skillResponse_format(outputs) - DALLE2 이미지 json 포맷
    """

    outputs = []
    output_text = prompt + "내용에 관한 이미지 입니다"

    if image_url:   # image_url에 할당된 값이 None 또는 공백("")이 아닌 경우 (None or Empty String Check)
        outputs.append({
            "simpleImage": {
                "image_url": image_url,
                "altText": output_text
            }
        })

    return skillResponse_format(outputs)

def timeOver_quickReplies() -> dict[str, Any]:
    """
    Description: 챗봇 응답 시간 5초 초과시 응답 재요청 메세지 카카오톡 채팅방 전송

    Parameters: 없음.

    Returns: skillResponse_format(outputs, quickReplies) - 응답 재요청 메세지 json 포맷
    """

    outputs = []
    quickReplies = []

    outputs.append({
        "simpleText": {
            "text": '요청사항 확인 중이에요.\n잠시후 아래 말풍선을 눌러주세요.'   # 챗봇 응답 시간 5초 초과시 응답 (바로가기 그룹 전송)
        }
    })

    quickReplies.append({
        "action": 'message',   # 사용자의 발화로 messageText 실행. (바로가기 응답의 메세지 연결 기능과 동일)
        "label": '생각 다 끝났나요?',   # 챗봇 응답 시간 5초 초과한 경우 챗봇 응답 메시지
        "messageText": '생각 다 끝났나요?'
    })

    return skillResponse_format(outputs, quickReplies)

def empty_response() -> dict[str, Any]:
    """
    Description: 비어있는 응답 메세지 카카오톡 채팅방 전송 (답변/그림 요청 외 나머지 일반 채팅일 경우)

    Parameters: 없음.

    Returns: skillResponse_format(outputs) - 비어있는 응답 메세지 json 포맷
    """

    outputs = []

    return skillResponse_format(outputs)
