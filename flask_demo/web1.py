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


@app.route("/api1", methods=["GET"])
def api1():
    request.args.get("id", None)   # 获取HTTP请求的Query String
    request.url                    # 获取HTTP请求的URL
    request.method                 # 获取HTTP请求的方法名
    request.headers                # 获取HTTP请求的headers（返回一个字典）
    return jsonify({"ret":0})


@app.route("/api2", methods=["POST"])
def api2():
    request.form.get("username", None)	# 获取x-www-form-urlencoded格式的表单数据
    request.json                   # 获取application/json格式的表单数据（dict类型）
    request.data                   # 获取application/json格式或text/xml格式的表单数据（bytes类型）
    return jsonify({"ret":0})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
