"""
* OpenAI 전용 유틸(util) openai==0.28.1

*** 참고 ***
*** ChatGPT 문서 ***
* ChatGPT 텍스트 응답 메시지
참고 URL - https://github.com/openai/openai-python

*** 파이썬 문서 ***
* urllib
참고 URL - https://docs.python.org/ko/3.13/library/urllib.html
참고 2 URL - https://docs.python.org/ko/3.13/library/urllib.request.html#module-urllib.request
참고 3 URL - https://docs.python.org/ko/3.13/library/urllib.request.html#legacy-interface
"""

##### 패키지 불러오기 #####
from utils import google_util   # Google 전용 유틸(util)

import openai
import urllib   # URL 처리

##### 기능 구현 함수 #####
##### 프로그램 내에서 ChatGPT한테 물어보거나 내용 번역 또는 요약 지시하거나 하는 그러한 기능들을 깔끔하게 함수화해서 정리
def get_response(messages_prompt: list[dict]) -> str:
    """
    Description: ChatGPT 텍스트 응답 메시지 가져오기

    Parameters: messages_prompt - 개발자가 요구하는 ChatGPT API 시스템 프롬프트(prompt) input 양식

    Returns: msg - ChatGPT 텍스트 응답 메시지
    """

    response = openai.ChatCompletion.create(model='gpt-3.5-turbo', messages=messages_prompt)  # ChatGPT 응답 받기 및 response 변수 저장

    msg = response["choices"][0]["message"]["content"]   # ChatGPT 텍스트 응답 메시지 msg 변수 저장
    return msg

def image_url_dalle2(prompt: str) -> str:
    """
    Description: DALLE.2 이미지 생성 및 URL 주소 가져오기

    Parameters: prompt - 사용자 작성 내용

    Returns: image_url - 이미지 URL 주소
    """

    response = openai.Image.create(prompt=prompt,n=1,size="512x512")   # 이미지 생성 및 response 변수 저장

    image_url = response['data'][0]['url']   # 이미지 URL 주소(response['data'][0]['url']) image_url 변수 저장
    return image_url   # 이미지 다운로드 받을 수 있는 URL 주소 리턴


def downLoad_image_dalle2(topic: str, mood: str) -> None:
    """
    Description: DALLE.2 이미지 생성 및 다운로드

    Parameters: topic - 주제
                mood - 분위기

    Returns: 없음.
    """

    # 한글 -> 영어 번역
    t_topic = google_util.translate(topic, "en")   # 주제
    t_mood = google_util.translate(mood, "en")     # 분위기
    

    # f'~~~~~' - 시스템 프롬프트와 t_topic, t_mood 변수 합쳐서 구현.
    # 시스템 프롬프트 문자열
    # 1. 해당 주제에 대해서 그림 그리기 (Draw picture about {t_topic})
    # 2. 그림의 분위기는 다음과 같다. (picture Mood is {t_mood}')
    image_prompt = f'Draw picture about {t_topic}. picture Mood is {t_mood}'
    print(image_prompt)

    response = openai.Image.create(prompt=image_prompt, n=1, size="512x512")   # 이미지 생성 및 response 변수 저장

    image_url = response['data'][0]['url']  # 이미지 URL 주소(response['data'][0]['url']) image_url 변수 저장
    urllib.request.urlretrieve(image_url, "insta_image.jpg")  # 해당 이미지 다운로드 및 "insta_image.jpg" 파일명 저장