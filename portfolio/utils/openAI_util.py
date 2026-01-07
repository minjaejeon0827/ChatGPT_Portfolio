"""
* OpenAI 전용 유틸 (util) openai==0.28.1
"""

import openai

##### 기능 구현 함수 #####
##### 프로그램 내에서 ChatGPT한테 물어보거나 내용 번역 또는 요약 지시하거나 하는 그러한 기능들을 깔끔하게 함수화해서 정리
def ask_gpt(prompt: str) -> str:
    """
    Description: ChatGPT 텍스트 응답 메시지 가져오기

    Parameters: prompt - 사용자 질문 내용

    Returns: msg - ChatGPT 텍스트 응답 메시지
    """

    messages_prompt = [{"role": "system", "content": prompt}]   # ChatGPT API에게 개발자가 요구하는 prompt input 양식 변경 및 해당 input 양식을 messages_prompt 변수 저장
    response = openai.ChatCompletion.create(model='gpt-3.5-turbo', messages=messages_prompt)  # ChatGPT 응답 받기 및 response 변수 저장

    msg = response["choices"][0]["message"]["content"]   # ChatGPT 텍스트 응답 메시지 msg 변수 저장
    return msg