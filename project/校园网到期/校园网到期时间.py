import os
from datetime import datetime
from tools import send_msg
from feapder.utils.tools import log
from feapder import Request
from setting import LOGIN_USERNAME, LOGIN_PASSWORD, XYW_URL

stop_send_flag = False


def a():
    try:
        response1 = Request(
            # url="http://self.gzist.edu.cn:8080/Self/login/?302=LI"
            url=f"{XYW_URL}/Self/login/?302=LI"
        ).get_response()
        cookie = response1.cookies
        checkcode = response1.xpath('//*[@id="loginSet"]/div/div/form/div[1]/input[3]/@value').get()
    except:
        return None
    else:
        return cookie, checkcode


def b(cookie):
    try:
        response2 = Request(
            # url="http://self.gzist.edu.cn:8080/Self/login/randomCode",
            url=f"{XYW_URL}/Self/login/randomCode",
            cookies=cookie,
        ).get_response()
    except:
        return None
    else:
        return response2


def c(data, cookie):
    try:
        response3 = Request(
            # url="http://self.gzist.edu.cn:8080/Self/login/verify",
            url=f"{XYW_URL}/Self/login/verify",
            data=data,
            cookies=cookie,
        ).get_response()
        danger_state = response3.xpath(
            "(//span[@class='label label-danger'])[1]/text()").get()
        if danger_state:
            return danger_state
        expire_date = response3.xpath(
            "(//span[@class='label label-default'])[2]/text()").get()
    except:
        return None
    else:
        return expire_date


def main(data):
    msg = None
    cookie, checkcode = a()
    if not all([cookie, checkcode]):
        msg = "获取cookie失败"
        return msg
    if not b(cookie):
        msg = "获取验证码失败"
        return msg
    data["checkcode"] = checkcode
    expire_date = c(data, cookie)
    if not expire_date:
        msg = "获取到期时间失败"
        return msg
    try:
        date1 = datetime.strptime(expire_date, "%Y-%m-%d")
    except:
        msg = f"状态：{expire_date}"
        stop_or_start(1)
        return msg
    recover_flag = stop_or_start(0)
    log.info(f"到期时间：{expire_date}")
    date2 = datetime.now()
    difference = date1 - date2
    days_difference = difference.days
    log.info(f"剩余天数：{days_difference}")
    msg = f"到期时间：{expire_date}，\n剩余天数：{days_difference}"
    if recover_flag:
        msg = f"已复通\n{msg}"
        return msg
    if days_difference > 3:
        msg = None
    # msg = f"到期时间：{expire_date}，\n剩余天数：{days_difference}"
    return msg


def stop_or_start(flag=-1):
    global stop_send_flag
    filepath = "已停机"
    filepath_flag = os.path.exists(filepath)
    stop_send_flag = filepath_flag
    log.info(f"发送信息：{not filepath_flag}")
    if flag == 1:
        with open(filepath, 'w'):
            log.warning("已停机")
    if flag == 0 and filepath_flag:
        os.remove(filepath)
        log.info("已复通")
        stop_send_flag = False
    return filepath_flag


if __name__ == '__main__':
    data = {
        "checkcode": 'checkcode',
        "account": LOGIN_USERNAME,
        "password": LOGIN_PASSWORD,
    }
    msg = main(data)
    if msg:
        log.warning(msg)
        if not stop_send_flag:
            send_msg(msg, keyword="<校园网到期通知>\n")
    else:
        log.info("到期时间正常")
