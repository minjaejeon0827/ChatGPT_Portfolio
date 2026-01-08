"""
* Deepl 전용 유틸(util)

*** 참고 ***
*** 파이썬 문서 ***

"""

##### 패키지 불러오기 #####
import deepl   # Deepl 번역기

def translate(messages, deepl_api, lang_type):
    """
    Description: Deepl 번역

    Parameters: messages - 사용자 작성 번역 내용
                deepl_api - DeepL API
                lang_type - 번역 언어 타입 (한글 -> 영어 번역 (target_lang="EN") 참고: 영어 -> 한글 번역 (target_lang="KO"))

    Returns: result.text - 번역 내용
    """
    translator = deepl.Translator(deepl_api)
    result = translator.translate_text(messages, target_lang=lang_type)
    return result.text