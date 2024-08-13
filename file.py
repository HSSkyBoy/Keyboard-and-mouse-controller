import base64
import pynput.keyboard as kb
import os
def decrypt(name):
    s=''
    with open(name, 'r', encoding='UTF-8') as f:
        s="".join(f.readlines()).encode('utf-8')
        src=s
    while True:
        try:
            src=s
            s=base64.b16decode(s)
            str(s,'utf-8')
            continue
        except:
            pass
        try:
            src=s
            s=base64.b32decode(s)
            str(s,'utf-8')
            continue
        except:
            pass
        try:
            src=s
            s=base64.b64decode(s)
            str(s,'utf-8')
            continue
        except:
            pass
        break
    s2 = src.decode('utf-8')
    return s2
def Readfile(path):
    with open(path,'r') as f:
        return f.read()
def Writefile(path,text):
    with open(path,'w') as f:
        f.write(text)
def BinaryReadFile(path):
    with open(path,'rb') as f:
        return f.read()
def BinaryWriteFile(path,text):
    with open(path,'wb') as f:
        f.write(text)
def Deletefile(path):
    if os.path.exists(path):
        try:
            os.remove(path)
            return True
        except Exception as e:
            return (False,e)
    else:
        return None
#以下是对于KAMC的字典
ALL_Press = {'鼠标左键 - Left_Mouse' : 'M-1',                       # 键鼠对应关键字 字典
             '鼠标右键 - Right_Mouse' : 'M-2',
             '鼠标中键 - Middle_Mouse' : 'M-3',
             '上 - Up' : kb.Key.up,
             '下 - Down' : kb.Key.down,
             '左 - Left' : kb.Key.left,
             '右 - Right' : kb.Key.right,
             '空格 - Space' : kb.Key.space,
             '退格 - Backspace' : kb.Key.backspace,
             '切换 - Shift' : kb.Key.shift,
             '回车 - Enter' : kb.Key.enter,
             '制表 - Tab' : kb.Key.tab,
             '1' : '1',
             '2' : '2',
             '3' : '3',
             '4' : '4',
             '5' : '5',
             '6' : '6',
             '7' : '7',
             '8' : '8',
             '9' : '9',
             '0' : '0',
             'A' : 'a',
             'B' : 'b',
             'C' : 'c',
             'D' : 'd',
             'E' : 'e',
             'F' : 'f',
             'G' : 'g',
             'H' : 'h',
             'I' : 'i',
             'J' : 'j',
             'K' : 'k',
             'L' : 'l',
             'M' : 'm',
             'N' : 'n',
             'O' : 'o',
             'P' : 'p',
             'Q' : 'q',
             'R' : 'r',
             'S' : 's',
             'T' : 't',
             'U' : 'u',
             'V' : 'v',
             'W' : 'w',
             'X' : 'x',
             'Y' : 'y',
             'Z' : 'z',
             'F1' : kb.Key.f1,
             'F2' : kb.Key.f2,
             'F3' : kb.Key.f3,
             'F4' : kb.Key.f4,
             'F5' : kb.Key.f5,
             'F6' : kb.Key.f6,
             'F7' : kb.Key.f7,
             'F8' : kb.Key.f8,
             'F9' : kb.Key.f9,
             'F10' : kb.Key.f10,
             'F11' : kb.Key.f11,
             'F12' : kb.Key.f12
             }
Mouse_Press = {'鼠标左键 - Left_Mouse' : 'M-1',                       # 键鼠对应关键字 字典
               '鼠标右键 - Right_Mouse' : 'M-2',
               '鼠标中键 - Middle_Mouse' : 'M-3'
               }
Key_Press = {'上 - Up' : kb.Key.up,
             '下 - Down' : kb.Key.down,
             '左 - Left' : kb.Key.left,
             '右 - Right' : kb.Key.right,
             '空格 - Space' : kb.Key.space,
             '退格 - Backspace' : kb.Key.backspace,
             '切换 - Shift' : kb.Key.shift,
             '回车 - Enter' : kb.Key.enter,
             '制表 - Tab' : kb.Key.tab,
             '1' : '1',
             '2' : '2',
             '3' : '3',
             '4' : '4',
             '5' : '5',
             '6' : '6',
             '7' : '7',
             '8' : '8',
             '9' : '9',
             '0' : '0',
             'A' : 'a',
             'B' : 'b',
             'C' : 'c',
             'D' : 'd',
             'E' : 'e',
             'F' : 'f',
             'G' : 'g',
             'H' : 'h',
             'I' : 'i',
             'J' : 'j',
             'K' : 'k',
             'L' : 'l',
             'M' : 'm',
             'N' : 'n',
             'O' : 'o',
             'P' : 'p',
             'Q' : 'q',
             'R' : 'r',
             'S' : 's',
             'T' : 't',
             'U' : 'u',
             'V' : 'v',
             'W' : 'w',
             'X' : 'x',
             'Y' : 'y',
             'Z' : 'z',
             'F1' : kb.Key.f1,
             'F2' : kb.Key.f2,
             'F3' : kb.Key.f3,
             'F4' : kb.Key.f4,
             'F5' : kb.Key.f5,
             'F6' : kb.Key.f6,
             'F7' : kb.Key.f7,
             'F8' : kb.Key.f8,
             'F9' : kb.Key.f9,
             'F10' : kb.Key.f10,
             'F11' : kb.Key.f11,
             'F12' : kb.Key.f12
             }