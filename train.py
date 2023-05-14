import os
import numpy as np
import cv2
from PIL import ImageTk
import PIL.Image
from tkinter import *
from tkinter import ttk

def train_classifier():
    data_dir=("data_images_signup")
    path= [os.path.join(data_dir,file)for file in os.listdir(data_dir) ]

    faces=[]
    ids=[]
    for image in path:
        img=PIL.Image.open(image).convert('L')
        imageNp=np.array(img,'uint8')
        id = int(os.path.split(image)[1].split('.')[1])
        faces.append(imageNp)
        ids.append(id)
        cv2.imshow("Training",imageNp)
        cv2.waitKey(1)==13
    ids = np.array(ids)

    clf = cv2.face.LBPHFaceRecognizer_create()
    clf.train(faces,ids)
    clf.write("classifier.xml")
    cv2.destroyAllWindows()
train_classifier()