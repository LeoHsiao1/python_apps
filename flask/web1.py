# -*- coding: utf-8 -*-
"""
基于Flask运行一个简单的Web服务器。
"""

import os
from flask import Flask, request, render_template, jsonify, redirect, session

app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route("/", methods=["GET"])
def index():
    if session.get("logined", False):
        return render_template("common.html",
                               title="主页",
                               msg="已登录。",
                               url="/logout",
                               url_name="登出")
    else:
        return render_template("common.html",
                               title="主页",
                               msg="还没有登录。",
                               url="/login",
                               url_name="登录")


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("logined", False):
        return redirect("/")

    if request.method == "GET":
        return render_template("login.html", msg="请输入用户名和密码", captcha=b'')

    elif request.method == "POST":
        form = {"username": request.form["username"],
                "password": request.form["password"]}
        # check(username)
        session["logined"] = True
        return redirect("/")


@app.route("/logout", methods=["GET"])
def logout():
    session["logined"] = False
    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
