import os
import json
from loguru import logger


def get_user_config():
    """
    获取用户配置
    优先从环境变量获取，如果不存在则从 config.json 读取
    返回:
        user_account: 用户账号
        user_password: 用户密码
    """
    # 1. 尝试从环境变量获取
    user_account = os.getenv("USER_ACCOUNT")
    user_password = os.getenv("USER_PASSWORD")

    if user_account and user_password:
        logger.info("从环境变量中获取到用户配置")
        return user_account, user_password

    # 2. 尝试从 config.json 获取
    logger.info("环境变量未配置，尝试读取 config.json")

    # 检查配置文件是否存在
    if not os.path.exists("config.json"):
        # 创建默认配置文件
        default_config = {
            "user_account": "",
            "user_password": "",
        }
        with open("config.json", "w", encoding="utf-8") as f:
            json.dump(default_config, f, ensure_ascii=False, indent=4)
        logger.error(
            "配置文件不存在，已创建默认配置文件 config.json\n请填写相关信息后重新运行程序，或设置环境变量 USER_ACCOUNT 和 USER_PASSWORD"
        )
        exit(0)

    # 读取配置文件
    with open("config.json", "r", encoding="utf-8") as f:
        config = json.load(f)

    # 验证必填字段
    required_fields = ["user_account", "user_password"]
    for field in required_fields:
        if not config.get(field):
            raise ValueError(f"配置文件中缺少必填字段: {field}")

    return (
        config["user_account"],
        config["user_password"],
    )
