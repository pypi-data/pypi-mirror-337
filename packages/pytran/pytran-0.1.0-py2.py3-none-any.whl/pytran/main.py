import requests
from .cache import cached

class Translator:
    BASE_URL = "https://api.mymemory.translated.net/get"
    
    def __call__(self, text: str, from_lang: str = "auto", to_lang: str = "en") -> str:
        return self.translate(text, from_lang, to_lang)
    
    @staticmethod
    @cached
    def translate(text: str, from_lang: str = "auto", to_lang: str = "en") -> str:
        params = {
            "q": text,
            "langpair": f"{from_lang}|{to_lang}"
        }
        response = requests.get(Translator.BASE_URL, params=params)
        if response.status_code == 200:
            return response.json().get("responseData", {}).get("translatedText", "Translation Error")
        return "API Request Failed"