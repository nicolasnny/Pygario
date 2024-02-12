from tkinter import *
import tkinter.font as font
from ursina import Keys

class Bind:
    def __init__(self) -> None:
        self.word=None
        self.root=Tk()
        self.root.config(bg="#808080")
        self.root.bind("<a>",self.funcA )
        self.root.bind("<z>",self.funcZ) 
        self.root.bind("<e>",self.funcE) 
        self.root.bind("<r>",self.funcR) 
        self.root.bind("<t>",self.funcT ) 
        self.root.bind("<y>",self.funcY )
        self.root.bind("<u>",self.funcU )
        self.root.bind("<i>",self.funcI) 
        self.root.bind("<o>",self.funcO) 
        self.root.bind("<p>",self.funcP) 
        self.root.bind("<q>",self.funcQ ) 
        self.root.bind("<s>",self.funcS )
        self.root.bind("<d>",self.funcD )
        self.root.bind("<f>",self.funcF) 
        self.root.bind("<g>",self.funcG) 
        self.root.bind("<h>",self.funcH) 
        self.root.bind("<j>",self.funcJ ) 
        self.root.bind("<k>",self.funcK )
        self.root.bind("<space>",self.funcSpace )
        self.root.bind("<Shift_L>",self.funcLshift )
        self.root.bind("<Control_L>",self.funcLctrl )
        self.root.bind("<Down>",self.funcDown )
        self.root.bind("<Up>",self.funcUp )
        self.root.bind("<Left>",self.funcLeft )
        self.root.bind("<Right>",self.funcRight )
        self.root.bind("<Alt_L>",self.funcReturn )
        btn=Button(self.root,text="Click on the button when you have pressed a key",bg="#808080",command=self.root.destroy)
        btn.pack()
        self.root.mainloop()

    
    
    def funcA(self,event):
        self.word="a"

    def funcZ(self,event):
        self.word="z"

    def funcE(self,event):
        self.word="e"

    def funcR(self,event):
        self.word="r"

    def funcT(self,event):
        self.word="t"

    def funcY(self,event):
        self.word="y"

    def funcU(self,event):
        self.word="u"

    def funcI(self,event):
        self.word="i"

    def funcO(self,event):
        self.word="o"

    def funcP(self,event):
        self.word="p"

    def funcQ(self,event):
        self.word="q"

    def funcS(self,event):
        self.word="s"

    def funcD(self,event):
        self.word="d"

    def funcF(self,event):
        self.word="f"

    def funcG(self,event):
        self.word="g"

    def funcH(self,event):
        self.word="h"

    def funcJ(self,event):
        self.word="j"

    def funcK(self,event):
        self.word="k"

    def funcL(self,event):
        self.word="l"

    def funcM(self,event):
        self.word="m"

    def funcW(self,event):
        self.word="w"

    def funcX(self,event):
        self.word="x"

    def funcC(self,event):
        self.word="c"

    def funcV(self,event):
        self.word="v"

    def funcB(self,event):
        self.word="b"

    def funcN(self,event):
        self.word="n"

    def funcSpace(self,event):
        self.word="space"
    
    def funcReturn(self,event):
        self.word="return"

    def funcLshift(self,event):
        self.word=Keys.left_shift

    def funcLctrl(self,event):
        self.word=Keys.left_control
    
    def funcUp(self,event):
        self.word=Keys.up_arrow
    
    def funcDown(self,event):
        self.word=Keys.down_arrow

    def funcLeft(self,event):
        self.word=Keys.left_arrow

    def funcRight(self,event):
        self.word=Keys.right_arrow


class ForceDelete:
    def __init__(self,func1,func2,arg1,arg2) -> None:
        self.root=Tk()
        Button(self.root,text="Confirmer le changement",command=lambda:func1(arg1,arg2)).pack()
        Button(self.root,text="Annuler le changement",command=lambda:func2()).pack()
        self.root.mainloop()

    def kill(self):
        self.root.destroy()


    
    


if __name__=="__main__":
    pass