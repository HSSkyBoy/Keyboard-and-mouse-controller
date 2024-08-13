import tkinter as tk
class MenuPlus(object):
    def __init__(self,root,width=100,bg="#E7E7E7",fg='#000000',sidecolor='#DCDCDC'):
        self.root = root
        self.w = width
        self.sidecolor = sidecolor
        self.num1 = False
        
        if sidecolor != 'noside':
            self.MPside = tk.Frame(self.root,width=(self.w + 2),bg=sidecolor)
            self.MP = tk.Frame(self.MPside,bg=bg,width=self.w)
            self.MP.pack(padx=1,pady=1)
        else:
            self.MP = tk.Frame(self.root,bg=bg,width=self.w)
        self.All_MenuButton = []

    def add(self,text='',bg="#E7E7E7",fg='#000000',activebackground="#FAFAFA",activeforeground="#000000",command=None):
        self.mb = tk.Button(self.MP,
                            text=text,
                            bd=0, 
                            command=command,
                            width=self.w,
                            height=1,
                            bg=bg,
                            fg=fg,
                            activebackground=activebackground,
                            activeforeground=activeforeground)
        self.mb.pack()
        self.mb.bind('<Button-1>',lambda event:self.MP.focus_set())
        self.mb.bind('<Button-2>',lambda event:self.MP.focus_set())
        self.mb.bind('<Button-3>',lambda event:self.MP.focus_set())
        
        self.All_MenuButton.append(self.mb)
        
    def place(self,x=0,y=0):
        if self.sidecolor != 'noside':
            self.MPside.place(x=x,y=y,width=self.w)
        else:
            self.MP.place(x=x,y=y,width=self.w)
    
    def pack(self):
        if self.sidecolor != 'noside':
            self.MPside.pack()
        else:
            self.MP.pack
    
    def lift(self):
        if self.sidecolor != 'noside':
            self.MPside.lift()
        else:
            self.MP.lift()
    
    def lower(self):
        if self.sidecolor != 'noside':
            self.MPside.lower()
        else:
            self.MP.lower()
    
    def config(self,sidecolor=''):
        if sidecolor != '':
            if self.sidecolor != 'noside':
                self.MPside.config(bg=sidecolor)
    
    def button_config(self,index=0,text='',bg='',fg='',activebackground='',activeforeground='',command=None):
        if text != '':
            self.All_MenuButton[index].config(text=text)
        if bg != '':
            self.All_MenuButton[index].config(bg=bg)
        if fg != '':
            self.All_MenuButton[index].config(fg=fg)
        if activebackground != '':
            self.All_MenuButton[index].config(activebackground=activebackground)
        if activeforeground != '':
            self.All_MenuButton[index].config(activeforeground=activeforeground)
        if command != None:
            self.All_MenuButton[index].config(command=command)
    
    def button_config_all(self,text='',bg='',fg='',activebackground='',activeforeground='',command=None):
        for i in self.All_MenuButton:
            if text != '':
                i.config(text=text)
            if bg != '':
                i.config(bg=bg)
            if fg != '':
                i.config(fg=fg)
            if activebackground != '':
                i.config(activebackground=activebackground)
            if activeforeground != '':
                i.config(activeforeground=activeforeground)
            if command != None:
                i.config(command=command)
    
    def bind(self,key,func):
        self.MP.bind(key,func)
        
    def bind_all(self,key,func):
        self.MP.bind_all(key,func)