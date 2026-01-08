"""
* 파파고 전용 유틸(util)

*** 참고 ***
*** 파이썬 문서 ***

"""

import requests   # HTTP 요청(파파고 API 서비스)

##### 기능 구현 함수 #####

# def translate(messages, papago_id, papago_pw):
#     """
#     Description: 파파고 번역

#                  *** 주의사항 ***
#                  파파고 API 서비스 종료로 인해 실제로 사용하지 않는 함수

#     Parameters: messages - 사용자 작성 번역 요청 내용
#                 papago_id - 파파고 API ID
#                 papago_pw - 파파고 API PW

#     Returns: trans_messages - 번역 내용
#     """

#     data = {
#               'text' : messages,
#               'source' : 'en',
#               'target': 'ko'
#            }

#     url = "https://openapi.naver.com/v1/papago/n2mt"

#     header = {
#                "X-Naver-Client-Id": papago_id,
#                "X-Naver-Client-Secret": papago_pw
#              }

#     response = requests.post(url, headers=header, data=data)   # HTTP 통신(post)
#     status_code = response.status_code

#     if 200 == status_code:   # HTTP 통신 성공
#         send_data = response.json()
#         trans_messages = (send_data['message']['result']['translatedText'])
#         return trans_messages
#     else:   # HTTP 통신 실패
#         print("Error Code:" , status_code)