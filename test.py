# 读取.env文件
from dotenv import load_dotenv
import os

load_dotenv()

print(os.getenv("USER_ACCOUNT"))
print(os.getenv("USER_PASSWORD"))
