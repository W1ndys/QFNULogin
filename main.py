import requests
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup
from ics import Calendar, Event
from datetime import datetime
from captcha_ocr import get_ocr_res
import os
from pytz import timezone
from dotenv import load_dotenv

load_dotenv()


# 设置基本的URL和数据
RandCodeUrl = "http://zhjw.qfnu.edu.cn/verifycode.servlet"  # 验证码请求URL
loginUrl = "http://zhjw.qfnu.edu.cn/Logon.do?method=logonLdap"  # 登录请求URL
dataStrUrl = (
    "http://zhjw.qfnu.edu.cn/Logon.do?method=logon&flag=sess"  # 初始数据请求URL
)


def get_initial_session():
    """
    创建会话并获取初始数据
    返回: (session对象, cookies字典, 初始数据字符串)
    """
    session = requests.session()
    response = session.get(dataStrUrl, timeout=1000)
    cookies = session.cookies.get_dict()
    return session, cookies, response.text


def handle_captcha(session, cookies):
    """
    获取并识别验证码
    返回: 识别出的验证码字符串
    """
    response = session.get(RandCodeUrl, cookies=cookies)
    image = Image.open(BytesIO(response.content))
    return get_ocr_res(image)


def generate_encoded_string(data_str, user_account, user_password):
    """
    生成登录所需的encoded字符串
    参数:
        data_str: 初始数据字符串
        user_account: 用户账号
        user_password: 用户密码
    返回: encoded字符串
    """
    res = data_str.split("#")
    code, sxh = res[0], res[1]
    data = f"{user_account}%%%{user_password}"
    encoded = ""
    b = 0

    for a in range(len(code)):
        if a < 20:
            encoded += data[a]
            for _ in range(int(sxh[a])):
                encoded += code[b]
                b += 1
        else:
            encoded += data[a:]
            break
    return encoded


def login(session, cookies, user_account, user_password, random_code, encoded):
    """
    执行登录操作
    返回: 登录响应结果
    """
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
        "Origin": "http://zhjw.qfnu.edu.cn",
        "Referer": "http://zhjw.qfnu.edu.cn/",
        "Upgrade-Insecure-Requests": "1",
    }

    data = {
        "userAccount": user_account,
        "userPassword": user_password,
        "RANDOMCODE": random_code,
        "encoded": encoded,
    }

    return session.post(
        loginUrl, headers=headers, data=data, cookies=cookies, timeout=1000
    )


def get_exam_page(session, cookies):
    """
    获取考试安排页面内容
    返回: 页面响应内容
    """
    target_url = "http://zhjw.qfnu.edu.cn/jsxsd/xsks/xsksap_list?xqlbmc=&sxxnxq=&dqxnxq=&ckbz=&xnxqid=2024-2025-1&xqlb=#/"
    return session.get(target_url, cookies=cookies, timeout=1000)


def parse_exam_data(html_content):
    """
    解析考试数据并创建日历事件
    返回: Calendar对象
    """
    soup = BeautifulSoup(html_content, "html.parser")
    calendar = Calendar()

    for row in soup.select("table#dataList tr")[1:]:
        cells = row.find_all("td")
        if len(cells) < 11:
            continue

        # 提取信息
        exam_number = cells[0].text.strip()
        campus = cells[1].text.strip()
        session = cells[2].text.strip()
        course_code = cells[3].text.strip()
        course_name = cells[4].text.strip()
        teacher = cells[5].text.strip()
        exam_time = cells[6].text.strip()
        location = cells[7].text.strip()
        seat_number = cells[8].text.strip()

        # 解码考试时间
        date_str, time_range = exam_time.split(" ")
        start_time, end_time = time_range.split("~")

        # 解析日期和时间，并设置为东八区时间
        tz = timezone("Asia/Shanghai")
        start_datetime = tz.localize(
            datetime.strptime(f"{date_str} {start_time}", "%Y-%m-%d %H:%M")
        )
        end_datetime = tz.localize(
            datetime.strptime(f"{date_str} {end_time}", "%Y-%m-%d %H:%M")
        )

        # 创建一个事件
        event = Event()
        event.name = f"{course_name} - {teacher}"
        event.begin = start_datetime
        event.end = end_datetime
        event.location = location
        event.description = (
            f"序号: {exam_number}, 校区: {campus}, 场次: {session}, "
            f"课程编号: {course_code}, 座位号: {seat_number}, "
            f"考试时间: {exam_time}, 技术支持: https://www.w1ndys.top , "
            f"开发者qq: https://qm.qq.com/q/IeoRba7FmY"
        )

        # 添加事件到日历
        calendar.events.add(event)

    return calendar


def get_user_credentials():
    """
    获取用户账号和密码
    返回: (user_account, user_password)
    """
    user_account = os.getenv("USER_ACCOUNT")
    user_password = os.getenv("USER_PASSWORD")
    print(f"用户名: {user_account}\n")
    print(f"密码: {user_password}\n")
    return user_account, user_password


def simulate_login(user_account, user_password):
    """
    模拟登录过程
    返回: (session对象, cookies字典)
    抛出:
        Exception: 当验证码错误时
    """
    session, cookies, data_str = get_initial_session()
    random_code = handle_captcha(session, cookies)
    print(f"验证码: {random_code}")
    encoded = generate_encoded_string(data_str, user_account, user_password)
    response = login(
        session, cookies, user_account, user_password, random_code, encoded
    )

    # 检查响应状态码和内容
    if response.status_code == 200:

        if "验证码错误!!" in response.text:
            raise Exception("验证码识别错误，请重试")
        if "密码错误" in response.text:
            raise Exception("用户名或密码错误")
        return session, cookies
    else:
        raise Exception("登录失败")


def save_response_to_file(content, filename, description):
    """
    保存响应内容到文件
    参数:
        content: 要保存的内容
        filename: 文件名
        description: 描述信息
    """
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"{description}已保存到{filename}文件中")


def save_calendar_to_file(calendar, filename):
    """
    保存日历到文件
    参数:
        calendar: Calendar对象
        filename: 文件名
    """
    with open(filename, "w", encoding="utf-8") as f:
        f.write(calendar.serialize())
    print(f"考试安排已保存到{filename}文件中")


def main():
    """
    主函数，协调整个程序的执行流程
    """
    print("\n" * 30)
    print(f"\n{'*' * 10} 曲阜师范大学教务系统模拟登录脚本 {'*' * 10}\n")
    print("By W1ndys")
    print("https://github.com/W1ndys")
    print("\n\n")

    # 获取环境变量
    user_account, user_password = get_user_credentials()
    if not user_account or not user_password:
        print("请在.env文件中设置USER_ACCOUNT和USER_PASSWORD环境变量\n")
        # 重置.env文件
        with open(".env", "w", encoding="utf-8") as f:
            f.write("USER_ACCOUNT=\nUSER_PASSWORD=")
        return

    # 模拟登录并获取会话
    session, cookies = simulate_login(user_account, user_password)

    # 获取考试页面
    exam_response = get_exam_page(session, cookies)

    # 解析数据并生成日历
    calendar = parse_exam_data(exam_response.text)
    save_calendar_to_file(calendar, "2024_2025_1_exam_schedule.ics")


if __name__ == "__main__":
    main()
