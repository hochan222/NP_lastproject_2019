from slacker import Slacker
import os, json
from django.core.exceptions import ImproperlyConfigured

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOKEN = []

secret_file = os.path.join(BASE_DIR, 'secret', 'slack_token.json')

with open(secret_file) as f:
    secrets = json.loads(f.read())

def get_secret(setting, secrets=secrets):
    """비밀 변수를 가져오거나 명시적 예외를 반환한다."""
    try:
        return secrets["slackToken"]
    except KeyError:
        error_msg = "Set the {} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)

def slack_notify(text=None, channel='#backend', username='알림봇', attachments=None):
    TOKEN = get_secret("slackToken")
    slack = Slacker(TOKEN)
    attachments = [{
    "pretext": "경고 알림",
    # "color": "#36a64f",
    "color": "#ed2939",
    "title": "누군가가 노트북에 손을 댔습니다.",
    "title_link": "http://ghcksdk.dothome.co.kr/",
    "fallback": "클라이언트에서 노티피케이션에 보이는 텍스트 입니다. attachment 블록에는 나타나지 않습니다",
    "text": "자세히 보기 대충 이런 내용입니다.",
    "mrkdwn_in": ["text", "pretext"],
    }]
    # "text": "{}".format(book.title)

    slack.chat.post_message(text=text, channel=channel, username=username, attachments=attachments)

slack_notify()