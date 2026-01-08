"""
* PAPAGO 전용 유틸(util)

*** 참고 ***
*** 파이썬 문서 ***

"""

import requests   # HTTP 요청(PAPAGO API 서비스)

##### 기능 구현 함수 #####

def translate(messages, papago_id, papago_pw, lang_type: str) -> str | None:
    """
    Description: PAPAGO 번역

                 *** 주의사항 ***
                 PAPAGO API 서비스 종료로 인해 실제로 사용하지 않는 함수

    Parameters: messages - 사용자 작성 번역 요청 내용
                papago_id - PAPAGO API ID
                papago_pw - PAPAGO API PW
                lang_type - 번역 언어 타입 (한글 -> 영어 번역 ('target': "en") 참고: 영어 -> 한글 번역 ('target': "ko"))

    Returns: trans_messages - 번역 내용
    """

    data = {
              'text' : messages,
              'source' : 'en',
              'target': lang_type
           }

    url = "https://openapi.naver.com/v1/papago/n2mt"

    header = {
               "X-Naver-Client-Id": papago_id,
               "X-Naver-Client-Secret": papago_pw
             }

    response = requests.post(url, headers=header, data=data)   # HTTP 통신(post)
    status_code = response.status_code

    trans_messages = None   # 번역 내용 초기화

    if 200 == status_code:   # HTTP 통신 성공
        send_data = response.json()
        trans_messages = (send_data['message']['result']['translatedText'])

    else:   # HTTP 통신 실패
        print("Error Code:" , status_code)
    
    return trans_messages