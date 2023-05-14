from tkinter import *
from tkinter import ttk
from PIL import Image,ImageTk
from otp import otp
from tkinter import messagebox
import mysql.connector
import cv2
import os
import numpy as np
from config import passw

class signup:
    def __init__(self,root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")

        # variables
        self.var_fname = StringVar()
        self.var_lname = StringVar()
        self.var_acc = StringVar()
        self.var_mobile = StringVar()
        self.var_email = StringVar()
        self.var_pass = StringVar()

        limg = Image.open(r"Photos\limg1.jpg")
        limg = limg.resize((1530,790),Image.ANTIALIAS)
        self.photolimg = ImageTk.PhotoImage(limg)

        lbg_img = Label(self.root,image = self.photolimg)
        lbg_img.place(x=0,y=0,width=1400,height=790)

        title_lbll=Label(lbg_img,text="Sign Up", font=("Imprint MT Shadow",45,"bold"),fg="black", anchor="center")
        title_lbll.place(relx=0.5, rely=0.15, anchor="center")

        main_frame = Frame(lbg_img,bd=2)
        main_frame.place(x=450,y=200,width = 550,height=350)

        name_label = Label(main_frame,text="First name:",font=("Cascadia Code",14,"italic","bold"))
        name_label.grid(row=0,column=0,padx=10,pady=5, sticky=W)
        name_entry = ttk.Entry(main_frame,textvariable=self.var_fname ,width =28,font=("Cascadia Code",14,"bold"))
        name_entry.grid(row=0,column=1,padx=10,pady=5, sticky=W)

        lname_label = Label(main_frame,text="Last name:",font=("Cascadia Code",14,"italic","bold"))
        lname_label.grid(row=1,column=0,padx=10,pady=5, sticky=W)
        lname_entry = ttk.Entry(main_frame,textvariable=self.var_lname, width =28,font=("Cascadia Code",14,"bold"))
        lname_entry.grid(row=1,column=1,padx=10,pady=5, sticky=W)

        acc_label = Label(main_frame,text="Account no:",font=("Cascadia Code",14,"italic","bold"))
        acc_label.grid(row=2,column=0,padx=10,pady=5, sticky=W)
        acc_entry = ttk.Entry(main_frame,textvariable=self.var_acc, width =28,font=("Cascadia Code",14,"bold"))
        acc_entry.grid(row=2,column=1,padx=10,pady=5, sticky=W)

        mobile_label = Label(main_frame,text="Mobile no:",font=("Cascadia Code",14,"italic","bold"))
        mobile_label.grid(row=3,column=0,padx=10,pady=5, sticky=W)
        mobile_entry = ttk.Entry(main_frame,textvariable=self.var_mobile ,width =28,font=("Cascadia Code",14,"bold"))
        mobile_entry.grid(row=3,column=1,padx=10,pady=5, sticky=W)

        email_label = Label(main_frame,text="Email id:",font=("Cascadia Code",14,"italic","bold"))
        email_label.grid(row=4,column=0,padx=10,pady=5, sticky=W)
        email_entry = ttk.Entry(main_frame,textvariable=self.var_email ,width =28,font=("Cascadia Code",14,"bold"))
        email_entry.grid(row=4,column=1,padx=10,pady=5, sticky=W)

        password_label = Label(main_frame,text="Create password:",font=("Cascadia Code",14,"italic","bold"))
        password_label.grid(row=5,column=0,padx=10,pady=5, sticky=W)
        password_entry = ttk.Entry(main_frame,textvariable=self.var_pass ,width =28,font=("Cascadia Code",14,"bold"))
        password_entry.grid(row=5,column=1,padx=10,pady=5, sticky=W)

        img_verify = Image.open(r"Photos\verify.jpg")
        img_verify = img_verify.resize((150,80),Image.ANTIALIAS)
        self.photoimg_verify = ImageTk.PhotoImage(img_verify)

        b3 = Button(lbg_img,image = self.photoimg_verify,command = self.add_data ,cursor="hand2")
        b3.place(x=650,y=450,width = 150, height = 50)

    def otp_conn(self,mob_no):
        self.new_window=Toplevel(self.root)
        self.app = otp(self.new_window,mob_no)

    def add_data(self):
        if self.var_fname.get()=="" or self.var_mobile.get() =="" or self.var_acc.get() =="" or self.var_email.get() =="":
            messagebox.showerror("Error","All fields are required",parent = self.root)
        else:
            try:
                conn = mysql.connector.connect(host = "localhost",username = "root", password=passw,database = "face_recognition")
                my_cursor = conn.cursor()
                mob_no = self.var_mobile.get()
                acc_no = self.var_acc.get()
                my_cursor.execute("INSERT INTO user VALUES(%s, %s, %s, %s, %s, %s)", (self.var_fname.get(), self.var_lname.get(), acc_no, mob_no, self.var_email.get(), self.var_pass.get()))
                my_cursor.execute("INSERT INTO account(account_number,balance) VALUES(%s, %s)", (acc_no, 3000))
                conn.commit()
                conn.close()
                messagebox.showinfo("","Going for Image Capture",parent = self.root)                
                self.image_capture(acc_no)
                self.otp_conn(mob_no)
            except Exception as es:
                messagebox.showerror("Error",f"Due to: {str(es)}",parent = self.root)
        
    def image_capture(self,acc_no):
        try:
            face_classifier=cv2.CascadeClassifier("haarcascade_frontalface_default.xml")   
            cap = cv2.VideoCapture(0)
            img_counter =0
            while True:
                ret,frame = cap.read()
                col = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
                faces = face_classifier.detectMultiScale(
                    col,
                    scaleFactor = 1.1,
                    minNeighbors = 5,
                    minSize=(30,30),
                    flags=cv2.CASCADE_SCALE_IMAGE
                )
                img_counter +=1
                for(x,y,w,h) in faces:
                    cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),2)
                    cv2.putText(frame,str(img_counter),(50,50),cv2.FONT_HERSHEY_COMPLEX,2,(0,255,0),2)
                    file_name_path = "data_images_signup/user."+str(acc_no)+"."+str(img_counter)+".jpg"
                    if y + h <= frame.shape[0] and x + w <= frame.shape[1]:
                        col = col[y:y+h, x:x+w]
                        col = cv2.resize(col, (450, 450))
                        cv2.imwrite(file_name_path, col)
                cv2.imshow("Capturing Image",frame)
                if cv2.waitKey(1)==13 or int(img_counter)==100:
                    break
            cap.release()
            cv2.destroyAllWindows()
            messagebox.showinfo("Result","Generating data sets completed",parent = self.root)
        except Exception as es:
            messagebox.showerror("Error",f"Due to: {str(es)}",parent = self.root)


if __name__=='__main__':
    root = Tk()
    obj = signup(root)
    root.mainloop()
    
