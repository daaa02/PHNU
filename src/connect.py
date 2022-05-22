from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.text_to_speech_v1 import TextToSpeechV1
import os
import time
import requests

# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms

HIGH = 1
LOW = 0


def isNumber(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


class Connection:
    def __init__(self):
        # speech to text variants
        # self.kakao_account = 'f8f8c3f66bb3310016fdeccffba152e8'
        # os.system(f'gpio mode 7 out;gpio write 7 {HIGH}')

        self.STREAMING_LIMIT = 240000  # 4 minutes
        self.SAMPLE_RATE = 16000
        self.CHUNK_SIZE = int(self.SAMPLE_RATE / 10)  # 100ms

        self.RED = '\033[0;31m'
        self.GREEN = '\033[0;32m'
        self.YELLOW = '\033[0;33m'

        self.user_words = ''

    def assistant_connect(self, assistant_id):
        # dyk984@daum.net        
        authenticator = IAMAuthenticator('cQ1ex-J86yeMMtpqz9d78ZEuyO_zFl343mpy2cQ0CyD6')
        assistant_id = '2403128d-0671-4f67-8a12-1c8999bf2256'
        assistant = AssistantV2(
            version='2021-06-14',
            authenticator = authenticator
        )

        assistant.set_service_url('https://api.kr-seo.assistant.watson.cloud.ibm.com/instances/be52c633-3f03-4387-8837-0ab0fa90c952')

        response = assistant.create_session(
            assistant_id= assistant_id
        ).get_result()
        
        session_id = response['session_id']
        return assistant, session_id        



    # kakao tts api
    def tts(self, string, filename="tts.wav"):

        if self.kakao_account in [None, '']:
            raise Exception('Kakao account invalid')

        url = "https://kakaoi-newtone-openapi.kakao.com/v1/synthesize"
        headers = {
            'Content-Type': 'application/xml',
            'Authorization': 'KakaoAK ' + self.kakao_account
        }
        r = requests.post(url, headers=headers, data=string.encode('utf-8'))
        with open(filename, 'wb') as f:
            f.write(r.content)

    # kakao tts play
    def play(self, filename, out='local', volume='-2000.0', background=True):

        if not os.path.isfile(filename):
            raise Exception(f'"{filename}" does not exist')

        if not filename.split('.')[-1] in ['mp3', 'wav']:
            raise Exception(f'"{filename}" must be (mp3|wav)')

        if not out in ['local', 'hdmi', 'both']:
            raise Exception(f'"{out}" must be (local|hdmi|both)')

        if not isNumber(volume):
            raise Exception(f'"{volume}" is not Number')

        if type(background) != bool:
            raise Exception(f'"{background}" is not bool')

        opt = '&' if background else ''
        os.system(f'omxplayer -o {out} --vol {volume} {filename} {opt}')
