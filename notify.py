from flask import Flask, request
import requests

app = Flask(__name__)

'''
使用者訂閱網址：
https://notify-bot.line.me/oauth/authorize?response_type=code&client_id='my u
client_id'&redirect_uri='my uri'&scope=notify&state=NO_STATE
'''

def getNotifyToken(AuthorizeCode):
    body = {
        "grant_type": "authorization_code",
        "code": AuthorizeCode,
        "redirect_uri": 'my uri',
        "client_id": 'my client_id',
        "client_secret": 'my client_secret'
    }
    r = requests.post("https://notify-bot.line.me/oauth/token", data=body)
    return r.json()["access_token"]

def lineNotifyMessage(token, msg):
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    payload = {'message': msg}
    r = requests.post("https://notify-api.line.me/api/notify", headers=headers, data=payload)
    return r.status_code

@app.route('/', methods=['POST', 'GET'])
def hello_world():
    authorizeCode = request.args.get('code')
    token = getNotifyToken(authorizeCode)
    lineNotifyMessage(token, "恭喜你連動完成")
    return f"恭喜你，連動完成"


if __name__ == '__main__':
   app.run()