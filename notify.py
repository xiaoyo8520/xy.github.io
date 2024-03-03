import requests
from flask import Flask, request,render_template

app = Flask(__name__)

uri='https://10fb-114-33-4-188.ngrok-free.app' #callback網址

#訪問網址'https://notify-bot.line.me/oauth/authorize?response_type=code&client_id=9BhYhKzGtasty5jOlfsPGK&redirect_uri=&scope=notify&state=NO_STATE'

@app.route('/', methods=['POST', 'GET']) #連接端點，訪問notify網址連動時會轉到這
def hello_world():
    authorizeCode = request.args.get('code')
    token = getNotifyToken(authorizeCode)
    print(token)
    lineNotifyMessage(token, "連動完成!")
    return render_template('h.html')

@app.route('/ac/<name>/<msg>',methods=['POST','GET'])#提醒通知端，name為token，msg是訊息，再丟入發訊息函式
def hello_wor(name,msg):
    token=f'{name}'
    lineNotifyMessage(token, f'{msg}')
    

def getNotifyToken(AuthorizeCode): #運用網址'code'參數和相關資訊，生成oauth_token
    body = {
        "grant_type": "authorization_code",
        "code": AuthorizeCode,
        "redirect_uri": uri,
        "client_id": '9BhYhKzGtasty5jOlfsPGK',
        "client_secret": 'j0KmCm6UHc14lyD0qQeQqf3NTER2K2p8vFpIsjlJRD5'
    }
    r=requests.post("https://notify-bot.line.me/oauth/token", data=body)
    return r.json()["access_token"]

def lineNotifyMessage(token, msg): #根據token，向notify發出post，發送msg
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    payload = {'message': msg}
    r = requests.post("https://notify-api.line.me/api/notify", headers=headers, data=payload)
    return r.status_code

if __name__ == '__main__':
    app.run()
