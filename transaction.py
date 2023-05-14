from tkinter import *
from tkinter import ttk
from PIL import Image,ImageTk
from tkinter import messagebox
import mysql.connector
import cv2
import os
import numpy as np
from pinwindow import pinwindow
import tensorflow as tf
import datetime
from decimal import Decimal
from config import passw

class send_money:
    def __init__(self,root,mob_no):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")

        self.var_name = StringVar()
        self.var_account = StringVar()
        self.var_amount = StringVar()
        
        limg = Image.open(r"Photos\landing background.jpg")
        limg = limg.resize((1530,790),Image.ANTIALIAS)
        self.photolimg = ImageTk.PhotoImage(limg)

        lbg_img = Label(self.root,image = self.photolimg)
        lbg_img.place(x=0,y=0,width=1400,height=790)

        main_frame = Frame(lbg_img,bd=2)
        main_frame.place(x=420,y=230,width = 550,height=200)

        recipient_label = Label(main_frame,text="Recipient name",font=("Cascadia Code",14,"italic","bold"))
        recipient_label.grid(row=0,column=0,padx=10,pady=5, sticky=W)
        recipient_entry = ttk.Entry(main_frame,textvariable=self.var_name, width =28,font=("Cascadia Code",14,"bold"))
        recipient_entry.grid(row=0,column=1,padx=10,pady=5, sticky=W)

        account_label = Label(main_frame,text="Account number",font=("Cascadia Code",14,"italic","bold"))
        account_label.grid(row=1,column=0,padx=10,pady=5, sticky=W)
        account_entry = ttk.Entry(main_frame,textvariable=self.var_account ,width =28,font=("Cascadia Code",14,"bold"))
        account_entry.grid(row=1,column=1,padx=10,pady=5, sticky=W)
        

        amount_label = Label(main_frame,text="Amount:",font=("Cascadia Code",14,"italic","bold"))
        amount_label.grid(row=2,column=0,padx=10,pady=5, sticky=W)
        amount_entry = ttk.Entry(main_frame,textvariable=self.var_amount, width =28,font=("Cascadia Code",14,"bold"))
        amount_entry.grid(row=2,column=1,padx=10,pady=5, sticky=W)

        send_button = Button(lbg_img, text="Send",command=lambda: self.add_data(mob_no),font=("Imprint MT Shadow",20,"bold"),bg = "purple",fg="white",cursor = "hand2")
        send_button.place(x=620,y=370,width = 150, height = 50)

    def add_data(self,mob_no):
            if self.var_name.get()=="" or self.var_account.get() =="" or self.var_amount.get() =="":
                messagebox.showerror("Error","All fields are required",parent = self.root)
            else:
                
                conn = mysql.connector.connect(host = "localhost",username = "root", password=passw,database = "face_recognition")
                my_cursor = conn.cursor()
                my_cursor.execute("select id,balance from account where account_number=(select acc_no from user where mobile_no = %s)",(mob_no,) )
                res= my_cursor.fetchone()
                n = res[0]
                bal = res[1]
                if Decimal(self.var_amount.get())>bal:
                    messagebox.showerror("Error","Current balance is low",parent = self.root)
                else:
                    if self.face_recog(mob_no):
                        transaction_date = datetime.datetime.now()
                        my_cursor.execute("INSERT INTO transaction(recep_name,recep_acc_no,account_id,transaction_type,amount,transaction_date) VALUES(%s, %s,%s,%s,%s,%s)", (self.var_name.get(),self.var_account.get(),n,"Online",self.var_amount.get(),transaction_date))
                        my_cursor.execute("Update account set balance = %s where id=%s",(bal-Decimal(self.var_amount.get()),n))
                        conn.commit()
                        conn.close()
                    else:
                        messagebox.showerror("Error","Try again",parent = self.root)
    def face_recog(self,mob_no):
        access_granted = False
        fake_count=0
        faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.read("classifier.xml")
        eye_model = cv2.CascadeClassifier('haarcascade_eye.xml')
        liveness_model = tf.keras.models.load_model('liveness.model')
        labels = {0: 'Real', 1: 'Fake'}
        
        conn = mysql.connector.connect(host="localhost", username="root", password=passw, database="face_recognition")
        my_cursor = conn.cursor()
        def compute_texture_variance(image):
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            dx = cv2.Sobel(gray, cv2.CV_64F, 1, 0)
            dy = cv2.Sobel(gray, cv2.CV_64F, 0, 1)
            texture = np.sqrt(dx * dx + dy * dy)
            return np.var(texture)
        def are_eyes_open(roi_gray):
            eyes = eye_model.detectMultiScale(roi_gray)
            for (ex, ey, ew, eh) in eyes:
                eye_roi = roi_gray[ey:ey + eh, ex:ex + ew]
                _, threshold = cv2.threshold(eye_roi, 63, 255, cv2.THRESH_BINARY)
                contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                for contour in contours:
                    area = cv2.contourArea(contour)
                    if area > 20:
                        return True
            return False
        def run_access_control():
            nonlocal access_granted
            nonlocal fake_count
            liveness_confidence = 0.0
            cap = cv2.VideoCapture(0)
            img_counter = 0
            while True:
                ret, frame = cap.read()
                img_counter+=1
                # if not ret:
                #     break
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
                
                for (x, y, w, h) in faces:
                    face_roi = frame[y:y + h, x:x + w]
                    roi_gray = gray[y:y + h, x:x + w]
                    face_resized = cv2.resize(face_roi, (32, 32))
                    face_normalized = face_resized / 255.0
                    face_reshaped = np.reshape(face_normalized, (1, 32, 32, 3))
                    
                    texture_variance = compute_texture_variance(face_roi)
                    texture_threshold = 5000
                    eyes_open = are_eyes_open(roi_gray)
                    small_area_threshold = 10000
                    single_face_threshold = 1
                    
                    if texture_variance > texture_threshold or not eyes_open:
                        liveness_label = 'Fake'
                        fake_count+=1
                    elif w * h < small_area_threshold:
                        liveness_label = 'Fake'
                        fake_count+=1
                    elif len(faces) > single_face_threshold:
                        liveness_label = 'Fake'
                        fake_count+=1
                    else:
                        liveness_output = liveness_model.predict(face_reshaped)
                        liveness_label = labels[np.argmax(liveness_output)]
                        liveness_confidence = liveness_output[0][np.argmax(liveness_output)]
                        
                    id, predict = clf.predict(roi_gray)
                    confidence = int((100 * (1 - predict / 300)))

                    my_cursor.execute("SELECT first_name FROM user WHERE acc_no=" + str(id))
                    n = my_cursor.fetchone()
                    n = "+".join(n)

                    if confidence > 77 and liveness_label == 'Real':
                        my_cursor.execute("SELECT acc_no, first_name FROM user WHERE mobile_no=" + mob_no)
                        result = my_cursor.fetchone()
                        acc_no = result[0]
                        first_name = result[1]
                        cv2.putText(frame, f"Name: {n}", (x, y - 55), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
                        cv2.putText(frame, f"Acc_no: {id}", (x, y - 15), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)

                        if acc_no == str(id).strip():
                            cv2.putText(frame, "Access Granted", (x, y - 35), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
                            access_granted=True
                        else:
                            cv2.putText(frame, "Access Denied", (x, y - 35), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 255), 3)
                    else:
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 3)
                        cv2.putText(frame, "Unknown face or Fake", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, f'{liveness_label}: {liveness_confidence:.2f}', (x, y - 75),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                cv2.imshow('Face Recognition and Liveness Detection', frame)
                if cv2.waitKey(1) == 13 or int(img_counter) == 100:
                    break
            cap.release()
            cv2.destroyAllWindows()
        run_access_control()
        if access_granted and fake_count<5:
                # pass
                self.pin(mob_no)
        else:
            messagebox.showerror("Error","Try again, You tried to spoof",parent = self.root)
            return False
        return True
    def pin(self,mob_no):
        self.new_window=Toplevel(self.root)
        self.app = pinwindow(self.new_window,mob_no)



if __name__=='__main__':
    root = Tk()
    obj = send_money(root,mob_no)
    root.mainloop()
