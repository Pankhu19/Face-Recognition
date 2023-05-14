from tkinter import *
from tkinter import ttk
from PIL import Image,ImageTk
from signup import signup
from login import login

class Face_Recognition_System:
    def __init__(self,root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")

        img = Image.open(r"Photos\limg1.jpg")
        img = img.resize((1530,790),Image.ANTIALIAS)
        self.photoimg = ImageTk.PhotoImage(img)

        bg_img = Label(self.root,image = self.photoimg)
        bg_img.place(x=0,y=0,width=1400,height=790)

        title_lbl=Label(bg_img,text="Online Transaction System", font=("Imprint MT Shadow",35,"bold"),fg="black", anchor="center")
        title_lbl.place(relx=0.5, rely=0.1, anchor="center")

        img_login = Image.open(r"Photos\login-removebg-preview.png")
        img_login = img_login.resize((320,92),Image.ANTIALIAS)
        self.photoimg_login = ImageTk.PhotoImage(img_login)

        b1 = Button(bg_img,image = self.photoimg_login, command = self.login_conn, cursor="hand2")
        b1.place(x=200,y=350,width = 320, height = 92)
        
        img_signup = Image.open(r"Photos\signup-removebg-preview (1).png")
        img_signup = img_signup.resize((320,92),Image.ANTIALIAS)
        self.photoimg_signup = ImageTk.PhotoImage(img_signup)

        b2 = Button(bg_img,image = self.photoimg_signup,command = self.signup_conn, cursor="hand2")
        b2.place(x=800,y=350,width = 320, height = 92)

    def signup_conn(self):
        self.new_window=Toplevel(self.root)
        self.app = signup(self.new_window)
    
    def login_conn(self):
        self.new_window=Toplevel(self.root)
        self.app = login(self.new_window)

if __name__=='__main__':
    root = Tk()
    obj = Face_Recognition_System(root)
    root.mainloop()
    