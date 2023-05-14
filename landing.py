from tkinter import *
from tkinter import ttk
from PIL import Image,ImageTk
from transaction import send_money
from Information import info
from history import History

class landing:
    def __init__(self,root,mob_no):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")


        limg = Image.open(r"Photos\landing background.jpg")
        limg = limg.resize((1530,790),Image.ANTIALIAS)
        self.photolimg = ImageTk.PhotoImage(limg)

        lbg_img = Label(self.root,image = self.photolimg)
        lbg_img.place(x=0,y=0,width=1400,height=790)

        acc_info_btn = Button(lbg_img, text="Account Information",command=lambda: self.accinfo(mob_no) ,font=("Imprint MT Shadow",20,"bold"),bg = "purple",fg="white",cursor = "hand2")
        acc_info_btn.place(x=200,y=255,width = 320, height = 92)

        balance_btn = Button(lbg_img, text="Transaction History",command=lambda: self.thistory(mob_no),font=("Imprint MT Shadow",20,"bold"),bg = "purple",fg="white",cursor = "hand2")
        balance_btn.place(x=800,y=255,width = 320, height = 92)

        trans_btn = Button(lbg_img, text="Send Money",command=lambda: self.money(mob_no), font=("Imprint MT Shadow",20,"bold"),bg = "purple",fg="white",cursor = "hand2")
        trans_btn.place(x=500,y=425,width = 320, height = 92)

    def money(self,mob_no):
        self.mob_no = mob_no
        self.new_window=Toplevel(self.root)
        self.app = send_money(self.new_window,self.mob_no)

    def accinfo(self,mob_no):
        self.new_window=Toplevel(self.root)
        self.app = info(self.new_window,mob_no)

    def thistory(self,mob_no):
        self.new_window=Toplevel(self.root)
        self.app = History(self.new_window,mob_no)


if __name__=='__main__':
    root = Tk()
    obj = landing(root,mob_no)
    root.mainloop()
    