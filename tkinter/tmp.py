import tkinter


# 显示主窗口
w1 = tkinter.Tk()
w1.title("")        # 设置窗口的标题
w1.minsize(500, 300)  # 设置窗口的最小尺寸


# 显示一个文本框
T1 = tkinter.Text(w1)
T1.pack(side="top")
T1.insert("1.0", "Hello\n")  # 在指定位置插入一个字符串


# 显示一个输入框，以及配套的按钮
E1_var = tkinter.Variable()	 # 创建一个可及时刷新的变量，用于保存输入框的文本内容
E1 = tkinter.Entry(w1, textvariable=E1_var)
E1.pack(side="left")


def get_entry():
    value = E1_var.get()  # 获取输入框的文本内容
    T1.insert("end", value+'\n')


B1 = tkinter.Button(w1, text="Entry", command=get_entry)
B1.pack(side="left")


# 显示一个标签
# img = tkinter.PhotoImage(file=r"C:\Users\Leo\Desktop\1.png")
# tkinter.Label(w1, image= img).place(relwidth=1, relheight=0.8, relx=0, rely=0)

w1.mainloop()   # 进入主循环
