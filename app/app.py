import streamlit as st
import datetime
import smtplib
from email.mime.text import MIMEText
import csv
import os

st.title("📩 申訴信箱系統")

# ===== 表單 =====
name = st.text_input("姓名（可匿名）")
email = st.text_input("回覆信箱（可選）")
title = st.text_input("申訴標題")
content = st.text_area("申訴內容")

# ===== 管理者信箱設定 =====
sender = "yuupuntil@gmail.com"
password = "sbcn ticc ksnw cmye"
receiver = "yuupuntil@gmail.com"

# ===== 按鈕 =====
if st.button("送出申訴"):

    if content.strip() == "":
        st.error("申訴內容不能為空")
    else:

        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # ===== 組合信件 =====
        message = f"""
申訴系統通知

時間：{now}
姓名：{name}
回覆信箱：{email}

標題：{title}

內容：
{content}
"""

        msg = MIMEText(message, "plain", "utf-8")
        msg["Subject"] = f"申訴：{title}"
        msg["From"] = sender
        msg["To"] = receiver

        # ===== 存 CSV（備份）=====
        file_exists = os.path.isfile("complaints.csv")
        with open("complaints.csv", "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["time", "name", "email", "title", "content"])
            writer.writerow([now, name, email, title, content])

        # ===== 寄信 =====
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(sender, password)
            server.send_message(msg)
            server.quit()

            st.success("✅ 申訴已送出（Email + 紀錄完成）")

        except Exception as e:
            st.warning("⚠️ Email 寄送失敗，但資料已保存")
            st.error(e)
