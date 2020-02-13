"""
运行一个flask服务器，当收到某个IP发来的合法请求时，就会允许该IP访问本机的某个端口。
客户端的请求示例：curl <ip:port> -X POST -d "password=123456&port=5000"
"""

import os
from flask import Flask, request


app = Flask(__name__)


@app.route("/", methods=["POST"])
def register_port():
    password = request.form.get('password')
    port = request.form.get('port')
    if not port or not password:
        return 'Bad Request', 400
    try:
        port = int(port)
        assert (1000 < port < 10000)
    except:
        return 'Bad Request', 400
    if password != '123456':
        return 'Forbidden', 403

    command='iptables -I INPUT -p tcp -s {} --dport {} -j ACCEPT'.format(request.remote_addr, port)
    with os.popen(command) as p:
        print(p.read())
    return 'Port {} has been opened for you.'.format(port)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=False)
