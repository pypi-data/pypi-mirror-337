import re

class TEXTISM:
    mapping = {
        "ㄱ" : "고",
        "ㄴ": "노",
        "ㄷ": "덜",
        "ㅂ" : "바",
        "ㅇ": "응",
        "ㅈ": "지",
        "ㅉ": "쯧",
        "ㅋ": "크",
        "ㅎ": "하",
        "ㄱㅊ": "괜찮",
        "ㄱㄷ": "기달",
        "ㄲㅈ": "꺼져",
        "ㄱㅅ": "감사",
        "700": "귀여워",
        "ㄷㄹ": "들림",
        "ㄷㅊ": "닥쳐",
        "ㄹㄷ": "레디",
        "ㅁㄹ": "몰라",
        "ㅅㄱ": "수고",
        "ㅇㄷ": "어디",
        "ㅇㅋ": "오키",
        "ㅈㅅ": "죄송",
        "ㅊㅋ": "추카",
        "ㅈㅁ": "잠만",
        "ㅇㅈ": "인정",
        "ㅎㅇ": "하이",
        "ㅋㄷ": "키득",
        "ㅎㄹ": "헐",
        "ㄷㅈㄷ": "디진다",
        "ㄱㅇㅇ": "귀여워",
        "ㅇㅂㅇ": "입버릇",
        "ㅇㄱㄹㅇ": "이거레알",
        "ㅠ": "유"
    }

    @staticmethod
    def convert(word: str) -> str:
        """단일 단어 변환"""
        return TEXTISM.mapping.get(word, word)

    @staticmethod
    def convert_message(message: str) -> str:
        """문장에서 mapping에 해당하는 단어를 변환"""
        words = message.split()  # 공백 기준으로 단어 분리
        converted_words = [TEXTISM.convert(word) for word in words]  # 변환된 단어 리스트 생성
        return " ".join(converted_words)
