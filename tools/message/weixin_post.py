# 从测试号信息获取
import json

import requests

appID = "wx435f2f44aba9b9cd"
appSecret = "3affde0265539f122cc4854ca21f9e5e"
# 收信人ID即 用户列表中的微信号，见上文
openId = "onryO6FGwAEeIapfDmb-I-iOeNKU"
timetable_template_id = "aHzvWITHrbdjvGi0IAz0tj3AucXVaWHULzl8S7xl-oA"


def wx_warning(message):
    pass


def get_access_token():
    # 获取access token的url
    url = f'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={appID.strip()}&secret={appSecret.strip()}'
    response = requests.get(url).json()
    print(response)
    access_token = response.get('access_token')
    return access_token


def timetable(message):
    # 1.获取access_token
    access_token = get_access_token()
    # 3. 发送消息
    send_timetable(access_token, message)


def send_timetable(access_token, message):
    body = {
        "touser": openId,
        "template_id": timetable_template_id.strip(),
        "url": "https://xsfw.gzist.edu.cn/xsfw/sys/swmzncqapp/*default/index.do",
        "data": {
            "message": {
                "value": message
            },
            "retries": {
                "value": 123
            },
        }
    }
    url = f'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={access_token}'
    print(requests.post(url, json.dumps(body)).text)


if __name__ == '__main__':
    timetable("test")
