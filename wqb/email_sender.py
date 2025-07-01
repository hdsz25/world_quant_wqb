import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
import traceback
from os.path import expanduser
import json

home = expanduser("~")
with open(home + "/.worldquant/config.json", "r") as f:
    creds = json.load(f)
    # 配置发送方信息（需替换为你的QQ邮箱和授权码）
    SENDER_EMAIL = creds["email"]
    SENDER_NAME = "WQB Auto Alert System"
    SENDER_PASSWORD = creds["email_password"]


def send_email(subject: str, content: str = " ", receiver_email=SENDER_EMAIL):
    msg = MIMEText(content, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = formataddr((SENDER_NAME, SENDER_EMAIL))
    msg["To"] = receiver_email

    server = None
    try:
        # 不使用上下文管理器，改为手动控制
        server = smtplib.SMTP_SSL("smtp.qq.com", 465)
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, [receiver_email], msg.as_string())
        print("邮件发送成功")
    except Exception as e:
        print(f"邮件发送失败: {str(e)}")
        raise
    finally:
        if server:
            try:
                # 显式关闭连接但不检查响应
                server.close()
            except:
                pass  # 忽略关闭时的任何异常
