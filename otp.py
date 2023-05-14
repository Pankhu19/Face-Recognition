from tkinter import *
from tkinter import ttk
from PIL import ImageTk
import PIL.Image
from landing import landing
import random
from twilio.rest import Client
# from signup import signup
from tkinter import messagebox
import os
import cv2
import numpy as np
from config import auth_token,account_sid,to_phone_number,from_phone_number
class otp:
    def __init__(self,root,mob_no):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")
        self.n = random.randint(1000,9999)
        self.client = Client(account_sid,auth_token)
        self.client.messages.create(to = to_phone_number, from_ = from_phone_number,body = self.n)

        self.var_otp = StringVar()

        limg = PIL.Image.open(r"Photos\limg1.jpg")
        limg = limg.resize((1530,790),PIL.Image.ANTIALIAS)
        self.photolimg = ImageTk.PhotoImage(limg)

        lbg_img = Label(self.root,image = self.photolimg)
        lbg_img.place(x=0,y=0,width=1400,height=790)

        title_lbll=Label(lbg_img,text="Otp Verification", font=("Imprint MT Shadow",45,"bold"),fg="black", anchor="center")
        title_lbll.place(relx=0.5, rely=0.2, anchor="center")

        main_frame = Frame(lbg_img,bd=2)
        main_frame.place(x=450,y=300,width = 450,height=200)

        otp_label = Label(main_frame,text="Otp:",font=("Cascadia Code",14,"italic","bold"))
        otp_label.grid(row=1,column=0,padx=10,pady=10, sticky=W)
        otp_entry = ttk.Entry(main_frame,textvariable=self.var_otp,width =28,font=("Cascadia Code",14,"bold"))
        otp_entry.grid(row=1,column=1,padx=20,pady=10, sticky=W)

        img_verify = PIL.Image.open(r"Photos\verify.jpg")
        img_verify = img_verify.resize((150,80),PIL.Image.ANTIALIAS)
        self.photoimg_verify = ImageTk.PhotoImage(img_verify)

        b3 = Button(lbg_img,image = self.photoimg_verify,command = lambda: self.checkotp(mob_no) ,cursor="hand2")
        b3.place(x=605,y=370,width = 150, height = 50)

        img_resend = PIL.Image.open(r"Photos\resend.jpg")
        img_resend = img_resend.resize((150,80),PIL.Image.ANTIALIAS)
        self.photoimg_resend = ImageTk.PhotoImage(img_resend)

        b3 = Button(lbg_img,image = self.photoimg_resend,command =self.resendotp ,cursor="hand2")
        b3.place(x=605,y=440,width = 150, height = 50)

    def checkotp(self,mob_no):
        # try:
            otp_taken = self.var_otp.get()
            self.userInput = int(otp_taken)
            if self.userInput==self.n:
                messagebox.showinfo("Success","Login Success",parent = self.root)
                self.n="done"
                # self.train_classifier()
                self.landing_conn(mob_no)
            else:
                messagebox.showinfo("Wrong","Invalid Otp")
                # self.signup_conn()
        # except:
        #     messagebox.showinfo("Wrong","Invalid Otp")

    def resendotp(self):
        self.n=random.randint(1000,9999)
        self.client = Client("ACfa5cc11b0ae7370f71552e7dc11e33af","475634559a300e4083f22b4d1c744f87")
        self.client.messages.create(to = ["+917252896322"], from_ = "+15856288712",body = self.n)

        
    def landing_conn(self,mob_no):
        # self.mob_no = mob_no
        self.new_window=Toplevel(self.root)
        self.app = landing(self.new_window,mob_no)


if __name__=='__main__':
    root = Tk()
    obj = otp(root,mob_no)
    root.mainloop()