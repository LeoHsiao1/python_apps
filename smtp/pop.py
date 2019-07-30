# -*- coding: utf-8 -*-
"""
运行一个pop客户端，能从pop服务器拉取邮件，并解析邮件。
"""

import base64
import poplib
from email import header, message, parser


def parse(raw_data: bytes):
    """ parses the raw data of email, returns a dict as result.
     - result["Payload"] is a list, it may contains multiple parts. 
     Some parts may not be parsed.
    """
    _email = parser.Parser().parsestr(raw_data.decode())
    result = {}
    for k, v in _email.items():
        result[k] = v

    for k in ["From", "To", "Subject"]:
        result[k] = []
        for p in header.decode_header(_email[k]):
            if isinstance(p[0], str):
                value = p[0]
            else:
                value = p[0].decode(p[1])
            result[k].append(value)

    # parse payload
    result["Payload"] = []
    payload = _email.get_payload()
    if not isinstance(payload, list):
        payload = [_email]
    for p in payload:
        if isinstance(p, message.Message):
            if p.get_content_type() in ["text/plain", "text/html"]:
                content = p.get_payload(decode=True).decode(p.get_content_charset())
                result["Payload"].append(content)
            else:
                result["Payload"].append(p)
        else:
            result["Payload"].append(p)
    return result


def download_email(server):
    """ download all the email from POP server """
    res, _list, octets = server.list()
    if not res.decode().startswith("+OK"):
        raise ConnectionError("Failed to get email list: " + res.deocde())
    emails = {}
    for i in range(len(_list), 0, -1):
        print("Downloading email No.{}, {} bytes".format(
            *_list[i - 1].decode().split()))
        res, raw_data, octets = server.retr(i)
        if not res.decode().startswith("+OK"):
            raise ConnectionError(
                "Failed to download email No.{}: {}".format(i, res.deocde()))
        emails[i] = parse(b"\r\n".join(raw_data))
    return emails


if __name__ == "__main__":
    server = poplib.POP3_SSL(host="pop.163.com", port=995, timeout=3)
    server.user("will1334@163.com")
    server.pass_("password")
    emails = download_email(server)

    for k, v in emails[1].items():
        print(k, v)

