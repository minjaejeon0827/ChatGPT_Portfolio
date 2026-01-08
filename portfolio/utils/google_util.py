"""
* Google 전용 유틸(util)

*** 참고 ***
*** 파이썬 문서 ***
* 구글 번역기 오픈 소스 패키지 googletrans
참고 URL - https://pypi.org/project/googletrans/
"""

##### 패키지 불러오기 #####
from googletrans import Translator   # 구글 번역기

def translate(messages: str, lang_type: str) -> str:
    """
    Description: 구글 번역 (DALLE2 이미지 생성 용도 포함)

                 *** 참고 ***
                 현재 DALLE2에서 한글 텍스트 사용시 이미지가 엉망진창으로 생성됨.
                 왜냐면 아직 한글에 대한 학습이 원활하지 않는 것으로 확인.
                 하여 한글 -> 영어 번역한 텍스트 사용해서 DALLE2 이미지 생성함.

    Parameters: messages - 사용자 작성 내용 (주제, 분위기, 번역 내용 등등...)
                lang_type - 번역 언어 타입 (한글 -> 영어 번역 (dest="en") 참고: 영어 -> 한글 번역 (dest="ko"))

    Returns: result.text - 번역 내용
    """

    google = Translator()
    result = google.translate(messages, dest=lang_type)

    return result.text   # 번역 내용 리턴