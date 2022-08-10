from ast import Break
from distutils.cmd import Command
from math import fabs
from sys import breakpointhook
from tkinter import *
from time import sleep
import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import pyttsx3
from lib2to3.pgen2.token import NAME
import shutil
import http.server
import socketserver
import socket
import threading



win = Tk()
win.title('Face Attendance System [ Made by Dhananjay Sah ]')
win.geometry("800x650")
bg = PhotoImage(file = "img.png")
label1 = Label(win, image = bg)
label1.place(x = 0, y = 0)
p1 = PhotoImage(file = 'icon.png')
# Setting icon of master window
win.iconphoto(False, p1)




###################################################################
# Web Server
###################################################################
def Web_server():
    ip = socket.gethostbyname(socket.gethostname())
    PORT = 8080
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer((str(ip), PORT), Handler) as httpd:

        httpd.serve_forever()



###################################################################
# Clear About Windows
###################################################################
def Clear():
    txt.place_forget()
    back.place_forget()
    pass


###################################################################
# Add New User
###################################################################
def Add_usr():
    l = usr.get()
    name = "name.jpg"
    vid = cv2.VideoCapture(0)
    while(True):
        ret, frame = vid.read()
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.imwrite(name,frame)
            os.rename("name.jpg",str(l)+".jpg")
            shutil.move(str(l)+".jpg","images")
            entry.delete(0,END)
            break
    vid.release()
    # Destroy all the windows
    cv2.destroyAllWindows()



##########################################################################
# Remove User
##########################################################################
def Del_usr():
    ur = usr.get()
    os.remove(f"images/{ur}.jpg")
    entry.delete(0,END)





#############################################################################
# Menu for Delete user
#############################################################################
def Del_menu():
    entry.config( width=10,fg="black",bg="white",bd=5,font=("Arial",40),textvariable=usr)
    entry.focus_set()
    entry.place(x=30,y=550)
    btn1.config(text="Del",bg="white",fg="black",bd="5px",font=("Arial",25),command=Del_usr)
    btn1.place(x=340,y=550)




#################################################################################
# Menu for add new user
#################################################################################    
def Add_menu():
    entry.config( width=10,fg="black",bg="white",bd=5,font=("Arial",40),textvariable=usr)
    entry.focus_set()
    entry.place(x=30,y=550)
    btn1.config(text="Add",bg="white",fg="black",bd="5px",font=("Arial",25),command=Add_usr)
    btn1.place(x=340,y=550)




##################################################################################
# About Function
##################################################################################
def About():
    txt.config(bg="white",fg="black",text="""
    Advance Facial Recognition Attendance System\n
    Made By Dhananjay Sah\n
    Email: rootuserdj@gmail.com\n
    Contact: +977 9824204425\n
    Github: https://github.com/rootuserdj\n
    Addres: Mahagadhimai Muncipality 4 (Nepal)\n
    """,bd=10,font=("Arial",15))
    txt.place(x=290,y=40)
    back.config(fg="green",bg='white',text="🔙",font=("Arial",30),command=Clear)
    back.place(x=675,y=380)


########################################################################################
# Images Matching 
########################################################################################
def matching():
    path = 'images'
    images = []
    personNames = []
    myList = os.listdir(path)
    for cu_img in myList:
        current_Img = cv2.imread(f'{path}/{cu_img}')
        images.append(current_Img)
        personNames.append(os.path.splitext(cu_img)[0])

    encodeListKnown = faceEncodings(images)

    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        faces = cv2.resize(frame,(0,0), None, fx=0.25, fy=0.25)

        faces = cv2.cvtColor(faces, cv2.COLOR_BGR2RGB)

        facesCurrentFrame = face_recognition.face_locations(faces)
        encodesCurrentFrame = face_recognition.face_encodings(faces, facesCurrentFrame)

        for encodeFace, faceLoc in zip(encodesCurrentFrame, facesCurrentFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            # print(faceDis)
            matchIndex = np.argmin(faceDis)
            if matches[matchIndex]:
                name = personNames[matchIndex].upper()
             # print(name)
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(frame, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(frame, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                attendance(name)
                Speak(name)

        cv2.imshow('Webcam', frame)
        if cv2.waitKey(1) == 13:
            break

    cap.release()
    cv2.destroyAllWindows()






###################################################################################
# Speak Function
###################################################################################
def Speak(name):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice' , voices[1].id)
    rate = engine.getProperty('rate')
    engine.setProperty('rate', 170)
    sound = "Thank you ",str(name),"Your Attendance will be Saved"
    engine.say(sound)
    sleep(2)
    engine.runAndWait()





###################################################################################
# Face Encoding
###################################################################################
def faceEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList



########################################################################################
# Writng the attendance in text file with time and date
########################################################################################
def attendance(name):
    with open('Attendance.txt', 'r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            time_now = datetime.now()
            tStr = time_now.strftime('%H:%M:%S')
            dStr = time_now.strftime('%d/%m/%Y')
            f.writelines(f'\n{name},{tStr},{dStr}')


# Start Code
btn = Button(win,text="☤Start",bg="white",fg="black",bd="5px",font=("Arial",30),command=matching)
btn.place(x=110,y=100)

# Add new users
btn2 = Button(win,text="👮Add",bg="white",fg="black",bd="5px",font=("Arial",30),command=Add_menu)
btn2.place(x=119,y=215)

btn3 = Button(win,text="👮Del",bg="white",fg="black",bd="5px",font=("Arial",30),command=Del_menu)
btn3.place(x=125,y=335)

btn4 = Button(win,text="☢About",bg="white",fg="black",bd="5px",font=("Arial",30),command=About)
btn4.place(x=105,y=450)

usr = StringVar()
entry = Entry(win,textvariable=usr)
entry.focus_set()
btn1 = Button(win,bg="white",fg="black",bd="5px",font=("Arial",25))
back = Button(win)
txt = Label(win)
server = threading.Thread(target=Web_server)
server.start()


win.mainloop()