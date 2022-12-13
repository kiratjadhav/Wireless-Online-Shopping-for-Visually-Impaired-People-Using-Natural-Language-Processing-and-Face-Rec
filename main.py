import numpy as np 
import cv2
import pickle

import os
import time
import playsound
import speech_recognition as sr
from gtts import gTTS

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains



path = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(path)

#face-recog trained data
face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt2.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainner.yml")


#face-recog
def face_recog():
    og_labels = {}
    labels ={}
    with open("labels.pickle", "rb") as f:
        og_labels = pickle.load(f)
        labels = {v:k for k,v in og_labels.items()}

    cap = cv2.VideoCapture(0)

    while(True):
        #capture frame
        ret, frame =cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
        

        for(x, y, w, h) in faces:
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]

            #recognize
            id_, conf = recognizer.predict(roi_gray)
            if conf>=45 and conf<=85:
                name = labels[id_]
                font = cv2.FONT_HERSHEY_SIMPLEX
                color = (255,234,133)
                stroke = 2 
                cv2.putText(frame, name, (x,y), font, 1.5, color, stroke, cv2.LINE_AA)

            img_item = "new_image.png"
            cv2.imwrite(img_item, frame)

            color= (234, 234,122)
            stroke = 2
            end_cord_x = x + w
            end_cord_y = y + h
            cv2.rectangle(frame, (x, y), (end_cord_x, end_cord_y), color, stroke)

        cv2.imshow('frame', frame)

        if cv2.waitKey(6000) or 0xFF == ord('q'):
            break
        
    cap.release()
    cv2.destroyAllWindows()
    return name


# speak given text 
def speak(text):
    tts = gTTS(text=text, lang="en")
    filename = "voice_main.mp3"
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)

#specifying url to visit
def web(said):
    driver.get(said)


# listening to audio and return text
def get_audio():
    r = sr.Recognizer();
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ""
        try:
            said = r.recognize_google(audio)
            print(said)
        except Exception as e:
            print("Exception: " + str(e))
        return said


def web_open(domain):
    driver.get("https://" + domain + ".in")

#login process
def login(name):
    if(name == "kirat"):
        loginTextArea = driver.find_element_by_id("ap_email")
        loginTextArea.send_keys("enter email here")
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "continue"))).click()

        passwordTextArea = driver.find_element_by_id("ap_password")
        passwordTextArea.send_keys("enter password here")
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "signInSubmit"))).click()
        
        

#searching a specific product which is store in ITEM variable
def search_prod(): 
    search = driver.find_element_by_id("twotabsearchtextbox")
    search.send_keys("red tshirts")
    speak("searching for red tshirts")
    search.send_keys(Keys.RETURN)


#filtering products
def filter_prod():
#clicking 3 stars and above products image on left hand side 
    speak("Please wait, Filtering out products having ratings 4 and above")
    stars = driver.find_element_by_id('p_72/2661619011')
    stars.click()
    speak(" Filtering of products complete ")

    name = driver.find_elements_by_tag_name('h5')   
    price = driver.find_elements_by_class_name('a-price-whole')

    n=0
    for p in price:
        if(n <=5 ):
            print(name[n].text+" : $"+p.text)
            n+=1
        else:
            break



    print ("done")


























#web_open("amazon")
#time.sleep(1)



#item = get_audio()







#driver.quit()
