from PIL import Image
from io import BytesIO
import datetime
from dotenv import load_dotenv
from utils.session_manager import get_session
from utils.captcha_ocr import get_ocr_res
from utils.logger import setup_logger
from config import get_user_config
import time


# 在文件开头调用setup_logger
logger = setup_logger()

load_dotenv()


def handle_captcha():
    """
    获取并识别验证码
    返回: 识别出的验证码字符串
    """
    session = get_session()

    # 验证码请求URL
    RandCodeUrl = "http://zhjw.qfnu.edu.cn/jsxsd/verifycode.servlet"

    response = session.get(RandCodeUrl)

    if response.status_code != 200:
        logger.error(f"请求验证码失败，状态码: {response.status_code}")
        return None

    try:
        image = Image.open(BytesIO(response.content))
    except Exception as e:
        logger.error(f"无法识别图像文件: {e}")
        return None

    return get_ocr_res(image)


def generate_encoded_string(user_account, user_password):
    """
    生成登录所需的encoded字符串
    参数:
        data_str: 初始数据字符串 (实际未使用)
        user_account: 用户账号
        user_password: 用户密码
    返回: encoded字符串 (账号base64 + %%% + 密码base64)
    """
    import base64

    # 对账号和密码分别进行base64编码
    account_b64 = base64.b64encode(user_account.encode()).decode()
    password_b64 = base64.b64encode(user_password.encode()).decode()

    # 拼接编码后的字符串
    encoded = f"{account_b64}%%%{password_b64}"

    return encoded


def login(random_code, encoded):
    """
    执行登录操作
    返回: 登录响应结果
    """

    # 登录请求URL
    loginUrl = "http://zhjw.qfnu.edu.cn/jsxsd/xk/LoginToXkLdap"
    session = get_session()
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
        "Origin": "http://zhjw.qfnu.edu.cn",
        "Referer": "http://zhjw.qfnu.edu.cn/",
    }

    data = {
        "userAccount": "",
        "userPassword": "",
        "RANDOMCODE": random_code,
        "encoded": encoded,
    }

    return session.post(loginUrl, headers=headers, data=data, timeout=1000)


def simulate_login(user_account, user_password):
    """
    模拟登录过程
    返回: 是否登录成功
    """
    session = get_session()
    # 访问教务系统首页，获取必要的cookie
    response = session.get("http://zhjw.qfnu.edu.cn/jsxsd/")
    if response.status_code != 200:
        logger.error("无法访问教务系统首页，请检查网络连接或教务系统的可用性。")
        return False

    # 获取必要的cookie
    cookies = session.cookies
    logger.info(f"获取到的cookie: {cookies}")

    for attempt in range(3):
        random_code = handle_captcha()
        logger.info(f"验证码: {random_code}")
        encoded = generate_encoded_string(user_account, user_password)
        logger.info(f"encoded: {encoded}")
        response = login(random_code, encoded)
        logger.info(f"登录响应: {response.status_code}")

        if response.status_code == 200:
            if "验证码错误" in response.text:
                logger.warning(f"验证码识别错误，重试第 {attempt + 1} 次")
                continue
            if "密码错误" in response.text:
                raise Exception("用户名或密码错误")
            return True
        else:
            raise Exception("登录失败")

    raise Exception("验证码识别错误，请重试")


def print_welcome():
    logger.info(f"\n{'*' * 10} 曲阜师范大学模拟登录脚本 {'*' * 10}\n")
    logger.info("By W1ndys")
    logger.info("https://github.com/W1ndys")
    logger.info("\n\n")
    logger.info(f"当前时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


def main():
    """
    主函数，协调整个程序的执行流程
    """
    # 获取环境变量
    user_account, user_password = get_user_config()

    while True:  # 添加外层循环
        try:
            # 模拟登录
            if not simulate_login(user_account, user_password):
                logger.error("无法建立会话，请检查网络连接或教务系统的可用性。")
                time.sleep(1)  # 添加重试间隔
                continue  # 重试登录

            session = get_session()
            if not session:
                logger.error("无法建立会话，请检查网络连接或教务系统的可用性。")
                time.sleep(1)
                continue

            # 访问主页
            try:
                response = session.get(
                    "http://zhjw.qfnu.edu.cn/jsxsd/framework/xsMain.jsp"
                )
                logger.debug(f"页面响应状态码: {response.status_code}")
                if response.status_code == 200:
                    logger.info("登录成功!")
                    break
            except Exception as e:
                logger.error(f"访问页面失败: {str(e)}")
                raise

        except Exception as e:
            logger.error(f"发生错误: {str(e)}，正在重新登录...")
            time.sleep(1)
            continue  # 重新登录


if __name__ == "__main__":
    main()
