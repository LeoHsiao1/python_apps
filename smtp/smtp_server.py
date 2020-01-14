# -*- coding: utf-8 -*-
"""
运行一个简单的smtp服务器，能接收邮件。
"""

import asyncore
import smtpd

from pop import parse_email


class CustomSMTPServer(smtpd.SMTPServer):
    def process_message(self, peer, mailfrom, rcpttos, data, **kwargs):  # 重载处理邮件的方法
        print("\n\n# Received email")
        print("From: ", mailfrom, peer)
        print("To: ", rcpttos)
        print("parsed:", parse_email(data))


server = CustomSMTPServer(("127.0.0.1", 9000), None)  # 创建SMTP服务器
asyncore.loop()  # 异步循环运行
