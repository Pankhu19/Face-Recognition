from tkinter import *
from tkinter import ttk
from PIL import Image,ImageTk
import mysql.connector
# from login import login
from config import passw

class info:
    def __init__(self,root,mob_no):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")

        limg = Image.open(r"Photos\landing background.jpg")
        limg = limg.resize((1530, 790), Image.ANTIALIAS)
        self.photolimg = ImageTk.PhotoImage(limg)

        lbg_img = Label(self.root, image=self.photolimg)
        lbg_img.place(x=0, y=0, width=1400, height=790)

        main_frame = Frame(lbg_img, bd=2, bg="light blue")
        main_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        conn = mysql.connector.connect(host="localhost", username="root", password=passw, database="face_recognition")
        my_cursor = conn.cursor()
        my_cursor.execute("SELECT first_name, last_name, user.acc_no, mobile_no, email_id, balance FROM user, account WHERE mobile_no=%s and user.acc_no = account.account_number", (mob_no,))
        result = my_cursor.fetchone()

        first_name = result[0]
        last_name = result[1]
        acc_no = result[2]
        mobile_no = result[3]
        email_id = result[4]
        balance = result[5]

        label_first_name = Label(main_frame, text="First Name: " + first_name, font=("Arial", 16), bg="light blue", fg="black")
        label_first_name.pack(fill=X, padx=10, pady=10)

        label_last_name = Label(main_frame, text="Last Name: " + last_name, font=("Arial", 16), bg="light blue", fg="black")
        label_last_name.pack(fill=X, padx=10, pady=10)

        label_acc_no = Label(main_frame, text="Account Number: " + acc_no, font=("Arial", 16), bg="light blue", fg="black")
        label_acc_no.pack(fill=X, padx=10, pady=10)

        label_mobile_no = Label(main_frame, text="Mobile Number: " + str(mobile_no), font=("Arial", 16), bg="light blue", fg="black")
        label_mobile_no.pack(fill=X, padx=10, pady=10)

        label_email_id = Label(main_frame, text="Email ID: " + email_id, font=("Arial", 16), bg="light blue", fg="black")
        label_email_id.pack(fill=X, padx=10, pady=10)

        label_balance = Label(main_frame, text="Balance: " + str(balance), font=("Arial", 16), bg="light blue", fg="black")
        label_balance.pack(fill=X, padx=10, pady=10)

        conn.close()


    
if __name__=='__main__':
    root = Tk()
    obj = info(root,mob_no)
    root.mainloop()