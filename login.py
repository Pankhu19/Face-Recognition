from tkinter import *
from tkinter import ttk
from PIL import Image,ImageTk
# import PIL.Image
from otp import otp
import mysql.connector
from tkinter import messagebox
import cv2
import os
import numpy as np
import tensorflow as tf
from config import passw

class login:
    var_mobile=''
    def __init__(self,root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")

        self.var_pass = StringVar()
        self.var_mobile = StringVar()

        limg = Image.open(r"Photos\limg1.jpg")
        limg = limg.resize((1530,790),Image.ANTIALIAS)
        self.photolimg = ImageTk.PhotoImage(limg)

        lbg_img = Label(self.root,image = self.photolimg)
        lbg_img.place(x=0,y=0,width=1400,height=790)

        title_lbll=Label(lbg_img,text="Log in", font=("Imprint MT Shadow",45,"bold"),fg="black", anchor="center")
        title_lbll.place(relx=0.5, rely=0.2, anchor="center")

        main_frame = Frame(lbg_img,bd=2)
        main_frame.place(x=450,y=300,width = 500,height=180)

        mobile_label = Label(main_frame,text="Mobile no:",font=("Cascadia Code",14,"italic","bold"))
        mobile_label.grid(row=1,column=0,padx=10,pady=5, sticky=W)
        mobile_entry = ttk.Entry(main_frame,textvariable=self.var_mobile,width =28,font=("Cascadia Code",14,"bold"))
        mobile_entry.grid(row=1,column=1,padx=10,pady=5, sticky=W)

        pass_label = Label(main_frame,text="Password:",font=("Cascadia Code",14,"italic","bold"))
        pass_label.grid(row=2,column=0,padx=10,pady=5, sticky=W)
        pass_entry = ttk.Entry(main_frame,textvariable=self.var_pass,width =28,font=("Cascadia Code",14,"bold"))
        pass_entry.grid(row=2,column=1,padx=10,pady=5, sticky=W)

        img_verify = Image.open(r"Photos\verify-removebg-preview.png")
        img_verify = img_verify.resize((320,240),Image.ANTIALIAS)
        self.photoimg_verify = ImageTk.PhotoImage(img_verify)

        b3 = Button(lbg_img,image = self.photoimg_verify,command =self.validate_user ,cursor="hand2")
        b3.place(x=615,y=410,width = 150, height = 50)

    def otp_conn(self,mob_no):
        self.new_window=Toplevel(self.root)
        self.app = otp(self.new_window,mob_no)
    
    def validate_user(self):
        # try:
            conn = mysql.connector.connect(host = "localhost",username = "root", password=passw,database = "face_recognition")
            my_cursor = conn.cursor()
            mob_no = self.var_mobile.get()
            global mob_no_global
            mob_no_global = mob_no
            my_cursor.execute("select * from user where mobile_no=%s and pass=%s",(mob_no,self.var_pass.get()))
            result = my_cursor.fetchone()
            conn.close()
            if result:
                messagebox.showinfo("","Going for image capture",parent = self.root)
                self.face_recog()

            else:
                messagebox.showerror("Error","Invalid username or password")
        # except Exception as es:
        #     messagebox.showerror("Error",f"Due to: {str(es)}",parent = self.root)

    def face_recog(self):
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
                        my_cursor.execute("SELECT acc_no, first_name FROM user WHERE mobile_no=" + self.var_mobile.get())
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
                self.otp_conn(mob_no_global)
        else:
            messagebox.showerror("Error","Try again, You tried to spoof")


if __name__=='__main__':
    root = Tk()
    obj = login(root)
    # mob_no = obj.var_mobile
    root.mainloop()