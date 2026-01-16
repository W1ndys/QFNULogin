import os
import sys
from loguru import logger


def get_user_config():
    """
    获取用户配置
    仅从环境变量获取
    返回:
        user_account: 用户账号
        user_password: 用户密码
    """
    # 尝试从环境变量获取
    user_account = os.getenv("USER_ACCOUNT")
    user_password = os.getenv("USER_PASSWORD")

    if not user_account or not user_password:
        logger.error("未找到环境变量 USER_ACCOUNT 或 USER_PASSWORD，请设置后重试")
        sys.exit(1)

    logger.info("成功从环境变量中获取用户配置")
    return user_account, user_password
