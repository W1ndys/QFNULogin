import requests
from Crypto.Util.Padding import pad
from Crypto.Cipher import AES
from bs4 import BeautifulSoup as bs
import base64
import random
import html
import lxml
import os


def rand_str(n: int):
    return "".join(
        random.choices("ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678", k=n)
    )


def parse(s: str):
    return s.encode()


ses = requests.Session()

ses.get("http://zhjw.qfnu.edu.cn")

res = ses.get(
    "http://ids.qfnu.edu.cn/authserver/login?type=userNameLogin&service=http%3A%2F%2Fzhjw.qfnu.edu.cn%2Fsso.jsp"
)

r = bs(res.text, "html.parser")

key = r.select_one("#pwdEncryptSalt").attrs["value"].strip()

print("key =", key)

aes = AES.new(key=parse(key), mode=AES.MODE_CBC, iv=parse(rand_str(16)))

# 从环境变量中获取用户名和密码
username = os.getenv("USER_ACCOUNT")
password = os.getenv("USER_PASSWORD")
if password is None:
    raise ValueError("未设置 USER_PASSWORD 环境变量")

password = rand_str(64) + password

cipher = base64.b64encode(aes.encrypt(pad(password.encode(), 16)))

form_data = {
    "username": username,
    "password": cipher,
    "lt": "",
    "execution": r.select_one('input[name="execution"]').attrs["value"],
    "dllt": "generalLogin",
    "cllt": "userNameLogin",
    "captcha": "",
    "_eventId": "submit",
}

ses.headers = {
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Referer": "http://ids.qfnu.edu.cn/authserver/login?type=dynamicLogin&service=http%3A%2F%2Fzhjw.qfnu.edu.cn%2Fsso.jsp",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
}

res = ses.post(
    "http://ids.qfnu.edu.cn/authserver/login?service=http%3A%2F%2Fzhjw.qfnu.edu.cn%2Fsso.jsp",
    data=form_data,
    allow_redirects=True,
)

kb_data = {
    "rq": "2023-09-07",
    "sjmsValue": "94786EE0ABE2D3B2E0531E64A8C09931",
}
form_data.update(kb_data)
response = ses.post(
    "http://202.194.188.38/jsxsd/framework/main_index_loadkb.jsp",
    data=form_data,
    allow_redirects=False,
)

f = open("", "w", encoding="utf-8")
f.write(response.text)
