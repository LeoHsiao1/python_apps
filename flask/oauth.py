import os
from urllib.parse import urlencode

import requests
from flask import Flask, jsonify, redirect, render_template, request, session
from oauthlib import oauth2

app = Flask(__name__)
app.secret_key = os.urandom(24)

OAUTH = {
    "client_id": "6c6d1d870a45ec568f4eesaba548862dd907045a00471001b88201xdf6fc9364",
    "client_secret": "ab94b30cb1sd65885c9f05evf8b1a47c8de0ef96b2e1b2b5028a192e05g65e38",
    "redirect_uri": "http://192.168.0.1/login/oauth/callback/",
    "scope": "api",
    "auth_url": "http://gitlab.test/oauth/authorize",
    "token_url": "http://gitlab.test/oauth/token",
    "api_url": "http://gitlab.test/api/v4",
}
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true"  # 允许使用HTTP进行OAuth，而不是HTTPS


@app.route("/login/oauth/", methods=["GET"])
def oauth():
    """ 当用户点击该链接时，把用户重定向到Gitlab的OAuth2登录页面。 """
    client = oauth2.WebApplicationClient(OAUTH["client_id"])
    state = client.state_generator()    # 生成的随机的state参数
    auth_url = client.prepare_request_uri(OAUTH["auth_url"],
                                          OAUTH["redirect_uri"],
                                          OAUTH["scope"],
                                          state)  # 构造完整的auth_url，接下来要让用户重定向到它
    session["oauth_state"] = state
    return redirect(auth_url)


@app.route("/login/oauth/callback/", methods=["GET"])
def oauth_callback():
    """ 用户在同意授权之后，会被Gitlab重定向回到这个URL。 """
    # 解析得到code
    client = oauth2.WebApplicationClient(OAUTH["client_id"])
    code = client.parse_request_uri_response(request.url, session["oauth_state"]).get("code")

    # 请求token
    body = client.prepare_request_body(code,
                                       redirect_uri=OAUTH["redirect_uri"],
                                       client_secret=OAUTH["client_secret"])
    r = requests.post(OAUTH["token_url"], body)
    access_token = r.json().get("access_token")

    # 查询用户名并储存
    api_path = "/user"
    url = OAUTH["api_url"] + "/" + api_path + "?" + \
        urlencode({"access_token": access_token})
    r = requests.get(url)
    data = r.json()
    session["username"] = data.get("username")
    session["access_token"] = access_token  # 以后存到用户表中

    return redirect("/")


@app.route("/logout/", methods=["GET"])
def logout():
    session.pop("username", None)
    return redirect("/")


@app.route("/", methods=["GET"])
def home():
    username = session.get("username")
    if username:
        context = {"title": "主页", "msg": "你已登录：{}".format(username),
                   "url": "/logout/", "url_name": "登出"}
        return render_template("common.html", **context)
    else:
        context = {"title": "主页", "msg": "你还没有登录。",
                   "url": "/login/oauth/", "url_name": "通过Gitlab登录"}
        return render_template("common.html", **context)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
