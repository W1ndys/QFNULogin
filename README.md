# QFNULogin

曲阜师范大学教务系统（强智教务）模拟登陆脚本，便于各位写脚本读取教务系统数据

以读取考试安排为例，可以读取考试安排，并生成 ics 文件，导入到日历中

![Screenshot_2024-12-29-02-14-44-097_com microsoft emmx](https://github.com/user-attachments/assets/47132930-18c4-4580-8e6b-ef2835fb7ada)


## 使用

克隆项目

```bash
git clone https://github.com/W1ndys/QFNULogin.git
```

### 控制台运行

1. 安装依赖

```bash
pip install -r requirements.txt
```

2. 运行脚本

```bash
python main.py
```

### 网页版

1. 安装依赖

```bash
pip install -r requirements.txt
```

2. 运行脚本

```bash
cd app
python qfnuloginwebserver.py
```

3. 访问网页

```bash
http://127.0.0.1:5000
```

## 致谢

感谢 [ddddocr](https://github.com/sml2h3/ddddocr) 提供的验证码识别功能

感谢 [liu-zhe](https://github.com/liu-zhe)(Lukzia) 的[qfnu_api.py](https://github.com/liu-zhe/QFNU-ics/blob/main/qfnu_api.py) 模拟登录启发

感谢 [nakaii](https://github.com/nakaii-002)(nakaii) 的[Qfnu_CAS_token](https://github.com/nakaii-002/Qfnu_CAS_token) 验证码识别启发
