def remove_duplicates(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    unique_credentials = set()
    cleaned_lines = []

    for i in range(0, len(lines), 3):  # 每个账号密码对占3行（账号、密码、分隔符）
        account = lines[i].replace("账号：", "").strip()  # 移除“账号”字样
        password = lines[i + 1].replace("密码：", "").strip()  # 移除“密码”字样
        separator = lines[i + 2].strip()

        credential = (account, password)
        if credential not in unique_credentials:
            unique_credentials.add(credential)
            cleaned_lines.extend([account + "\n", password + "\n", separator + "\n"])
    file_path = "user_credentials_cleaned.txt"
    with open(file_path, "w", encoding="utf-8") as file:
        file.writelines(cleaned_lines)
    print(f"Duplicate entries removed. Cleaned data saved to {file_path}")


# 使用示例
remove_duplicates("user_credentials.txt")
