
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import mysql.connector
from config import passw
class History:
    def __init__(self, root,mob_no):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")

        limg = Image.open(r"Photos\landing background.jpg")
        limg = limg.resize((1530, 790), Image.ANTIALIAS)
        self.photolimg = ImageTk.PhotoImage(limg)

        lbg_img = Label(self.root, image=self.photolimg)
        lbg_img.place(x=0, y=0, width=1530, height=790)  # Adjust the width and height

        main_frame = Frame(lbg_img, bd=2)
        main_frame.place(x=30, y=200, width=1300)  # Adjust the width
        main_frame.grid_rowconfigure(0, weight=1)  

        # Styling for Treeview
        style = ttk.Style()
        style.configure("Treeview",
                        background="#D3D3D3",
                        foreground="black",
                        rowheight=25,
                        fieldbackground="#D3D3D3",
                        font=("Cascadia Code", 14))  # Increase font size here
        
        style.configure("Treeview.Heading",
                        background="purple",
                        foreground="black",
                        font=("Cascadia Code", 14, "italic", "bold")
                        )
                        # relief = "flat")
        style.map("Treeview",
                  background=[("selected", "purple")])

        treeview = ttk.Treeview(main_frame, style="Treeview")
        treeview["columns"] = ("recep_name", "recep_acc_no", "transaction_type", "amount", "transaction_date")
        treeview.column("#0", width=0, stretch=NO)  # Hide the first empty column
        treeview.column("recep_name", width=150, anchor=CENTER)
        treeview.column("recep_acc_no", width=150, anchor=CENTER)
        treeview.column("transaction_type", width=100, anchor=CENTER)
        treeview.column("amount", width=100, anchor=CENTER)
        treeview.column("transaction_date", width=150, anchor=CENTER)

        treeview.heading("recep_name", text="Recipient Name", anchor=CENTER)  # No font option
        treeview.heading("recep_acc_no", text="Recipient Account No", anchor=CENTER)  # No font option
        treeview.heading("transaction_type", text="Transaction Type", anchor=CENTER)  # No font option
        treeview.heading("amount", text="Amount", anchor=CENTER)  # No font option
        treeview.heading("transaction_date", text="Date and Time", anchor=CENTER)  # No font option

        # treeview.tag_configure("heading", font=("Cascadia Code", 14, "italic", "bold"))  # Increase font size here
        treeview.tag_configure("column", font=("Cascadia Code", 14))

        
        scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=treeview.yview)
        scrollbar.pack(side=RIGHT, fill=Y)

        treeview.configure(yscrollcommand=scrollbar.set)
        treeview.pack(fill=BOTH, expand=YES)

        # Retrieve transactions from the database
        conn = mysql.connector.connect(host="localhost", username="root", password=passw, database="face_recognition")
        my_cursor = conn.cursor()
        my_cursor.execute("SELECT recep_name, recep_acc_no, transaction_type, amount, transaction_date FROM transaction WHERE account_id = (SELECT id FROM account WHERE account_number = (SELECT acc_no FROM user WHERE mobile_no = %s))", (mob_no,))
        transactions = my_cursor.fetchall()

        # Insert transactions into the Treeview
        for transaction in transactions:
            treeview.insert("", "end", values=transaction)

        conn.close()

if __name__ == '__main__':
    root = Tk()
    obj = History(root,mob_no)
    root.mainloop()
