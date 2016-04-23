#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import ttk
from tkinter.messagebox import *
import sqlite3

def expense(child, exp, current_sum):
    print('消费%s' %exp.get())
    conn = sqlite3.connect('SmartCard.db')
    print('打开数据库..')
    if ((float(current_sum.get()) - float(exp.get())) < 0):
        showinfo(title='消息',message='\n余额不足')
    else:
        current_sum = str(float(current_sum.get()) - float(exp.get()))
        conn.execute("UPDATE STUDENT set SUM=%f where CARDID=%d" %(float(current_sum), int(num.get())))
        cursor = conn.execute("SELECT CARDID,NAME,SEX,ACADEMY,STUID,SUM from STUDENT where CARDID=%d" %int(num.get()))
        for row in cursor:
            print("CARDID = ", row[0])
            print("NAME = ", row[1])
            print("SEX = ", row[2])
            print("ACADEMY = ", row[3])
            print("STUID = ", row[4])
            print("SUM = ", row[5], "\n")
        conn.commit()
        conn.close()
        print('关闭数据库.')
        showinfo(title='消息',message='\n扣费成功')
    child.destroy()
    Window2()

def Recharge(child, rec, current_sum):
    print('充值:%s' %rec.get())
    conn = sqlite3.connect('SmartCard.db')
    print('打开数据库..')
    current_sum = str(float(current_sum.get()) + float(rec.get()))
    conn.execute("UPDATE STUDENT set SUM=%f where CARDID=%d" %(float(current_sum), int(num.get())))
    cursor = conn.execute("SELECT CARDID,NAME,SEX,ACADEMY,STUID,SUM from STUDENT where CARDID=%d" %int(num.get()))
    for row in cursor:
        print("CARDID = ", row[0])
        print("NAME = ", row[1])
        print("SEX = ", row[2])
        print("ACADEMY = ", row[3])
        print("STUID = ", row[4])
        print("SUM = ", row[5], "\n")
    conn.commit()
    conn.close()
    print('关闭数据库.')
    showinfo(title='消息',message='\n充值成功')
    child.destroy()
    Window2()

def Window2(*args):
    print(num.get())
    conn = sqlite3.connect('SmartCard.db')
    print('打开数据库..')
    cursor = conn.execute("SELECT CARDID from STUDENT")
    whether = False
    for row in cursor:
        if (row[0] == int(num.get())):
            whether = True
            print('有此卡号,可以登陆')
            break
        else:
            whether = False
            print('无此卡号,不能登陆')
    if (whether == False):
        showinfo(title='消息',message='\n登陆失败\n无此卡号')
        num.set('')
        conn.close()
        print('关闭数据库.')
    else:
        print('登陆成功..')
        print(int(num.get()))
        cursor = conn.execute("SELECT SUM FROM STUDENT WHERE CARDID = %d " %int(num.get()))
        for row in cursor:
            print(row[0])
        conn.close()
        print('关闭数据库.')
        win2 = Toplevel()
        win2.title('账户: %s'  %num.get())
        win2.geometry('415x355+425+100')
        current_sum = StringVar()
        current_sum.set(str(row[0]))
        #显示图片
        Label(win2, image=img).grid(column=0, columnspan=5, row=0, rowspan=4)
        #账户余额
        Label(win2, text='账户余额', font=("宋体", 18, "normal")).grid(column=1, row=4, sticky=(W, E))
        Label(win2, text=current_sum.get(), font=("宋体", 15, "normal")).grid(column=1, row=5, sticky=(W, E))
        #消费
        exp = StringVar()
        exp_entry = ttk.Entry(win2,width=10, textvariable=exp)
        exp_entry.grid(column=3, row=4, sticky=W)
        ttk.Button(win2, text='消费', width=5, command=lambda m = win2:expense(m, exp, current_sum)).grid(column=3, row=4, sticky=E)
        #充值
        rec = StringVar()
        rec_entry = ttk.Entry(win2,width=10, textvariable=rec)
        rec_entry.grid(column=3, row=5, sticky=W)
        ttk.Button(win2, text='充值', width=5, command=lambda m = win2:Recharge(m, rec, current_sum)).grid(column=3,row=5, sticky=E)
        #查询交易记录
        ttk.Button(win2, text='查询交易记录').grid(column=3, row=6, sticky=(E,W))
        for child in win2.winfo_children():child.grid_configure(padx=5, pady=8)

#--------------------------------我是一条可爱的分界线--------------------------------
#                                    这是注册窗口

def insert(cardID, name, sex, academy, stuID):
    #写入数据库
    print('录入中...')
    conn = sqlite3.connect('SmartCard.db')
    stu = [(int(cardID.get()), str(name.get()), str(sex.get()), str(academy.get()), str(stuID.get()), 100.00)]
    conn.executemany("INSERT INTO STUDENT (CARDID,NAME,SEX,ACADEMY,STUID,SUM) VALUES (?, ?, ?, ?, ?, ?)", stu)
    print('录入成功')
    #记得提交和关闭
    conn.commit()
    cursor = conn.execute("SELECT cardid, name, sex, academy, stuid, sum  from STUDENT")
    for row in cursor:
        print("CARDID = ", row[0])
        print("NAME = ", row[1])
        print("SEX = ", row[2])
        print("ACADEMY = ", row[3])
        print("STUID = ", row[4])
        print("SUM = ", row[5], "\n")
    conn.close()
    print('数据库关闭.')

def register(child,name, sex, academy, stuID):
    if (name.get()=='' or sex.get()=='' or academy.get()==''or stuID.get()==''):
        #信息要全部填好,不然就重新填
        showinfo(title='消息',message='\n注册失败\n请填入完整信息')
    else:
        #打开数据库(已存在STUDENT表)
        conn = sqlite3.connect('SmartCard.db')
        print ("打开数据库.")
        #获得表中行数
        count = conn.execute("SELECT count(*) from STUDENT")
        len = count.fetchone()[0]
        print('STUDENT表中行数: %d' %len)

        cardID = IntVar()
        if (len == 0):
            #表中无数据,直接给定一个最前的卡号
            cardID.set(100000)
            print(cardID.get())
            print(name.get())
            print(sex.get())
            print(academy.get())
            print(stuID.get())
            #写入数据库
            insert(cardID, name, sex, academy, stuID)
            showinfo(title='消息',message='\n注册成功\n你的卡号是%s' %cardID.get())
            #清空输入框
            name.set('')
            sex.set('')
            academy.set('')
            stuID.set('')
            child.destroy()
        else:
            #表中有数据
            #打印整个表
            cursor = conn.execute("SELECT cardid, name, sex, academy, stuid, sum  from STUDENT")
            for row in cursor:
                print("CARDID = ", row[0])
                print("NAME = ", row[1])
                print("SEX = ", row[2])
                print("ACADEMY = ", row[3])
                print("STUID = ", row[4])
                print("SUM = ", row[5], "\n")
            cursor = conn.execute("SELECT STUID from STUDENT")
            whether = True
            for row in cursor:
                if (row[0] == stuID.get()):
                    whether = False
                    print('相同学号')
                    break
                else:
                    whether = True
                    print('不同学号')
            if (whether == True):
                print('可以注册')
                #产生一个卡号(最新卡号增加1)
                cursor = conn.execute("SELECT CARDID from STUDENT")
                i = []
                for row in cursor:
                    i.append(row[0])
                cardID.set(i[len-1]+1)
                print(cardID.get())
                print(name.get())
                print(sex.get())
                print(academy.get())
                print(stuID.get())
                #写入数据库
                insert(cardID, name, sex, academy, stuID)
                showinfo(title='消息',message='\n注册成功\n你的卡号是%s' %cardID.get())
                #清空输入框
                name.set('')
                sex.set('')
                academy.set('')
                stuID.set('')
                child.destroy()
            else:
                print('此学号已注册过,不可以注册')
                showinfo(title='消息',message='\n注册失败\n已存在此卡')
                name.set('')
                sex.set('')
                academy.set('')
                stuID.set('')
                conn.close()
                print('关闭数据库.')
def sex_selected(var, sex):
    #把性别Radiobutton获得的值传给sex
     if var.get()==1:
        print('男')
        sex.set('男')
     else:
        print('女')
        sex.set('女')
def academy_selected(aca, mb, academy):
    print("~被调用了~")
    print(aca.get())
    if (aca.get() == 0):
        mb['text'] = '工学院'
        academy.set('工学院')
    elif (aca.get() == 1):
        mb['text'] = '理学院'
        academy.set('理学院')
    elif (aca.get() == 2):
        mb['text'] = '文学院'
        academy.set('文学院')
    elif (aca.get() == 3):
        mb['text'] = '法学院'
        academy.set('法学院')
    elif (aca.get() == 4):
        mb['text'] = '商学院'
        academy.set('商学院')
    elif (aca.get() == 5):
        mb['text'] = '新闻学院'
        academy.set('新闻学院')
    elif (aca.get() == 6):
        mb['text'] = '艺术学院'
        academy.set('艺术学院')

def Window3(*args):
    #创建toplevel顶层部件窗口
    win3 = Toplevel()
    win3.title('注册窗口')
    win3.geometry('220x355+425+100')
    print('打开注册窗口')
    #创建控件
    sex = StringVar()
    academy = StringVar()
    stuID = StringVar()
    #占行
    Label(win3, text=" ").grid(column=1, row=1)
    Label(win3, text=" ").grid(column=1, row=6)
    #姓名
    name = StringVar()
    Label(win3, text='姓名:', font=("宋体", 15, "normal")).grid(column=2, row=2, sticky=W)
    name_entry = ttk.Entry(win3, width=12, textvariable=name).grid(column=3, row=2, sticky=W)
    #学号
    Label(win3, text='学号:', font=("宋体", 15, "normal")).grid(column=2, row=3, sticky=E)
    StuID_entry = ttk.Entry(win3, width=12, textvariable=stuID).grid(column=3, row=3, sticky=W)
    #学院
    Label(win3, text='学院:', font=("宋体", 15, "normal")).grid(column=2, row=4, sticky=E)
    mb = ttk.Menubutton(win3, text="请选择")
    mb.grid(column=3, row=4, sticky=W)
    aca = IntVar()
    aca.set('10')
    filemenu = Menu(mb, tearoff=False)
    filemenu.add_radiobutton(label="工学院", variable=aca, value=0, command=lambda m = win3:academy_selected(aca, mb, academy))
    filemenu.add_radiobutton(label="理学院", variable=aca, value=1, command=lambda m = win3:academy_selected(aca, mb, academy))
    filemenu.add_radiobutton(label="文学院", variable=aca, value=2, command=lambda m = win3:academy_selected(aca, mb, academy))
    filemenu.add_radiobutton(label="法学院", variable=aca, value=3, command=lambda m = win3:academy_selected(aca, mb, academy))
    filemenu.add_radiobutton(label="商学院", variable=aca, value=4, command=lambda m = win3:academy_selected(aca, mb, academy))
    filemenu.add_radiobutton(label="新闻学院", variable=aca, value=5, command=lambda m = win3:academy_selected(aca, mb, academy))
    filemenu.add_radiobutton(label="艺术学院", variable=aca, value=6, command=lambda m = win3:academy_selected(aca, mb, academy))
    mb.config(menu = filemenu)
    #性别
    Label(win3, text='性别:', font=("宋体", 15, "normal")).grid(column=2, row=5, sticky=E)
    var = IntVar()
    var.set(2)
    ttk.Radiobutton(win3, text='男', variable=var, value=1, command=lambda m = win3:sex_selected(var, sex)).grid(column=3, row=5, sticky=W)
    ttk.Radiobutton(win3, text='女', variable=var, value=0, command=lambda m = win3:sex_selected(var, sex)).grid(column=3, row=5, sticky=E)
    #注册
    ttk.Button(win3, text='注册',command=lambda m = win3:register(m, name, sex, academy, stuID)).grid(column=2, columnspan=2, row=7, sticky=(E,W))




    #在每个控件周围添加一小点距离
    for child in win3.winfo_children():child.grid_configure(padx=5, pady=8)

#-----------------------我是一条帅气的分界线-----------------------------
#                           这是登陆窗口
#创建主窗口
root = Tk()
root.title('STU Smartcard')
root.geometry('415x355+5+100')
#创建一个框架部件,用来控制所有控件
mainframe = ttk.Frame(root, padding='3 3 12 12')
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
#如果主窗口改变大小,框架应该扩展刚到其余空间
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

#显示图片label
filename = 'SmartCard.gif'
img = PhotoImage(file=filename)
Label(mainframe, image=img).grid(column=1, columnspan=2, row=1, rowspan=1)
Label(mainframe, text="", bg="#e7e7e7").grid(column=1, row=2)
Label(mainframe, text="", bg="#e7e7e7").grid(column=1, row=4)

#创建数据库和表(没有时,row[0]==0)
conn = sqlite3.connect('SmartCard.db')
print('打开数据库..')
count = conn.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='STUDENT'")
for row in count:
    print('数据库中有表个数:%d' %row[0])
if (row[0] == 0):
    print('数据库中没有表')
    print('创建表格...')
    conn.execute('''CREATE TABLE STUDENT
       (CARDID        INT,
       NAME           TEXT,
       SEX            TEXT,
       ACADEMY        TEXT,
       STUID          TEXT,
       SUM            REAL);''')
else:
    print('打印数据库')
    cursor = conn.execute("SELECT cardid, name, sex, academy, stuid, sum  from STUDENT")
    for row in cursor:
        print("CARDID = ", row[0])
        print("NAME = ", row[1])
        print("SEX = ", row[2])
        print("ACADEMY = ", row[3])
        print("STUID = ", row[4])
        print("SUM = ", row[5], "\n")
conn.close()
print('关闭数据库..')

#刷卡
num = StringVar()
num_entry = ttk.Entry(mainframe,width=17, textvariable=num)
num_entry.grid(column=1, row=3, sticky=E)
ttk.Button(mainframe, text='读取卡号', width=8, command=Window2).grid(column=2, row=3, sticky=W)

#注册
style = ttk.Style()
style.configure("BW.TLabel")
ttk.Button(mainframe, text='_新用户请注册用户_',style="BW.TLabel", command=Window3).grid(column=2, row=5, sticky=E)

#在每个控件周围添加一小点距离
for child in mainframe.winfo_children():child.grid_configure(padx=2, pady=5)
# #光标默认在num输入框内
num_entry.focus()
root.bind('<Return>')
root.mainloop()