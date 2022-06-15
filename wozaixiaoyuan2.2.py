import datetime
import logging
import random
import smtplib
import time
from email.header import Header
from email.mime.text import MIMEText
from email.utils import formataddr

import requests

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class answer:

    def __init__(self):
        data = [
            # 所有的内容填进引号，如果不需要直接留空，不要删除！
            "",  # 你的名字，可随意填写
            "",  # User-Agent
            "",  # JWSESSION
            "pushplus",  # 通知方式，公众号搜pushplus
            "",  # PushPlus 的授权码（通知方式为推送加时填写，否则留空）,记得下面run里面也要填写
        ]
        self.jwsessionName = ["{}".format(data[0])]
        self.push_method = data[3]
        self.pushplus_token = data[4]
        self.my_user = self.my_sender
        self.api = "https://student.wozaixiaoyuan.com/heat/save.json"
        self.headers = {
            "Host": "student.wozaixiaoyuan.com",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept-Encoding": "gzip, compress, br, deflate",
            "Connection": "close",  # 或者"keep-alive"
            "User-Agent": data[1],
            "Referer": "https://servicewechat.com/wxce6d08f781975d91/{}/page-frame.html".format(
                random.randrange(160, 190, 1)),
            "Content-Length": "567",
            "JWSESSION": data[2],
        }

        self.data = {
            "answers": '["0"]',
            "seq": self.get_seq(),
            "temperature": self.get_random_temprature(),
            "longitude": "23.{}".format(self.get_random_location()),  # 默认为广外
            "latitude": "113.{}".format(self.get_random_location()),
            "country": "中国",
            "province": "广东省",
            "city": "广州市",
            "district": "番禺区",
            "township": "小谷围街道",
            "street": "大学城中环东路",
            "myArea": "南校区",
            "areacode": "440113",
            "timestampHeader": "",  # 自行抓包获取下同
            "signatureHeader": "",
        }

    def get_random_temprature(self):
        random.seed(time.ctime())
        return "{:.1f}".format(random.uniform(36.0, 36.9))

    def get_seq(self):
        current_hour = datetime.datetime.now()
        current_hour = current_hour.hour + 8
        if 6 <= current_hour <= 10:
            return "1"
        elif 19 <= current_hour < 23:
            return "3"
        else:
            return 1

    def get_status(self, res_code):
        if res_code == 0:
            print("日检日报打卡成功")
            result = "日检日报打卡成功"
            return "日检日报打卡成功。"
        elif res_code == 1:
            print("当前非日检日报时间")
            result = "当前非日检日报时间"
            return "当前非日检日报时间。"

        elif res_code == -10:
            print("JWSESSION 已失效，请重新抓包")
            result = "JWSESSION 已失效，请重新抓包"
            return "JWSESSION 已失效，请重新抓包。"
        else:
            print("未知错误，错误代码为{}")
            result = f'未知错误，错误代码为{{res_code}}'
            return "未知错误，错误代码为{}。".format(res_code if res_code != "" else "空")

    def run(self):
        res = requests.post(self.api, headers=self.headers, data=self.data, ).json()
        time.sleep(1)
        res_code = res["code"]
        mail_content = self.get_status(res_code)
        token = ''  # pushplus授权码
        title = self.jwsessionName[0]
        content = mail_content
        url = 'http://www.pushplus.plus/send?token=' + token + '&title=' + title + '&content=' + content
        requests.get(url)
        print("推送完成")
        return True

    def get_random_location(self):
        loc = ""
        for i in range(14):
            loc += str(random.randrange(0, 9, 1))
        return loc


if __name__ == "__main__":
    answer().run()


def main_handler(event, context):
    logger.info('got event{}'.format(event))
    return answer().run()
