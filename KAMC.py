# KAMC 键鼠连点器
# 键鼠控制 - Keyboard and mouse controller
# 制作者：昌龙XL -- 请认准原创，开放源码仅为大家学习，各位请自觉遵守！
# 当前版本：v1.3.0

# 界面库
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from tkinter import filedialog
from TkinterPlus import *
import sv_ttk
from PIL import Image, ImageTk
from pystray import MenuItem
import pystray

# 功能库
import pynput
import pynput.keyboard as kb
import pynput.mouse as mo
from file import *
import threading as td
import logging
import webbrowser as web
from ctypes import windll
import win32api
import win32con

# 工具库
import os
import sys
import copy
import time
import random
import pickle

start_time = time.time()

# 微秒级等待
def __sleep(sec):
    st = time.perf_counter()
    while time.perf_counter() - st < sec:
        pass

# 图片设置
def resize(w, h, w_box, h_box, pil_image):  
    ''' 
    resize a pil_image object so it will fit into 
    a box of size w_box times h_box, but retain aspect ratio 
    对一个pil_image对象进行缩放，让它在一个矩形框内，还能保持比例 
    '''  
    f1 = 1.0*w_box/w
    f2 = 1.0*h_box/h
    factor = min([f1, f2])
    width = int(w*factor)
    height = int(h*factor)
    return pil_image.resize((width, height))

def openPic(path,width,height):
    w_box = width
    h_box = height
    pil_image = Image.open(path)
    w, h = pil_image.size
    pil_image_resized = resize(w, h, w_box, h_box, pil_image)
    tk_image = ImageTk.PhotoImage(pil_image_resized)
    return tk_image

#由键获取值（字典）
def get_key_by_value(dictionary, value):
    try:
        inverted_dict = {v: k for k, v in dictionary.items()}
        return inverted_dict.get(value)
    except:
        return None

# 窗口设置
root = tk.Tk()

root.title(' 键鼠控制 - Keyboard and mouse controller')
root.resizable(0,0) # type: ignore

sw = root.winfo_screenwidth()
sh = root.winfo_screenheight()

ww = 450
wh = 340

x = (sw-ww) / 2
y = (sh-wh) / 2
root.geometry("%dx%d+%d+%d" %(ww,wh,x,y))

#窗口宽450，高340
#标签页内宽450，高270

# 列表：用户设置
Theme = pickle.loads(BinaryReadFile('./UsersTheme.pkl'))

# 窗口移动

def MouseDown(event):
    global mousX
    global mousY
    mousX=event.x
    mousY=event.y

def MouseMove(event):
    root.geometry(f'+{event.x_root - mousX}+{event.y_root - mousY}')

move = tk.Canvas(root,highlightthickness=0,width=460,height=30)
move.config(bg="#E7E7E7")
move.pack(fill=Y)

move.bind("<Button-1>",MouseDown)
move.bind("<B1-Motion>",MouseMove)

# 窗口顶部项目

# 图标
icon_tk_image = openPic('./KAMC_icon.ico',25,25)
icon_img = tk.Label(root, image=icon_tk_image, width=25, height=25) 
icon_img.place(x=3,y=3)
icon_img.config(bg="#E7E7E7")

move.create_text(160,18,text="键鼠控制 - Keyboard and mouse controller")

# 日志

log_is_show = False

log_root = Frame(root)
log_root.place(x=0,y=35,width=450,height=310)

log_title_Label = Label(log_root,text='运行日志',font=('Segoe UI',11))
log_title_Label.pack(pady=3,fill=Y)

scrollx = Scrollbar(log_root, orient=HORIZONTAL)
scrollx.pack(side=BOTTOM,fill=X)
scrolly = Scrollbar(log_root)
scrolly.pack(side=RIGHT,fill=Y)

Fl = ('Segoe UI',9)
log_text = Text(log_root,wrap="none",font=Fl,cursor='arrow')
log_text.pack(fill=tk.BOTH,expand=True)

scrollx.config(command=log_text.xview)
log_text.config(yscrollcommand=scrollx.set)

scrolly.config(command=log_text.yview)
log_text.config(yscrollcommand=scrolly.set)

# 重定向控制台输出到一个文件
logging.basicConfig(level=logging.INFO, format='%(message)s')

color = None
lposition = END
# 创建一个自定义的日志处理器
class TextHandler(logging.Handler):
    def emit(self, record):
        global LOG,color,lposition
        msg = self.format(record)
        if color != None:
            log_text.tag_config(color, foreground=color, font=Fl)
            log_text.insert(lposition, msg + '\n', color)
        else:
            log_text.insert(lposition, msg + '\n')
        log_text.see(lposition)

# 将自定义的处理器添加到logging模块中
logger = logging.getLogger()
logger.addHandler(TextHandler())

def OL(_text='',_color=None,lposition1=END):
    global color,lposition
    color = _color
    lposition = lposition1
    logger.info(str(_text))
    color = None
    lposition = END

def log_show():
    global Log,log_is_show,log_root,log_text,U
    if not log_is_show:
        log_is_show = True
        logback.lift()
        log_root.lift()
    else:
        log_is_show = False
        U = log_is_show
        log_root.lower()
        logback.lower()

def In_log_text(event):
    log_root.focus_set()

log_text.bind('<FocusIn>',In_log_text)

logback_icon = openPic('./Pic/light/back.png',20,20)
logback_icon_dark = openPic('./Pic/dark/back.png',20,20)

logback = tk.Button(root, 
                    image=logback_icon, 
                    bd=0, 
                    relief=tk.FLAT,
                    font=("Segoe UI",10),
                    activebackground="#D2D2D2",
                    activeforeground="#010101",
                    command=log_show)
logback.config(bg="#E7E7E7")
logback.place(x=342,y=0,width=36,height=36)

# 主题
ld = Theme[0]

def light_dark(mode=0):
    global ld,mp_p
    if mode == 0:
        if ld == 'light':
            ld = 'dark'
            logback.config(bg="#2F2F2F",image=logback_icon_dark,activebackground='#505050',activeforeground="#ffffff")
            menu.config(bg="#2F2F2F",activebackground='#505050')
            mp.button_config_all(activebackground='#464646',activeforeground='#ffffff',bg='#2F2F2F')
            mp.config(sidecolor='#646464')
            small.config(bg="#2F2F2F",activebackground='#505050',activeforeground="#ffffff")
            close.config(bg="#2F2F2F")
            move.config(bg="#2F2F2F")
            bg_fill1.config(bg="#2F2F2F")
            bg_fill2.config(bg="#2F2F2F")
            icon_img.config(bg="#2F2F2F")
            move.delete(tk.ALL)
            move.create_text(160,18,text="键鼠控制 - Keyboard and mouse controller",fill='white')
        else:
            ld = 'light'
            logback.config(bg="#E7E7E7",image=logback_icon,activebackground="#D2D2D2",activeforeground="#010101")
            menu.config(bg="#E7E7E7",activebackground="#D2D2D2")
            mp.button_config_all(activebackground='#FAFAFA',activeforeground='#010101',bg='#E7E7E7')
            mp.config(sidecolor='#DCDCDC')
            small.config(bg="#E7E7E7",activebackground="#D2D2D2",activeforeground="#010101")
            close.config(bg="#E7E7E7")
            move.config(bg="#E7E7E7")
            bg_fill1.config(bg="#E7E7E7")
            bg_fill2.config(bg="#E7E7E7")
            icon_img.config(bg="#E7E7E7")
            move.delete(tk.ALL)
            move.create_text(160,18,text="键鼠控制 - Keyboard and mouse controller",fill='black')
    elif mode == 1:
        if ld == 'dark':
            logback.config(bg="#2F2F2F",image=logback_icon_dark,activebackground='#505050',activeforeground="#ffffff")
            menu.config(bg="#2F2F2F",activebackground='#505050')
            mp.button_config_all(activebackground='#464646',activeforeground='#ffffff',bg='#2F2F2F')
            mp.config(sidecolor='#646464')
            small.config(bg="#2F2F2F",activebackground='#505050',activeforeground="#ffffff")
            close.config(bg="#2F2F2F")
            move.config(bg="#2F2F2F")
            bg_fill1.config(bg="#2F2F2F")
            bg_fill2.config(bg="#2F2F2F")
            icon_img.config(bg="#2F2F2F")
            move.delete(tk.ALL)
            move.create_text(160,18,text="键鼠控制 - Keyboard and mouse controller",fill='white')
        else:
            logback.config(bg="#E7E7E7",image=logback_icon,activebackground="#D2D2D2",activeforeground="#010101")
            menu.config(bg="#E7E7E7",activebackground="#D2D2D2")
            mp.button_config_all(activebackground='#FAFAFA',activeforeground='#010101',bg='#E7E7E7')
            mp.config(sidecolor='#DCDCDC')
            small.config(bg="#E7E7E7",activebackground="#D2D2D2",activeforeground="#010101")
            close.config(bg="#E7E7E7")
            move.config(bg="#E7E7E7")
            bg_fill1.config(bg="#E7E7E7")
            bg_fill2.config(bg="#E7E7E7")
            icon_img.config(bg="#E7E7E7")
            move.delete(tk.ALL)
            move.create_text(160,18,text="键鼠控制 - Keyboard and mouse controller",fill='black')
    else:
        print(f'Error Mode {mode}')
    if ld == 'light':
        if mp_p == 0:
            menu.config(image=ddm_img)
        elif mp_p == 1:
            menu.config(image=ddm_img1)
    else:
        if mp_p == 0:
            menu.config(image=ddm_img_dark)
        elif mp_p == 1:
            menu.config(image=ddm_img_dark1)
    sv_ttk.set_theme(ld)

# 关于
string = decrypt('RW5jcnlwdGVkIHRleHQ=166.dll')
def how_use():
    global string
    messagebox.showinfo(' 关于',string, icon="question")

# 下拉菜单
def shuaxin():
    root.update()
    f1.update()
    Update_ScriptBox()
    f2.update()
    f3.update()
    light_dark(mode=1)
    messagebox.showinfo('提示',' 已刷新窗口.')
    OL('[#]已刷新','#ff7c3e')

mp = MenuPlus(root,width=120)
mp.add(text='明暗切换',command=light_dark)
mp.add(text='拓展功能',command=lambda:messagebox.showinfo('提示',' 敬请期待awa.'))
mp.add(text='窗口刷新',command=shuaxin)
mp.add(text='运行日志',command=log_show)
mp.add(text='前往官网',command=lambda:web.open('http://www.58html.com/html/view.php?logid=8570'))
mp.add(text='关于软件',command=how_use)
mp.button_config_all(activeforeground='#010101',bg='#EBEBEB')

mp_p = 0
def show_Menu():
    global mp_p,ld
    if mp_p == 0:
        if ld == 'light':
            menu.config(image=ddm_img1)
            
        else:
            menu.config(image=ddm_img_dark1)
            
        mp.place(x=302,y=35)
        mp.lift()
        mp_p = 1
    elif mp_p == 1:
        if ld == 'light':
            menu.config(image=ddm_img)
        else:
            menu.config(image=ddm_img_dark)
        mp.place(x=600,y=35)
        mp.lower()
        mp_p = 0

ddm_img = openPic("./Pic/light/ddm.png",20,20)
ddm_img1 = openPic("./Pic/light/ddm1.png",20,20)

ddm_img_dark = openPic("./Pic/dark/ddm.png",20,20)
ddm_img_dark1 = openPic("./Pic/dark/ddm1.png",20,20)

menu = tk.Button(root, 
                 image=ddm_img, 
                 bd=0, 
                 relief=tk.FLAT, 
                 font=("Segoe UI",12), 
                 command=show_Menu,
                 activebackground="#D2D2D2",
                 anchor='center')
menu.config(bg="#E7E7E7")
menu.place(x=342,y=0,width=36,height=36)

# 最小化窗口按钮
c = 0
smroot = False
def small_root():
    global smroot
    root.overrideredirect(False)
    root.iconify()
    root.bind('<Map>',re_root) # type: ignore
    smroot = True
    time.sleep(0.05)

def re_root(event=0):
    global c
    c += 1
    if c == 2:
        root.unbind('<Map>')
        root.deiconify()
        root.overrideredirect(True)
        c = 0
        root.after(10, lambda: set_appwindow(root=root))
    time.sleep(0.05)
    
wd = False
tray_timer = ''
def trayroot_pressed(event):
    global tray_timer
    try:
        tray_timer = root.after(600, Tray_root)  # 设置计时器
    except:
        pass

def trayroot_released(event):
    try:
        root.after_cancel(tray_timer)  # 取消计时器
    except:
        pass

def Tray_root():
    global wd,tray_timer
    try:
        root.after_cancel(tray_timer)
    except:
        pass
    if not wd:
        root.withdraw()
        wd = True

def reTray_root():
    global wd
    if wd:
        root.wm_deiconify()
        wd = False
    if smroot:
        re_root()

small = tk.Button(root, 
                  text="__", 
                  bd=0, 
                  relief=tk.FLAT,
                  font=("微软雅黑",10),
                  activebackground="#D2D2D2",
                  activeforeground="#010101",
                  command=small_root,
                  anchor='center')
small.config(bg="#E7E7E7")
small.place(x=378,y=-2,width=36,height=38)

small.bind("<Button-1>", trayroot_pressed)
small.bind("<ButtonRelease-1>", trayroot_released)

# 关闭窗口按钮
def on_closing(event=0,mode=True):
    global Theme,stop,ld
    BinaryWriteFile('./User_Action_Retention.pkl',pickle.dumps(__set__))
    Theme = [ld, 
             f1CB1['value'].index(f1CB1.get()),
             [
              f1CB2['value'].index(f1CB2.get()),
              int(f1CB2_C_SB1_value1.get()),
              int(f1CB2_C_SB1_value2.get())
             ],
             f1CB3['value'].index(f1CB3.get()),
             float(f1Sc1.get()),
             int(f1CB3switch_Var.get())]
    BinaryWriteFile('./UsersTheme.pkl',pickle.dumps(Theme))
    try:
        root.destroy()
        stop = True
        Trayicon.stop()
        if mode:
            os._exit(0)
    except:
        os._exit(0)

restart_timer = ''
def close_pressed(event):
    global restart_timer
    try:
        restart_timer = root.after(600, restart)  # 设置计时器
    except:
        pass

def close_released(event):
    try:
        root.after_cancel(restart_timer)  # 取消计时器
    except:
        pass

def restart():
    try:
        root.after_cancel(restart_timer)
        on_closing(mode=False)
        p = sys.executable
        try:
            s = os.path.join(os.getcwd(), './KAMC.py')
        except:
            s = os.path.join(os.getcwd(), './KAMC.exe')
        os.execl(p, p, s)
    except:
        pass

close = tk.Button(root, 
                  text="╳", 
                  bd=0, 
                  relief=tk.FLAT, 
                  highlightthickness=0, 
                  font=("微软雅黑",14), 
                  command=on_closing, 
                  activebackground="red", 
                  anchor='sw',
                  padx=8,pady=4)
close.config(bg="#E7E7E7")
close.place(x=417,y=0,width=40,height=36)

close.bind("<Button-1>", close_pressed)
close.bind("<ButtonRelease-1>", close_released)

# 系统托盘
def click_Traymenu(icon, item):
    print("点击了", item)

def on_exit(Trayicon, item):
    global Theme,ld
    BinaryWriteFile('./User_Action_Retention.pkl',pickle.dumps(__set__))
    Theme = [ld, 
             f1CB1['value'].index(f1CB1.get()),
             [
              f1CB2['value'].index(f1CB2.get()),
              int(f1CB2_C_SB1_value1.get()),
              int(f1CB2_C_SB1_value2.get())
             ],
             f1CB3['value'].index(f1CB3.get()),
             float(f1Sc1.get()),
             int(f1CB3switch_Var.get())]
    BinaryWriteFile('./UsersTheme.pkl',pickle.dumps(Theme))
    os._exit(0)

def notify(Trayicon: pystray.Icon):
    Trayicon.notify("测试消息", "KAMC")

Traymenu = (MenuItem(text='显示窗口', action=reTray_root),
            MenuItem(text='退出', action=on_exit),
            MenuItem(text='KAMC', action=reTray_root, default=True, visible=False)
           )
Trayimage = Image.open("./KAMC_icon.ico")
Trayicon = pystray.Icon("KAMC", Trayimage, "KAMC", Traymenu)
def iconRUN():
    Trayicon.run()

iR = td.Thread(target=iconRUN)
iR.start()

# 变量设置
mouse = pynput.mouse.Controller()            # 键鼠控制组件
keyboard = pynput.keyboard.Controller()

CBw = 240              # CB组件长度
Font__ = ('Segoe UI', 11)

stop = False            # 多线程开关

RUN_Press = False       # 连点开关

Hotkeys_ = {'关闭 - OFF' : False,
            }

Hotkeys_.update(ALL_Press)

# 将焦点移回窗口
def fs_root(event):
    root.focus_set()

def fs_f1(event=0):
    f1.focus_set()

def fs_f2(event=0):
    f2.focus_set()

def fs_fES(event=0):
    f_ES.focus_set()

# 标签页
NB1 = Notebook(root)
NB1.pack(fill=tk.BOTH, expand=True)

f1 = Frame()
f2 = Frame()
f3 = Frame()

NB1.add(f1, text='  键鼠连点  ')
NB1.add(f2, text='  操作脚本  ')
NB1.add(f3, text='  定时任务  ')

# f1 的界面 ----------------------------------------------------------+

f1_Ground = Frame(f1)
f1_Ground.place(x=0,y=0,width=450,height=360)

def f1_wheel(event):
    if event.delta > 0 and (f1_Ground.winfo_y() + (event.delta/2)) < 0:
        f1_Ground.place(x=0,y=f1_Ground.winfo_y() + (event.delta/2))
    elif event.delta > 0 and (f1_Ground.winfo_y() + (event.delta/2)) >= 0:
        f1_Ground.place(x=0,y=0)
    elif event.delta < 0 and (f1_Ground.winfo_y() + (event.delta/2)) > -90:
        f1_Ground.place(x=0,y=f1_Ground.winfo_y() + (event.delta/2))
    elif event.delta < 0 and (f1_Ground.winfo_y() + (event.delta/2)) <= -90:
        f1_Ground.place(x=0,y=-90)
    
f1.bind("<MouseWheel>",f1_wheel)
f1_Ground.bind("<MouseWheel>",f1_wheel)

   # 连击目标
f1L1 = Label(f1_Ground,text="连击目标 - Click target",font=Font__)
f1L1.place(x=12,y=10)

f1CB1_Canvas = tk.Canvas(f1_Ground,highlightthickness=0)
f1CB1_Canvas.place(x=7,y=34,width=CBw+2,height=35)

f1CB1 = Combobox(f1_Ground,state="readonly",font=Font__)

ALL_Press_Key = []
for item in ALL_Press:
    ALL_Press_Key.append(item)
ALL_Press_Key = tuple(ALL_Press_Key)

f1CB1['value'] = ALL_Press_Key
f1CB1.current(Theme[1])
f1CB1.place(x=8,y=35,width=CBw)

   # 连击间隔
Click_sec = None

def set_sec():
    global Click_sec,f1CB2
    def Execute(_a,_b=Click_sec):
        global Click_sec
        if f1Sc1.get() > 0:
            a = _b - abs(Click_sec * (f1Sc1.get()/100))
            if a < 0:
                a = 0.0
            b = _b + abs(Click_sec * (f1Sc1.get()/100))
            if b < 0:
                b = 0.0
            Click_sec = abs(random.uniform(a, b))
            f1Sc1_L2.config(text='实际间隔时间：( '+str(round(a,4))+' ~ '+str(round(b,4))+' ) '+str(Click_sec)+' s')
        else:
            f1Sc1_L2.config(text='实际间隔时间：'+_a+' s')
    while not stop:
        if f1CB2.get() == '自定义（单位：ms / clk）':
            if int(f1CB2_C_SB1.winfo_x()) == 600:
                f1CB2_C_SB1.place(x=270)
            Click_sec = ( int(f1CB2_C_SB1.get()) / 1000 ) - 0.008
            if not RUN_Press:
                f1Sc1.config(state='normal')
            Execute(str(Click_sec+0.008),( int(f1CB2_C_SB1.get()) / 1000 ))
        elif f1CB2.get() == '自定义（单位：cps / s）':
            if int(f1CB2_C_SB1.winfo_x()) == 600:
                f1CB2_C_SB1.place(x=270)
            Click_sec = ( 1 / int(f1CB2_C_SB1.get()) ) - 0.008
            if not RUN_Press:
                f1Sc1.config(state='normal')
            Execute(str(Click_sec+0.008),( 1 / int(f1CB2_C_SB1.get()) ))
        elif f1CB2.get() == '能多快有多快 - Max_Speed':
            if int(f1CB2_C_SB1.winfo_x()) == 270:
                f1CB2_C_SB1.place(x=600)
            Click_sec = 0
            if not RUN_Press:
                f1Sc1.config(state='disabled')
            f1Sc1_L2.config(text='实际间隔时间：0 s')
        elif f1CB2.get() == '极致连点 - Extreme_Click':
            if int(f1CB2_C_SB1.winfo_x()) == 270:
                f1CB2_C_SB1.place(x=600)
            Click_sec = 'extreme'
            if not RUN_Press:
                f1Sc1.config(state='disabled')
            f1Sc1_L2.config(text='实际间隔时间：无')
        else:
            if int(f1CB2_C_SB1.winfo_x()) == 270:
                f1CB2_C_SB1.place(x=600)
            try:
                Click_sec = float(f1CB2.get()[:-2]) - 0.008
            except:
                Click_sec = 0.1
            if not RUN_Press:
                f1Sc1.config(state='normal')
            Execute(str(float(f1CB2.get()[:-2])),float(f1CB2.get()[:-2]))
        time.sleep(0.01)

f1L2 = Label(f1_Ground,text="连击间隔 - Click interval",font=Font__)
f1L2.place(x=12,y=80)
f1CB2 = Combobox(f1_Ground,state="readonly",font=Font__)
f1CB2['value'] = ('0.01 s','0.05 s','0.1 s','0.2 s','0.5 s','1 s',
                  '能多快有多快 - Max_Speed',
                  '极致连点 - Extreme_Click',
                  '自定义（单位：ms / clk）',
                  '自定义（单位：cps / s）')
f1CB2.current(Theme[2][0])
f1CB2.place(x=8,y=105,width=CBw)

def f1CB2_SB1_validate_input(text):
    try:
        if f1CB2.get() == '自定义（单位：ms / clk）':
            if text.isdigit() and 1 <= int(text):
                return True
            else:
                return False
        elif f1CB2.get() == '自定义（单位：cps / s）':
            if text.isdigit() and 1 <= int(text) <= 1000:
                return True
            else:
                return False
        else:
            return False
    except:
        return False

f1CB2_C_SB1_value1 = tk.StringVar()
f1CB2_C_SB1_value1.set(Theme[2][1])

f1CB2_C_SB1_value2 = tk.StringVar()
f1CB2_C_SB1_value2.set(Theme[2][2])

f1CB2_C_SB1 = Spinbox(f1_Ground,font=Font__,from_=1,to=1000,
                      textvariable=f1CB2_C_SB1_value1,
                      validate='key')
f1CB2_C_SB1["validatecommand"] = (f1CB2_C_SB1.register(f1CB2_SB1_validate_input), "%P")
f1CB2_C_SB1.place(x=600,y=105,width=140)
def f1CB2_C_SB1_set__(event):
    if f1CB2.get() == '自定义（单位：ms / clk）':
        f1CB2_C_SB1.config(textvariable=f1CB2_C_SB1_value1)
    elif f1CB2.get() == '自定义（单位：cps / s）':
        f1CB2_C_SB1.config(textvariable=f1CB2_C_SB1_value2)
f1CB2.bind('<<ComboboxSelected>>',f1CB2_C_SB1_set__)

   # 开关热键
f1L3 = Label(f1_Ground,text="开关热键 - Switch Hotkeys",font=Font__)
f1L3.place(x=12,y=150)

f1CB3_Canvas = tk.Canvas(f1_Ground,highlightthickness=0)
f1CB3_Canvas.place(x=7,y=174,width=CBw+2,height=35)

f1CB3 = Combobox(f1_Ground,state="readonly",font=Font__)

Hotkeys_Key = []
for item in Hotkeys_:
    Hotkeys_Key.append(item)
Hotkeys_Key = tuple(Hotkeys_Key)

f1CB3['value'] = Hotkeys_Key
f1CB3.current(Theme[3])
f1CB3.place(x=8,y=175,width=CBw)

f1CB3switch_Var = StringVar(value=str(Theme[5]))
f1CB3switch = Checkbutton(f1_Ground, text=" 长按触发", style="Switch.TCheckbutton",variable=f1CB3switch_Var)
f1CB3switch.place(x=268,y=178)


f1L4 = Label(f1_Ground,text='随机延迟 - Random Delay',font=Font__)
f1L4.place(x=12,y=230)
f1Sc1 = Scale(f1_Ground, from_=0.0, to=300.0,length=240,orient="horizontal")
f1Sc1.place(x=12,y=255)
f1Sc1.set(Theme[4])
f1Sc1_L1 = Label(f1_Ground,text='0.0 %',font=('微软雅黑',11))
f1Sc1_L1.place(x=260,y=254)
f1Sc1_L2 = Label(f1_Ground,text='实际间隔时间：NaN',font=('微软雅黑',10))
f1Sc1_L2.place(x=12,y=280)

allow_click = True
def f1Sc1_get_show():
    global allow_click
    while True:
        a = f1Sc1.get()
        f1Sc1_L1.config(text=str(round(a,1))+' %')
        if f1CB1.get() == f1CB3.get():
            allow_click = False
            f1CB1_Canvas.config(bg='#ff0000')
            f1CB3_Canvas.config(bg='#ff0000')
        else:
            allow_click = True
            if ld == 'light':   
                f1CB1_Canvas.config(bg='#fafafa')
                f1CB3_Canvas.config(bg='#fafafa')
            elif ld == 'dark':
                f1CB1_Canvas.config(bg='#1c1c1c')
                f1CB3_Canvas.config(bg='#1c1c1c')
        time.sleep(0.01)

for item in f1_Ground.winfo_children():
    item.bind("<MouseWheel>",f1_wheel)

# f2的界面 ----------------------------------------------------------+
__set__ = {}
call_print = 0
try:
    __set__ = pickle.loads(BinaryReadFile('User_Action_Retention.pkl'))
except:
    call_print = 1
    BinaryWriteFile('User_Action_Retention.pkl',pickle.dumps({}))
ScriptDataRecord = {}

Wm1_de_index = 0 #插入的位置
WAmode = 0 #想要如何添加，0为‘添加’，1为‘插入’
AddMode = 0 #所添加的模式
get__ = None #获取

O_Temporary_List = [] #原本临时脚本列表
Temporary_List = [] #临时脚本列表
IndexRecord = None #记录序号

Is_Edit_ = False

_y = 0

def Copy_O_T_to_T(index=None):
    global O_Temporary_List,IndexRecord
    O_Temporary_List = copy.deepcopy(Temporary_List)
    if index != None:
        IndexRecord = index

def Delete__set__Project(index):
    global __set__,ScriptDataRecord
    ls_l = []
    for j in __set__.values():
        ls_l.append(j)
    try:
        ls_l.pop(int(index))
        for widget in f2_Ground.winfo_children():
            widget.destroy()
        ScriptDataRecord.clear()
        f2_Ground.update()
        __set__.clear()
        for j,item in enumerate(ls_l):
            __set__[j] = item
        f2_Ground.update()
        Update_ScriptBox(__set__)
    except:
        f2_Ground.update()
        Update_ScriptBox(__set__)

def Is_Edit_become_True():
    global Is_Edit_
    Is_Edit_ = True

def Update_ScriptBox(f=__set__):
    global _y,ScriptDataRecord
    ScriptDataRecord = {}
    _y = 5
    for i,item in enumerate(f.values()):
        name = str(item[1])
        
        frame = tk.Frame(f2_Ground)
        frame.place(x=5, y=_y, width=437, height=40)
        ScriptDataRecord['frame'+str(i)] = frame

        bg_button = Button(ScriptDataRecord['frame'+str(i)],
                           command=lambda i=i:
                               (exec('f_ES_E1.delete(0,END)'),
                                eval('f_ES_E1.insert(END,__set__['+str(i)+'][1])'),
                                exec('Copy_O_T_to_T('+str(i)+')'),
                                exec('Update_List(__set__['+str(i)+'][4])'),
                                exec('f_ES.lift()'),
                                exec('Is_Edit_become_True()')
                               )
                           )
        bg_button.pack(fill=BOTH, expand=1)
        bg_button.bind("<Button-1>", fs_fES) # type: ignore
        ScriptDataRecord['bg_button'+str(i)] = bg_button

        ED = BooleanVar()
        ED_button = Checkbutton(ScriptDataRecord["bg_button"+str(i)],
                                variable=ED,
                                style="Switch.TCheckbutton",
                                command=lambda i=i: 
                                    (exec('__set__['+str(i)+'][2] = ScriptDataRecord["ED"+str('+str(i)+')].get()')
                                    ) 
                                )
        ED_button.place(x=10, y=6)
        ED.set(eval(str(f[i][2])))
        ScriptDataRecord['ED'+str(i)] = ED
        ScriptDataRecord['ED_button'+str(i)] = ED_button

        L_name = Label(ScriptDataRecord['bg_button'+str(i)], text=name)
        L_name.place(x=65, y=10)
        ScriptDataRecord['L_name'+str(i)] = L_name
        
        Delete_button = tk.Button(ScriptDataRecord['bg_button'+str(i)],
                                  relief=FLAT,
                                  bd = 0,
                                  text='⚫',
                                  command=lambda i=i:
                                    (exec('a = messagebox.askyesno(" 提示", "确认删除脚本 '+str(name)+' 吗？",icon="warning")'),
                                     exec('Delete__set__Project(int('+str(i)+'))') if eval('a') else exec('pass')
                                    )
                                 )
        Delete_button.place(x=402,y=5,width=30,height=30)
        ScriptDataRecord['Delete_button'+str(i)] = Delete_button
        
        _y += 45

    if _y > 270:
        f2_Ground.place(height=_y+20)
    else:
        f2_Ground.place(height=271)

    for child in ScriptDataRecord.values():
        try:
            child.bind("<MouseWheel>",f2_Ground_wheel)
        except:
            pass
    
    children = f2_Ground.master.winfo_children()
    if f2_Ground == children[-1]:
        f2bottom.lift()
        
def f2_Ground_wheel(event):
    addy = int(event.delta)/30
    nowy = f2_Ground.winfo_y()
    if _y > 180:
        if addy > 0 and nowy < 0:
            f2_Ground.place(y=nowy + addy)
        elif addy < 0 and nowy > -(_y - 170):
            f2_Ground.place(y=nowy + addy)
        # 修正位置
        nowy = f2_Ground.winfo_y()
        if nowy > 0:
            f2_Ground.place(y=0)
        elif nowy < -(_y - 170):
            f2_Ground.place(y=-(_y - 170))
    f2_Ground.update()
    
def NewScript():
    global Temporary_List,IndexRecord,Is_Edit_
    Temporary_List = []
    f_ES_E1.delete(0,END)
    f_ES_E1.insert(END,'# 新脚本')
    Update_List([])
    Copy_O_T_to_T()
    IndexRecord = len(__set__)
    f_ES.lift()
    Is_Edit_ = True

def OpenScript():
    global __set__
    file_path = filedialog.askopenfilename(title='导入 KAMC 脚本',
                                           filetypes=(("KAMC files", "*.kamc"),("Text files", "*.txt"))
    )
    if file_path != '':
        try:
            data = pickle.loads(BinaryReadFile(file_path))
            __set__[int(len(__set__))] = data
            Update_ScriptBox(__set__)
            OL(f'[F]成功导入脚本 {data[1]}',
            '#1E90FF')
        except:
            OL(f'[F]导入脚本 {data[1]} 时出现错误',
            '#1E90FF')
            

f2_Ground = tk.Frame(f2)
f2_Ground.place(x=0,y=0,width=450,height=270)

f2bottom = tk.Frame(f2)
f2bottom.place(x=0,y=170,width=450,height=100)

f2B1 = Button(f2bottom, text='新建脚本',command=NewScript)
f2B1.place(x=25,y=30,width=200, height=50)

f2B1 = Button(f2bottom, text='录制脚本',state="disabled",cursor='no')
f2B1.place(x=230,y=30,width=95, height=50)

f2B1 = Button(f2bottom, text='导入脚本',command=OpenScript)
f2B1.place(x=330,y=30,width=95, height=50)


f_ES = Frame(f2)
f_ES.place(x=0,y=0,width=450,height=270)

def Update_List(TL):
    global Temporary_List
    Temporary_List = copy.deepcopy(TL)
    f_ES_List1.delete(0,END)
    try:
        f_ES_CB1.current(ALL_Press_Key.index(get_key_by_value(ALL_Press,__set__[int(IndexRecord)][3]))) # type: ignore
    except:
        pass
    for item in TL:
        if item[0] == '0':
            f_ES_List1.insert(END,' ┌重复执行直到再次触发')
        elif item[0] == '1':
            f_ES_List1.insert(END,f' 等待 {item[1]} 毫秒')
        elif item[0] == '2':
            f_ES_List1.insert(END,f' 鼠标 移到 x{item[1]}，y{item[2]}')
        elif item[0] == '3':
            f_ES_List1.insert(END,f' 鼠标 点击 {get_key_by_value(Mouse_Press,item[1])} 键')
        elif item[0] == '4':
            f_ES_List1.insert(END,f' 键盘 点击 {get_key_by_value(Key_Press,item[1])} 键')
        elif item[0] == '5':
            f_ES_List1.insert(END,f' 输入 “ {item[1]} ”')
        else:
            pass


def Add_S():
    global Wm1_de_index,WAmode,AddMode
    f_ES_f_Add.lift()
    f_ES_f_Add_CB1.config(state="editable")
    f_ES_f_Add_CB1.delete(0,END)
    f_ES_f_Add_CB1.insert(END,'--请选择--')
    f_ES_f_Add_CB1.config(state="readonly")
    JudgmentOptions()
    AddMode = 0
    WAmode = 0

def Delete_S():
    global get__
    get__ = f_ES_List1.curselection()
    c = 0
    for i in get__:
        i1 = i - c
        f_ES_List1.delete(int(i1))
        Temporary_List.pop(int(i1))
        c += 1

def Insert_S():
    global get__,Wm1_de_index,WAmode,AddMode
    get__ = f_ES_List1.curselection()
    if len(get__) == 1:
        AddMode = 0
        WAmode = 1
        Wm1_de_index = int(get__[0])

        f_ES_f_Add.lift()
        f_ES_f_Add_CB1.config(state="editable")
        f_ES_f_Add_CB1.delete(0,END)
        f_ES_f_Add_CB1.insert(END,'--请选择--')
        f_ES_f_Add_CB1.config(state="readonly")
        JudgmentOptions()
    elif len(get__) == 0:
        messagebox.showinfo(' 提示','请选择插入的位置.')
    elif len(get__) >= 2:
        messagebox.showinfo(' 提示','请只选择一项.')
    else:
        pass

f_ES_L1 = Label(f_ES,text='名称：')
f_ES_L1.place(x=5,y=3)
f_ES_E1 = tk.Entry(f_ES)
f_ES_E1.place(x=50,y=4,width=100,height=20)

f_ES_ListF = Frame(f_ES)
f_ES_ListF.place(x=5,y=30,width=200,height=230)

     # 垂直滚动条
f_ES_List1_scrollbar_y = ttk.Scrollbar(f_ES_ListF)
f_ES_List1_scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

     # 水平滚动条
f_ES_List1_scrollbar_x = ttk.Scrollbar(f_ES_ListF, orient=tk.HORIZONTAL)
f_ES_List1_scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

f_ES_List1 = Listbox(f_ES_ListF, selectmode=MULTIPLE)
f_ES_List1.pack(fill=BOTH,expand=True)

     # 滚动条关联
f_ES_List1.config(yscrollcommand=f_ES_List1_scrollbar_y.set,
                  xscrollcommand=f_ES_List1_scrollbar_x.set)
f_ES_List1_scrollbar_y.config(command=f_ES_List1.yview)
f_ES_List1_scrollbar_x.config(command=f_ES_List1.xview)
     # ----------

f_ES_B1 = Button(f_ES,text='添加',command=Add_S)
f_ES_B1.place(x=225,y=20,width=205,height=32)

f_ES_B2 = Button(f_ES,text='删除',command=Delete_S)
f_ES_B2.place(x=225,y=57,width=100,height=32)

f_ES_B3 = Button(f_ES,text='插入',command=Insert_S)
f_ES_B3.place(x=330,y=57,width=100,height=32)

f_ES_CB1 = Combobox(f_ES,state='readonly',font=Font__)
f_ES_CB1['value'] = ALL_Press_Key
f_ES_CB1.current(0)
f_ES_CB1.place(x=225,y=100,width=205,height=32)

def SaveChanges():
    global __set__,IndexRecord
    if IndexRecord == len(__set__):
        __set__[int(IndexRecord)] = [] # type: ignore
        __set__[int(IndexRecord)].append('0') # type: ignore
        __set__[int(IndexRecord)].append(f_ES_E1.get()) # type: ignore
        __set__[int(IndexRecord)].append(False) # type: ignore
        __set__[int(IndexRecord)].append(ALL_Press[f_ES_CB1.get()]) # type: ignore
        __set__[int(IndexRecord)].append(Temporary_List)      # type: ignore
    else:
        __set__[int(IndexRecord)][0] = '0' # type: ignore
        __set__[int(IndexRecord)][1] = f_ES_E1.get() # type: ignore
        __set__[int(IndexRecord)][3] = ALL_Press[f_ES_CB1.get()] # type: ignore
        __set__[int(IndexRecord)][4] = Temporary_List # type: ignore
    Copy_O_T_to_T()

def ExitEdit():
    global __set__,IndexRecord,Is_Edit_
    try:
        if (O_Temporary_List != Temporary_List or
            __set__[int(IndexRecord)][1] != f_ES_E1.get() or # type: ignore
            __set__[int(IndexRecord)][3] != ALL_Press[f_ES_CB1.get()]): # type: ignore
            c = messagebox.askyesnocancel(" 提示", "你还未保存，是否要保存？")
            if c == None:
                return
            elif c:
                SaveChanges()
                f2_Ground.lift()
                f2bottom.lift()
            else:
                f2_Ground.lift()
                f2bottom.lift()
        else:
            f2_Ground.lift()
            f2bottom.lift()
    except:
        c = messagebox.askyesnocancel(" 提示", "你还未保存，是否要保存？")
        if c == None:
            return
        elif c:
            SaveChanges()
            f2_Ground.lift()
            f2bottom.lift()
        else:
            f2_Ground.lift()
            f2bottom.lift()
    IndexRecord = None
    Update_ScriptBox(__set__)
    Is_Edit_ = False

def ExportFile():
    file_path = filedialog.asksaveasfilename(title='导出 KAMC 脚本',
                                             defaultextension=".kamc",
                                             filetypes=(("KAMC Files", "*.kamc"), ("Text Files", "*.txt")))
    if file_path != '':
        ls_l = []
        ls_l.append('0')
        ls_l.append(f_ES_E1.get())
        ls_l.append(False)
        ls_l.append(ALL_Press[f_ES_CB1.get()])
        ls_l.append(Temporary_List)
        BinaryWriteFile(file_path,pickle.dumps(ls_l))
        OL(f'[F]成功导出脚本 {f_ES_E1.get()}',
           '#1E90FF')

f_ES_B4 = Button(f_ES,text='保存',command=SaveChanges)
f_ES_B4.place(x=225,y=190,width=205,height=32)

f_ES_B5 = Button(f_ES,text='退出',command=ExitEdit)
f_ES_B5.place(x=225,y=227,width=100,height=32)

f_ES_B5 = Button(f_ES,text='导出',command=ExportFile)
f_ES_B5.place(x=330,y=227,width=100,height=32)

# 添加界面 ---------------------------
def To_Add():
    global Wm1_de_index,WAmode,AddMode,get__
    if WAmode == 0:
        if AddMode == 1:
            try:
                if Temporary_List[0][0] != '0':
                    Temporary_List.insert(0,['0'])
                else:
                    messagebox.showinfo(' 提示','脚本已启用“┌重复执行直到再次触发”语句.')
                    return
            except:
                Temporary_List.insert(0,['0'])
        elif AddMode == 2:
            Temporary_List.append(['1',int(f_ES_f_Add_Parameter_1.get())])
        elif AddMode == 3:
            Temporary_List.append(['2',int(f_ES_f_Add_Parameter_1.get()),int(f_ES_f_Add_Parameter_2.get()),Mouse_Press[f_ES_f_Add_Parameter_3.get()]])        
        elif AddMode == 4:
            Temporary_List.append(['3',Mouse_Press[f_ES_f_Add_Parameter_3.get()]])
        elif AddMode == 5:
            Temporary_List.append(['4',Key_Press[f_ES_f_Add_Parameter_3.get()]])
        elif AddMode == 6:
            Temporary_List.insert(Wm1_de_index + 1, ['5',f_ES_f_Add_Parameter_4.get()])
    elif WAmode == 1:
        if AddMode == 1:
            try:
                if Temporary_List[0][0] != '0':
                    Temporary_List.insert(0,['0'])
                else:
                    messagebox.showinfo(' 提示','脚本已启用“┌重复执行直到再次触发”语句.')
            except:
                Temporary_List.insert(0,['0'])
        elif AddMode == 2:
            Temporary_List.insert(Wm1_de_index + 1, ['1',int(f_ES_f_Add_Parameter_1.get())])
        elif AddMode == 3:
            Temporary_List.insert(Wm1_de_index + 1, ['2',int(f_ES_f_Add_Parameter_1.get()),int(f_ES_f_Add_Parameter_2.get())])        
        elif AddMode == 4:
            Temporary_List.insert(Wm1_de_index + 1, ['3',Mouse_Press[f_ES_f_Add_Parameter_3.get()]])
        elif AddMode == 5:
            Temporary_List.insert(Wm1_de_index + 1, ['4',Key_Press[f_ES_f_Add_Parameter_3.get()]])
        elif AddMode == 6:
            Temporary_List.insert(Wm1_de_index + 1, ['5',f_ES_f_Add_Parameter_4.get()])
    Update_List(Temporary_List)
    f_ES.lift()

f_ES_f_Add = Frame(f2)
f_ES_f_Add.place(x=0,y=0,width=450,height=270)

f_ES_f_Add_CB1 = Combobox(f_ES_f_Add,font=Font__)
f_ES_f_Add_CB1.place(x=100,y=30,width=250,height=35)
f_ES_f_Add_CB1['value'] = ['┌重复执行直到再次触发',
                           '等待 [ ] 毫秒',
                           '鼠标 移到 x[ ]，y[ ]',
                           '鼠标 点击 [ ] 键',
                           '键盘 点击 [ ] 键',
                           '输入 [ ]'
                           ]
f_ES_f_Add_CB1.insert(END,'--请选择--')
f_ES_f_Add_CB1.config(state="readonly")

  # 参数

def validate_input(new_value):
    try:
        value = float(new_value)
        if value < 0:
            return False
    except ValueError:
        return False
    return True

validate_func = root.register(validate_input)

f_ES_f_Add_Parameter_1_value = tk.StringVar()
f_ES_f_Add_Parameter_1_value.set("0")

f_ES_f_Add_Parameter_2_value = tk.StringVar()
f_ES_f_Add_Parameter_2_value.set("0")

f_ES_f_Add_Parameter_1_L = Label(f_ES_f_Add,text='参数1：',font=Font__)
f_ES_f_Add_Parameter_1_L.place(x=600,y=85)

f_ES_f_Add_Parameter_1 = Spinbox(f_ES_f_Add,from_=0,to=float('inf'),
                                 validate='key',
                                 validatecommand=(validate_func, '%P'),
                                 textvariable=f_ES_f_Add_Parameter_1_value)
f_ES_f_Add_Parameter_1.place(x=600,y=80,width=150,height=30)

f_ES_f_Add_Parameter_2_L = Label(f_ES_f_Add,text='参数2：',font=Font__)
f_ES_f_Add_Parameter_2_L.place(x=600,y=125)

f_ES_f_Add_Parameter_2 = Spinbox(f_ES_f_Add,from_=0,to=float('inf'),
                                 validate='key',
                                 validatecommand=(validate_func, '%P'),
                                 textvariable=f_ES_f_Add_Parameter_2_value)
f_ES_f_Add_Parameter_2.place(x=600,y=120,width=150,height=30)


f_ES_f_Add_Parameter_3 = Combobox(f_ES_f_Add,state='readonly')
f_ES_f_Add_Parameter_3.place(x=600,y=160,width=150,height=30)

f_ES_f_Add_Parameter_4 = Entry(f_ES_f_Add)
f_ES_f_Add_Parameter_4.place(x=600,y=160,width=190,height=29)

Mouse_Press_list = []
for item in Mouse_Press:
    Mouse_Press_list.append(item)
Mouse_Press_list = tuple(Mouse_Press_list)

Key_Press_list = []
for item in Key_Press:
    Key_Press_list.append(item)
Key_Press_list = tuple(Key_Press_list)

f_ES_f_Add_Parameter_3['value'] = Mouse_Press_list
f_ES_f_Add_Parameter_3.place(x=600,y=160,width=210,height=30)

f_ES_f_Add_B1 = Button(f_ES_f_Add,text='添加',command=To_Add)
f_ES_f_Add_B1.place(x=600,y=200,width=250,height=32)

def BackAdd():
    Update_List(Temporary_List)
    f_ES.lift()

f_ES_f_Add_B2 = Button(f_ES_f_Add,text='退出',command=BackAdd)
f_ES_f_Add_B2.place(x=100,y=240,width=250,height=32)


def clear__():
    f_ES_f_Add_Parameter_1_value.set("0")
    f_ES_f_Add_Parameter_2_value.set("0")
    f_ES_f_Add_Parameter_3.current(0)
    f_ES_f_Add_Parameter_4.delete(0,END)

def JudgmentOptions(event=0):
    global AddMode,get__
    get__ = f_ES_f_Add_CB1.get()
    if get__ == '┌重复执行直到再次触发':
        AddMode = 1
        f_ES_f_Add_Parameter_1.place(x=600)
        f_ES_f_Add_Parameter_1_L.place(x=600)
        f_ES_f_Add_Parameter_2.place(x=600)
        f_ES_f_Add_Parameter_2_L.place(x=600)
        f_ES_f_Add_Parameter_3.place(x=600,y=160)
        f_ES_f_Add_Parameter_4.place(x=600,y=160)
        f_ES_f_Add_B1.place(x=100,y=85)
        f_ES_f_Add_B2.place(x=100,y=125)
        clear__()
    elif get__ == '等待 [ ] 毫秒':
        AddMode = 2
        f_ES_f_Add_Parameter_1.place(x=155)
        f_ES_f_Add_Parameter_1_L.place(x=100)
        f_ES_f_Add_Parameter_2.place(x=600)
        f_ES_f_Add_Parameter_2_L.place(x=600)
        f_ES_f_Add_Parameter_3.place(x=600,y=160)
        f_ES_f_Add_Parameter_4.place(x=600,y=160)
        f_ES_f_Add_B1.place(x=100,y=125)
        f_ES_f_Add_B2.place(x=100,y=165)
        clear__()
    elif get__ == '鼠标 移到 x[ ]，y[ ]':
        AddMode = 3
        f_ES_f_Add_Parameter_1.place(x=155)
        f_ES_f_Add_Parameter_1_L.place(x=100)
        f_ES_f_Add_Parameter_2.place(x=155)
        f_ES_f_Add_Parameter_2_L.place(x=100)
        f_ES_f_Add_Parameter_3.place(x=600,y=160)
        f_ES_f_Add_Parameter_4.place(x=600,y=160)
        f_ES_f_Add_B1.place(x=100,y=165)
        f_ES_f_Add_B2.place(x=100,y=205)
        f_ES_f_Add_Parameter_3['value'] = Mouse_Press_list
        clear__()
    elif get__ == '鼠标 点击 [ ] 键':
        AddMode = 4
        f_ES_f_Add_Parameter_1.place(x=600)
        f_ES_f_Add_Parameter_1_L.place(x=90)
        f_ES_f_Add_Parameter_2.place(x=600)
        f_ES_f_Add_Parameter_2_L.place(x=600)
        f_ES_f_Add_Parameter_3.place(x=145,y=80)
        f_ES_f_Add_Parameter_4.place(x=600,y=160)
        f_ES_f_Add_B1.place(x=100,y=125)
        f_ES_f_Add_B2.place(x=100,y=165)
        f_ES_f_Add_Parameter_3['value'] = Mouse_Press_list
        clear__()
    elif get__ == '键盘 点击 [ ] 键':
        AddMode = 5
        f_ES_f_Add_Parameter_1.place(x=600)
        f_ES_f_Add_Parameter_1_L.place(x=90)
        f_ES_f_Add_Parameter_2.place(x=600)
        f_ES_f_Add_Parameter_2_L.place(x=600)
        f_ES_f_Add_Parameter_3.place(x=145,y=80)
        f_ES_f_Add_Parameter_4.place(x=600,y=160)
        f_ES_f_Add_B1.place(x=100,y=125)
        f_ES_f_Add_B2.place(x=100,y=165)
        f_ES_f_Add_Parameter_3['value'] = Key_Press_list
        clear__()
    elif get__ == '输入 [ ]':
        AddMode = 6
        f_ES_f_Add_Parameter_1.place(x=600)
        f_ES_f_Add_Parameter_1_L.place(x=100)
        f_ES_f_Add_Parameter_2.place(x=600)
        f_ES_f_Add_Parameter_2_L.place(x=600)
        f_ES_f_Add_Parameter_3.place(x=600,y=160)
        f_ES_f_Add_Parameter_4.place(x=155,y=80)
        f_ES_f_Add_B1.place(x=100,y=125)
        f_ES_f_Add_B2.place(x=100,y=165)
        f_ES_f_Add_Parameter_3['value'] = Mouse_Press_list
        clear__()
    else:
        f_ES_f_Add_Parameter_1.place(x=600)
        f_ES_f_Add_Parameter_1_L.place(x=600)
        f_ES_f_Add_Parameter_2.place(x=600)
        f_ES_f_Add_Parameter_2_L.place(x=600)
        f_ES_f_Add_Parameter_3.place(x=600)
        f_ES_f_Add_Parameter_4.place(x=600)
        f_ES_f_Add_B1.place(x=600)
        f_ES_f_Add_B2.place(x=100,y=85)
        f_ES_f_Add_Parameter_3['value'] = Mouse_Press_list
        clear__()

f_ES_f_Add_CB1.bind('<<ComboboxSelected>>',JudgmentOptions) # type: ignore

# ------------------------------------

f2_Ground.lift()
Update_ScriptBox(__set__)

# f3的界面 ----------------------------------------------------------+

f3L1 = Label(f3,text="敬请期待",font=("宋体",20))
f3L1.pack(anchor=tk.CENTER,expand=True)

# 键鼠点击事件
NB1.bind("<FocusIn>",fs_root)
f1CB1.bind("<<ComboboxSelected>>",fs_f1)
f2B1.bind("<Button-1>",fs_f2)
f1_Ground.bind("<Button-1>",fs_f1)
f2.bind("<Button-1>",fs_f2)
f2_Ground.bind("<Button-1>",fs_f2)
f2_Ground.bind("<MouseWheel>",f2_Ground_wheel)
f_ES.bind("<Button-1>",fs_fES)

gw = None
def ddm_back(event):
    global mp_p,gw
    try:
        gw = event.widget.winfo_containing(event.x_root, event.y_root)
        if gw != menu:
            for b in mp.All_MenuButton:
                if gw == b:
                    return
            else:
                if mp_p == 1:
                    show_Menu()
    except:
        pass
root.bind_all('<Button-1>',ddm_back)

# 多线程：解析脚本
sR_dict = {}
Rnum = 0

def ParsingScripts(index,script,m=mo.Controller()):
    global color
    def Execute():
        for i,item in enumerate(script):
            if Is_Edit_ or not sR_dict[index][1]:
                break
            else:
                if item[0] == '1':
                    ls_st = time.perf_counter()
                    while (time.perf_counter() - ls_st < float(item[1]/1000)) and (not Is_Edit_):
                        pass
                elif item[0] == '2':
                    m.position = (int(item[1]),int(item[2]))
                elif item[0] == '3':
                    if item[1] == 'M-1':
                        b = mo.Button.left
                    elif item[1] == 'M-2':
                        b = mo.Button.right
                    elif item[1] == 'M-3':
                        b = mo.Button.middle
                    m.click(button=b)
                elif item[0] == '4':
                    keyboard.press(item[1])
                    keyboard.release(item[1])
                elif item[0] == '5':
                    keyboard.type(item[1])
    Execute()
    if sR_dict[index][1]:
        while not(Is_Edit_ or not sR_dict[index][1]):
            Execute()
    __sleep(0.01)
    color = 'brown'
    logger.info('[-] 脚本 '+str(sR_dict[index][0])+' 结束运行，编号：'+str(index))
    color = None

# 多线程：启禁控件

ED = RUN_Press

def Enable_Disable():
    global ED
    while not stop:
        if ED != RUN_Press:
            if RUN_Press:
                f1CB3switch.config(state='disabled')
                f1CB1.config(state='disabled')
                f1CB2.config(state='disabled')
                f1CB3.config(state='disabled')
                f1Sc1.config(state='disabled')
                f1CB2_C_SB1.config(state='disabled')
            else:
                f1CB1.config(state='readonly')
                f1CB2.config(state='readonly')
                f1CB3.config(state='readonly')
                f1Sc1.config(state='normal')
                f1CB2_C_SB1.config(state='normal')
                f1CB3switch.config(state='normal')
            ED = RUN_Press
        time.sleep(0.001)

ED_set = td.Thread(target=Enable_Disable)
ED_set.start()

# 热键启动多线程

def start_press():
    global RUN_Press
    if RUN_Press:
        RUN_Press = False
        OL('[*] 键鼠连点 - OFF','red')
    else:
        RUN_Press = True
        OL('[*] 键鼠连点 - ON','#00CD00')

save_key = None
def key_on_press(key):
    global save_key
    print(f'按下了{key}')
    if int(f1CB3switch_Var.get()):
        if allow_click:
            if (Hotkeys_[f1CB3.get()] != False and
                Hotkeys_[f1CB3.get()] != 'M-1' and
                Hotkeys_[f1CB3.get()] != 'M-2' and
                Hotkeys_[f1CB3.get()] != 'M-3'):
                if (str(key).replace("'",'') == str(Hotkeys_[f1CB3.get()]) and 
                    str(key).replace("'",'') != save_key
                   ):
                    start_press()
                    save_key = str(key).replace("'",'')

def key_on_release(key):
    global allow_click,__set__,sR_dict,Rnum,Is_Edit_,save_key
    if allow_click:
        if (Hotkeys_[f1CB3.get()] != False and
            Hotkeys_[f1CB3.get()] != 'M-1' and
            Hotkeys_[f1CB3.get()] != 'M-2' and
            Hotkeys_[f1CB3.get()] != 'M-3'):
            if str(key).replace("'",'') == str(Hotkeys_[f1CB3.get()]):
                start_press()
                save_key = None
    if not Is_Edit_:
        a = False
        for i in sR_dict.values():
            if i[1] and (str(i[3]) == str(key).replace("'",'')):
                i[1] = False
                a = True
        if not a:
            for i,item in enumerate(__set__.values()):
                if item[2]:
                    if str(item[3]) == str(key).replace("'",''):
                        sR_dict[Rnum] = []
                        sR_dict[Rnum].append(item[1])
                        try:
                            if item[4][0][0] == '0':
                                sR_dict[Rnum].append(True)
                            else:
                                sR_dict[Rnum].append(False)
                        except:
                            sR_dict[Rnum].append(False)
                        t = td.Thread(target=ParsingScripts,args=(Rnum,item[4]))
                        sR_dict[Rnum].append(t)
                        sR_dict[Rnum][2].daemon = True
                        OL('[-] 脚本 '+str(item[1])+' 开始运行，编号：'+str(Rnum),_color='brown')
                        sR_dict[Rnum][2].start()
                        sR_dict[Rnum].append(item[3])
                        Rnum += 1
    
def RUN_1():
    with kb.Listener(on_press=key_on_press,on_release=key_on_release) as listener1:
        listener1.join()

Hotkeys1 = td.Thread(target=RUN_1)
Hotkeys1.start()

def mouse_on_click(x, y, button, pressed):
    global allow_click,__set__,sR_dict,Rnum,Is_Edit_
    if not int(f1CB3switch_Var.get()):
        if not pressed:
            if allow_click:
                if ((Hotkeys_[f1CB3.get()] == 'M-1' and str(button) == 'Button.left') or 
                    (Hotkeys_[f1CB3.get()] == 'M-2' and str(button) == 'Button.right') or 
                    (Hotkeys_[f1CB3.get()] == 'M-3' and str(button) == 'Button.middle')):
                    start_press()
    else:
        if allow_click:
            if ((Hotkeys_[f1CB3.get()] == 'M-1' and str(button) == 'Button.left') or 
                (Hotkeys_[f1CB3.get()] == 'M-2' and str(button) == 'Button.right') or 
                (Hotkeys_[f1CB3.get()] == 'M-3' and str(button) == 'Button.middle')):
                start_press()
    if not pressed:
        if not Is_Edit_:
            a = False
            for i in sR_dict.values():
                if i[1] and ((i[3] == 'M-1' and str(button) == 'Button.left') or
                             (i[3] == 'M-2' and str(button) == 'Button.right') or 
                             (i[3] == 'M-3' and str(button) == 'Button.middle')):
                    i[1] = False
                    a = True
            if not a:  
                for i,item in enumerate(__set__.values()):
                    if item[2]:
                        if ((item[3] == 'M-1' and str(button) == 'Button.left') or
                            (item[3] == 'M-2' and str(button) == 'Button.right') or 
                            (item[3] == 'M-3' and str(button) == 'Button.middle')):
                            sR_dict[Rnum] = []
                            sR_dict[Rnum].append(item[1])
                            try:
                                if item[4][0][0] == '0':
                                    sR_dict[Rnum].append(True)
                                else:
                                    sR_dict[Rnum].append(False)
                            except:
                                sR_dict[Rnum].append(False)
                            t = td.Thread(target=ParsingScripts,args=(Rnum,item[4]))
                            sR_dict[Rnum].append(t)
                            sR_dict[Rnum][2].daemon = True
                            OL('[-] 脚本 '+str(item[1])+' 开始运行，编号：'+str(Rnum),_color='brown')
                            sR_dict[Rnum][2].start()
                            Rnum += 1
    
def RUN_2():
    while not stop:
        with mo.Listener(on_click=mouse_on_click) as listener2:
            listener2.join()
        time.sleep(0.001)
        
Hotkeys2 = td.Thread(target=RUN_2)
Hotkeys2.start()

# 连点

def __press__():
    while not stop:
        if Click_sec != 'extreme':
            while RUN_Press:
                if ALL_Press[f1CB1.get()] == "M-1":
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
                elif ALL_Press[f1CB1.get()] == "M-2":
                    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0)
                    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0)
                elif ALL_Press[f1CB1.get()] == "M-3":
                    win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEDOWN, 0, 0)
                    win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEUP, 0, 0)
                else:
                    keyboard.press(ALL_Press[f1CB1.get()])
                    keyboard.release(ALL_Press[f1CB1.get()])
                __sleep(Click_sec)
            time.sleep(0.001)
        else:
            time.sleep(0.001)

_press_ = td.Thread(target=__press__)
_press_.start()

# 极致连点

def __extreme_click__():
    k = kb.Controller()
    while not stop:
        if Click_sec == 'extreme':
            while RUN_Press:
                if ALL_Press[f1CB1.get()] == "M-1":
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
                elif ALL_Press[f1CB1.get()] == "M-2":
                    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0)
                    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0)
                elif ALL_Press[f1CB1.get()] == "M-3":
                    win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEDOWN, 0, 0)
                    win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEUP, 0, 0)
                else:
                    k.press(ALL_Press[f1CB1.get()])
                    k.release(ALL_Press[f1CB1.get()])
                pass
            time.sleep(0.001)
        else:
            time.sleep(0.001)
            
_extreme_click_ = td.Thread(target=__extreme_click__)
_extreme_click_.start()

# 窗口样式
bg_fill1 = tk.Canvas(root,highlightthickness=0,width=10,height=4)
bg_fill1.place(x=0,y=30)

bg_fill2 = tk.Canvas(root,highlightthickness=0,width=10,height=4)
bg_fill2.place(x=440,y=30)

bg_fill1.config(bg="#E7E7E7")
bg_fill2.config(bg="#E7E7E7")

close.lift()
menu.lift()
small.lift()

# 窗口运行

sv_ttk.set_theme(ld)
light_dark(mode=1)
light_dark(mode=1)

GWL_EXSTYLE = -20
WS_EX_APPWINDOW = 0x00040000
WS_EX_TOOLWINDOW = 0x00000080
def set_appwindow(root):
    hwnd = windll.user32.GetParent(root.winfo_id())
    style = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
    style = style & ~WS_EX_TOOLWINDOW
    style = style | WS_EX_APPWINDOW
    res = windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)
    root.wm_withdraw()
    root.after(10, lambda: root.wm_deiconify())

root.protocol("WM_DELETE_WINDOW", on_closing)

set_sec_td = td.Thread(target=set_sec)
set_sec_td.daemon = True
set_sec_td.start()

f1Sc1_get_show_td = td.Thread(target=f1Sc1_get_show)
f1Sc1_get_show_td.start()


if call_print == 0:
    OL("[F]已成功加载脚本储存文件.",
    '#1E90FF')
elif call_print == 1:
    OL("[F]未发现脚本储存文件或脚本储存文件错误.\n[F]已重置脚本储存文件.",
    '#1E90FF')

OL(f'''运行成功！
打开时间：{time.time() - start_time} s\n''',lposition1='1.0')
OL('''欢迎使用KAMC-键鼠控制器！
当前版本：v1.3.0
认准正版，杜绝抄袭！
===================================''',lposition1='1.0')


root.wm_title("KAMC 键鼠控制器")
icon = ImageTk.PhotoImage(Image.open("KAMC_icon.ico"))
root.wm_iconphoto(True, icon)
root.overrideredirect(True)
root.after(10, lambda: set_appwindow(root=root))
root.update()
root.mainloop()
