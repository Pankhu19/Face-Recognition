from tkinter import *
from tkinter import ttk
from PIL import Image,ImageTk
from tkinter import messagebox
import mysql.connector
from config import passw

class pinwindow:
    def __init__(self,root,mob_no):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")
        self.var_pass = StringVar()
        
        limg = Image.open(r"Photos\landing background.jpg")
        limg = limg.resize((1530,790),Image.ANTIALIAS)
        self.photolimg = ImageTk.PhotoImage(limg)

        lbg_img = Label(self.root,image = self.photolimg)
        lbg_img.place(x=0,y=0,width=1400,height=790)
        
        main_frame = Frame(lbg_img,bd=2)
        main_frame.place(x=450,y=280,width = 520,height=100)

        password_label = Label(main_frame,text="Enter pin:",font=("Cascadia Code",14,"italic","bold"))
        password_label.grid(row=2,column=0,padx=10,pady=5, sticky=W)
        password_entry = ttk.Entry(main_frame,textvariable=self.var_pass ,width =28,font=("Cascadia Code",14,"bold"))
        password_entry.grid(row=2,column=1,padx=10,pady=5, sticky=W)

        img_verify = Image.open(r"Photos\verify.jpg")
        img_verify = img_verify.resize((150,80),Image.ANTIALIAS)
        self.photoimg_verify = ImageTk.PhotoImage(img_verify)

        b3 = Button(lbg_img,image = self.photoimg_verify,command =lambda: self.verifydata(mob_no),cursor="hand2")
        b3.place(x=630,y=330,width = 150, height = 50)

    def verifydata(self,mob_no):
        password = self.var_pass.get()
        if password=="":
                messagebox.showerror("Error","Pin is required",parent = self.root)
           
        else:
            conn = mysql.connector.connect(host = "localhost",username = "root", password=passw,database = "face_recognition")
            my_cursor = conn.cursor()
            my_cursor.execute("select pass from user where mobile_no=%s",(mob_no,))
            n = my_cursor.fetchone()
            n = "+".join(n)
            # conn.close()
            if n==password:
                messagebox.showinfo("Success","Transaction Completed")     
            else:
                 messagebox.showerror("Error","Wrong pin", parent = self.root)

if __name__=='__main__':
    root = Tk()
    obj = pinwindow(root,mob_no)
    root.mainloop()