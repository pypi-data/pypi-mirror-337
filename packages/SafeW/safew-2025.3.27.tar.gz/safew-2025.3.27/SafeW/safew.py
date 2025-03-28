import requests
import json
'''Its a demo-free module, However you may cause a lot of errors, report bugs to owner telegram username.'''
class SafeWBot:
    def __init__(self, token: str):
        self.base_url = f"https://api.safew.org/bot{token}/"

    def call_method(self, method: str, params: dict = None, use_post: bool = False):
        url = self.base_url + method
        params = params or {}

        try:
            response = requests.post(url, json=params) if use_post else requests.get(url, params=params)
            data = response.json()

            if not data.get("ok"):
                raise Exception(f"API Error {data.get('error_code')}: {data.get('description')}")

            return data.get("result")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request Failed: {e}")

    def get_me(self):
        return self.call_method("getMe")

    def get_updates(self, offset=None, limit=None, timeout=None, **kwargs):
        return self.call_method("getUpdates", {"offset": offset, "limit": limit, "timeout": timeout, **kwargs})

    def get_chat(self, chat_id):
        return self.call_method("getChat", {"chat_id": chat_id})

    def send_message(self, chat_id, text, **kwargs):
        return self.call_method("sendMessage", {"chat_id": chat_id, "text": text, **kwargs}, use_post=True)

    def send_photo(self, chat_id, photo, **kwargs):
        return self.call_method("sendPhoto", {"chat_id": chat_id, "photo": photo, **kwargs}, use_post=True)

    def send_video(self, chat_id, video, **kwargs):
        return self.call_method("sendVideo", {"chat_id": chat_id, "video": video, **kwargs}, use_post=True)

    def send_audio(self, chat_id, audio, **kwargs):
        return self.call_method("sendAudio", {"chat_id": chat_id, "audio": audio, **kwargs}, use_post=True)

    def send_document(self, chat_id, document, **kwargs):
        return self.call_method("sendDocument", {"chat_id": chat_id, "document": document, **kwargs}, use_post=True)

    def send_voice(self, chat_id, voice, **kwargs):
        return self.call_method("sendVoice", {"chat_id": chat_id, "voice": voice, **kwargs}, use_post=True)

    def set_webhook(self, url, **kwargs):
        return self.call_method("setWebhook", {"url": url, **kwargs}, use_post=True)

    def edit_message_text(self, chat_id, message_id, text, **kwargs):
        return self.call_method("editMessageText", {"chat_id": chat_id, "message_id": message_id, "text": text, **kwargs}, use_post=True)