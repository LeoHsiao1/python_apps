import poplib
from email import parser, header, message


def parse_email(raw: [str, bytes]) -> dict:
    """
    Parses the raw data of the email. Some fields may not be parsed.
    """
    if not isinstance(raw, str):
        raw = raw.decode()

    # parse most fields
    msg = parser.Parser().parsestr(raw)  # it is <email.message.Message object>
    result = {k: v for k, v in msg.items()}

    # parse several fields
    for k in ["From", "To", "Subject"]:
        result[k] = []
        # this field has a list of values, like: [(b'hello', 'utf-8')]
        values = header.decode_header(msg[k])
        for v in values:
            if isinstance(v[0], str):
                _v = v[0]
            else:
                _v = v[0].decode(v[1] or 'utf-8')
            result[k].append(_v)

    # parse the payload
    result["Payload"] = parse_payload(msg)
    return result


def parse_payload(msg):
    payload = msg.get_payload()
    if not isinstance(payload, list):
        return {'Payload': payload}
    # The payload may be multiple parts, multiple types, and nested.
    result = []
    for p in payload:
        p_dict = {k: v for k, v in p.items()}
        p_dict['raw'] = p
        if p.is_multipart():
            p_dict['Payload'] = parse_payload(p)
        elif p.get_content_type() in ["text/plain", "text/html"]:
            p_dict['Payload'] = p.get_payload(decode=True).decode(p.get_content_charset())
        result.append(p_dict)
    return result


def download_email(server):
    """ download all the email from POP server """
    res, _list, octets = server.list()
    if not res.decode().startswith("+OK"):
        raise ConnectionError("Failed to get email list: " + res.deocde())
    emails = []
    for i in range(len(_list), 0, -1):
        print("Downloading email No.{}, {} bytes".format(*_list[i-1].decode().split()))
        res, lines, octets = server.retr(i)
        if not res.decode().startswith("+OK"):
            raise ConnectionError("Failed to download email No.{}: {}".format(i, res.deocde()))
        email = parse_email(b"\n".join(lines))
        emails.append(email)
    return emails[::-1]


if __name__ == "__main__":
    server = poplib.POP3_SSL(host="pop.163.com", port=995, timeout=3)
    server.user("will1334@163.com")
    server.pass_("******")
    emails = download_email(server)

    for k, v in emails[0].items():
        print(k, v)
