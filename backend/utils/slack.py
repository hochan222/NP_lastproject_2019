from slacker import Slacker
import os, json


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOKEN = []

secret_file = os.path.join(BASE_DIR, 'secret', 'slack_token.json')

with open(secret_file) as f:
    secrets = json.loads(f.read())

def get_secret(setting, secrets=secrets):
    """비밀 변수를 가져오거나 명시적 예외를 반환한다."""
    return secrets["slackToken"]

def slack_notify(text=None, channel='#backend', username='알림봇', attachments=None):
    # TOKEN = get_secret("slackToken")
    TOKEN = "xoxb-623136227107-661697401447-dU6MKUfX8dKQtmDoQU2wDXxk"
    slack = Slacker(TOKEN)
    attachments = [{
    "pretext": "경고 알림",
    # "color": "#36a64f",
    "color": "#ed2939",
    "title": "누군가가 노트북에 손을 댔습니다.",
    "title_link": "http://127.0.0.1:8000/img/",
    "fallback": "클라이언트에서 노티피케이션에 보이는 텍스트 입니다. attachment 블록에는 나타나지 않습니다",
    # "image_url": "http://127.0.0.1:8000/img/",
    "text": "자세히 보기 대충 이런 내용입니다.",
    "mrkdwn_in": ["text", "pretext"],
    }]
    # "text": "{}".format(book.title)

    slack.chat.post_message(text=text, channel=channel, username=username, attachments=attachments)

slack_notify()