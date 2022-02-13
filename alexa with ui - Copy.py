import sys
import speedtest
import instaloader
import pyautogui
import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import smtplib
import wolframalpha
import requests
from bs4 import BeautifulSoup
import pyjokes
import subprocess
import ctypes
import time
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer,QTime, QDate,Qt
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from alexaui import Ui_MainWindow
from requests import get
import pywhatkit as wkit
import psutil

engine = pyttsx3.init("sapi5")
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def speak(audio):  # text to speech
    engine.say(audio)
    # print(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)

    if 0 <= hour < 12:
        speak("Good Morning")
    elif 12 <= hour < 18:
        speak("Good Afternoon")
    else:
        speak(f"Good Evening")

    speak(f"I am alexa ")
    speak("How may I help you?")



def sendEmail(to_, content_):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('username', 'password')
    server.sendmail('email', to_, content_)
    server.close()



def search(web):
    url = "https://www.google.co.in/search?q=" + web

    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
    }
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    try:
        result = soup.find(class_="Z0LcW XcVN5d").get_text()
        print(result)
        speak(result)
    except Exception:
        try:
            result = soup.find(class_="hgKElc").get_text()
            print(result)
            speak(result)
        except Exception:
            result = soup.find(class_="kno-rdesc").get_text()
            result = result.replace('Description', '')
            result = result.replace('Wikipedia', '')
            print(result)
            speak(result)

class MainThread(QThread):
    def __init__(self):
        super(MainThread,self).__init__()

    def run(self):
        self.TaskExecution()



    def takeCommand(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("listening.....")
            try:
                r.pause_threshold = 1
                audio = r.listen(source, timeout=None, phrase_time_limit=5)
                print("Recognising......")
                string = r.recognize_google(audio, language='en-in')
                print(f"user said:  {string}")
            except Exception:
                print("say that again please")
                return "none"
            return string


    def TaskExecution(self):
        wishMe()
        while True:
            self.query = self.takeCommand().lower()
            # creating logics

            if 'wikipedia' in self.query:
                speak('Searching wikipedia....')
                self.query = self.query.replace('wikipedia', '')
                try:
                    results = wikipedia.summary(self.query, sentences=2)
                    speak("According to wikipedia....")
                    print(results)
                    speak(results)
                except Exception as e:
                    print(e)
                    speak("No data found in wikipedia")

            elif "your name" in self.query:
                speak("My name is alexa")
                speak("how may I help you")

            elif 'hi' in self.query or 'hello' in self.query or 'hi' in self.query:
                speak("Hello")
                speak("how may I help you")

            elif "ok" in self.query:
                speak('say something')

            elif 'good morning' in self.query or 'good afternoon' in self.query or 'good avening' in self.query:
                hour = int(datetime.datetime.now().hour)
                if 0 <= hour < 12:
                    speak("Good Morning")
                elif 12 <= hour < 18:
                    speak("Good Afternoon")
                else:
                    speak(f"Good Evening")
                speak("how may I help you")

            elif 'good night' in self.query:
                speak("Good Night")
                speak("Sweet Dreams")
                speak("Should I stop?")
                self.query = self.takeCommand().lower()
                if 'yes' in self.query:
                    speak("Closing")
                    sys.exit()

            elif "my name" in self.query:
                speak("Your name is vikas")
                speak("how may I help you sir")

            elif "my love" in self.query:
                speak("You have not tell me yet")

            elif "what are you doing" in self.query or "what is going on" in self.query:
                speak("Waiting for your commands")

            elif "who are you" in self.query:
                speak("I am your voice assistant")
                speak("What can I do for you")

            elif "what can you do" in self.query:
                speak("You can say open youtube")
                speak("or Play music")

            elif 'open youtube' in self.query:
                speak("opening YouTube")
                webbrowser.open('Youtube.com')

            elif 'play song on youtube' in self.query:
                speak("what have to play on youtube")
                name=self.takeCommand()
                wkit.playonyt(name)

            elif 'open google' in self.query:
                speak("opening google")
                webbrowser.open('google.com')
            elif 'stack overflow' in self.query:
                speak("opening stackoverflow")
                webbrowser.open('stackoverflow.com')
            elif 'search' in self.query:
                self.query = self.query.replace('search', '')
                speak("searching")
                webbrowser.open(self.query)
            elif 'open instagram' in self.query:
                speak("opening instagram")
                webbrowser.open('instagram.com')

            elif 'play music' in self.query or 'play a song' in self.query:
                music_dir = 'D:\\music'
                songs = os.listdir(music_dir)
                speak("playing music")
                os.startfile(os.path.join(music_dir, songs[0]))

            elif 'ip address' in self.query:
                ip = get('https://api.ipify.org').text
                print(f"your IP address is {ip}")
                speak(f"your IP address is {ip}")

            elif 'the time' in self.query:
                strTime = datetime.datetime.now().strftime("%H:%M:%S")
                print(strTime)
                speak(f"Sir, the time is {strTime}")

            elif 'open code blocks' in self.query:
                filepath = "C:\\Program Files\\CodeBlocks\\codeblocks.exe"
                speak("opening codeblocks")
                os.startfile(filepath)
            elif 'open pycharm' in self.query:
                filepath = "C:\\Program Files\\JetBrains\\PyCharm Community Edition 2021.1.2\\bin\\pycharm64.exe"
                speak("opening pycharm")
                os.startfile(filepath)
            elif 'open notepad' in self.query:
                filepath = "C:\\Windows\\system32\\notepad.exe"
                speak("opening notepad")
                os.startfile(filepath)
            elif 'open paint' in self.query:
                filepath = "C:\\Windows\\system32\\mspaint.exe"
                speak("opening paint")
                os.startfile(filepath)
            elif 'open command promp' in self.query or 'open cmd' in self.query:
                filepath = "C:\\Windows\\system32\\cmd.exe"
                speak("opening command prompt")
                os.startfile(filepath)
            elif 'open adobe' in self.query or 'open pdf reader' in self.query:
                filepath = "C:\\Program Files (x86)\\Adobe\\Acrobat Reader DC\\Reader\\AcroRd32.exe"
                speak("opening adobe pdf reader")
                os.startfile(filepath)
            elif 'open excel' in self.query:
                filepath = "C:\\Program Files\\Microsoft Office\\root\Office16\\EXCEL.EXE"
                speak("opening Microsoft Excel")
                os.startfile(filepath)
            elif 'open word' in self.query:
                filepath = "C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE"
                speak("opening microsoft word")
                os.startfile(filepath)
            elif 'open powerpoint' in self.query:
                filepath = "C:\\Program Files\\Microsoft Office\\root\\Office16\\POWERPNT.EXE"
                speak("opening Microsoft Power Point")
                os.startfile(filepath)
            elif 'open chrome' in self.query or 'open browser' in self.query:
                filepath = "C:\\Program Files (x86)\Google\\Chrome\\Application\\chrome.exe"
                speak("opening chrome browser")
                os.startfile(filepath)
            elif 'open setting' in self.query:
                filepath = "C:\\Windows\\System32\\Control.exe"
                speak("opening settings")
                os.startfile(filepath)

            elif 'close code blocks' in self.query:
                speak("closing")
                os.system('TASKKILL /F /IM codeblocks.exe')
            elif 'close pycharm' in self.query:
                speak("closing")
                os.system('TASKKILL /F /IM pycharm64.exe')
            elif 'close notepad' in self.query:
                speak("closing")
                os.system('TASKKILL /F /IM notepad.exe')

            elif 'close paint' in self.query:
                speak("closing")
                os.system('TASKKILL /F /IM mspaint.exe')
            elif 'close command promp' in self.query or 'close cmd' in self.query:
                speak("closing")
                os.system('TASKKILL /F /IM cmd.exe')
            elif 'close adobe' in self.query or 'close pdf reader' in self.query:
                speak("closing")
                os.system('TASKKILL /F /IM AcroRd32.exe')
            elif 'close excel' in self.query:
                speak("closing")
                os.system('TASKKILL /F /IM excel.exe')
            elif 'close word' in self.query:
                speak("closing")
                os.system('TASKKILL /F /IM winword.exe')
                os.startfile(filepath)
            elif 'close powerpoint' in self.query:
                speak("closing")
                os.system('TASKKILL /F /IM powerpnt.exe')
            elif 'close chrome' in self.query or 'close browser' in self.query:
                speak("closing")
                os.system('TASKKILL /F /IM chrome.exe')
                os.startfile(filepath)
            elif 'close setting' in self.query:
                speak("closing")
                os.system('TASKKILL /F /IM control.exe')

            elif 'switch window' in self.query or 'switch tab' in self.query:
                pyautogui.keyDown('alt')
                pyautogui.press("tab")
                time.sleep(1)
                pyautogui.keyUp('alt')



            elif 'send message' in self.query or 'send a message' in self.query:
                try:
                    speak("what I say")
                    message = self.takeCommand().lower()
                    wkit.sendwhatmsg_instantly("+917448020583",message,10)
                    speak("message has been sent")
                except Exception:
                    speak("Unable to send at the moment")


            elif 'send email' in self.query:
                try:
                    speak("What should I say?")
                    content = self.takeCommand()
                    to = "email"							# enter email id 
                    speak("Sending Email")
                    sendEmail(to, content)
                    speak("Email has been sent")
                except Exception as e:
                    print(e)
                    speak("sorry, I am not able to send email at this moment")


            elif "say hi to" in self.query:
                name = self.query.replace("say hi to", "")
                speak(f"Hi {name}")
                speak("Nice to meet You")
                speak("how may I help you")

            elif self.query == "none":
                pass

            elif 'calculate' in self.query:
                try:
                    client = wolframalpha.Client('client id')				# create your client id
                    res = client.query(self.query)
                    answer = next(res.results).text
                    print(answer)
                    speak(answer)
                except Exception:
                    webbrowser.open("https://www.google.co.in/search?q=" + self.query)

            elif 'joke' in self.query:
                joke = pyjokes.get_joke(language="en", category='all')
                print(joke)
                speak(joke)

            elif "who i am" in self.query:
                speak("If you talk then definitely your human.")

            elif "why you came to world" in self.query:
                speak("Thanks to Vikas. further It's a secret")

            elif 'is love' in self.query:
                speak("It is 7th sense that destroy all other senses")

            elif "Good Morning" in self.query:
                speak("Good Morning")
                speak("How are you ")

            elif "will you be my girlfriend" in self.query or "will you be my boyfriend" in self.query:
                speak("I'm not sure about, may be you should give me some time")

            elif "how are you" in self.query or 'what about you' in self.query:
                speak("I'm fine, Thank You. How may I help you")

            elif "i love you" in self.query:
                speak("Ooops. It's hard to understand")

            elif "sleep" in self.query:
                speak("Sleeping")
                speak("to continue just say alexa")
                i=True
                while i:
                    self.query = self.takeCommand().lower()
                    if "alexa" in self.query or 'are you there' in self.query or "hello" in self.query or 'wake up' in self.query:
                        speak("Yes Sir. Ready to go")
                        i=False


            elif "where is" in self.query or "how to go to " in self.query:
                self.query = self.query.replace("where is", "")
                self.query = self.query.replace("how to go to", "")
                location = self.query
                speak("User asked to Locate")
                speak(location)
                webbrowser.open("https://www.google.com/maps/place/" + location)

            elif 'where I am' in self.query or 'find my location' in self.query:
                speak("wait sir... let me check")
                try:
                    ipAdd = requests.get('https://api.ipify.org').text
                    print(ipAdd)
                    url= 'https://get.geojs.io/v1/ip/geo/' + ipAdd + '.json'
                    geo_requsts = requests.get(url)
                    geo_data = geo_requsts.json()
                    city = geo_data['city']
                    country = geo_data['country']
                    speak(f"sir I am not sure, but I think we are in {city} city of {country} country")
                except Exception:
                    speak("Sorry, I am not able find location at this momemt")
                    pass

            elif "battery" in self.query or "charging" in self.query:
                battery = psutil.sensors_battery()
                percent = battery.percent
                speak(f"Sir our system have {percent} percent battery")

            elif "don't listen" in self.query or "stop listening" in self.query:
                speak("for how much time you want to stop alexa from listening commands")
                try:
                    a = self.takeCommand()
                    a = int(a.rstrip())
                    print(a)
                    time.sleep(a)
                except Exception:
                    time.sleep(10)
                    speak('stop listening for 10 seconds')
            elif "screenshot" in self.query:
                speak("sir, please tell me the name for this screenshot")
                name= self.takeCommand().lower()
                speak("please sir hold the screen for few seconds, i am taking screenshot")
                time.sleep(3)
                img = pyautogui.screenshot()
                img.save(f"{name}.png")
                speak("Screenshot captured succesfully. Now I am ready for next task")

            elif  'lock' in self.query:
                speak("locking the device")
                ctypes.windll.user32.LockWorkStation()

            elif 'shutdown' in self.query:
                speak('Hold On a Sec! do you really want to shut down')
                self.query = self.takeCommand().lower()
                if 'yes' in self.query:
                    speak("Your system is on its way to shut down")
                    subprocess.call('shutdown / p /f')
                    speak('shutting down')
                    sys.exit()
                else:
                    pass

            elif "restart" in self.query:
                speak("Hold On a Sec! Do you really want to restart the system")
                self.query = self.takeCommand().lower()
                if 'yes' in self.query:
                    speak(" Your system is on its way to restarting")
                    subprocess.call(["shutdown", "/r"])
                    speak("restarting window")
                    sys.exit()
                else:
                    pass

            elif "log off" in self.query or "sign out" in self.query or "log out" in self.query:
                speak("Hold On a Sec ! Do you really want to lof off")
                self.query = self.takeCommand().lower()
                if 'yes' in self.query:
                    speak(" Your system is on its way to signing out")
                    time.sleep(5)
                    subprocess.call(["shutdown", "/l"])
                    speak("signing out")
                    sys.exit()
                else:
                    pass

            elif "hibernate" in self.query or "sleep mode" in self.query:
                speak("Sleeping down")
                subprocess.call("shutdown /h")
                time.sleep(5)

            elif "quit" in self.query or "close" in self.query or "stop" in self.query:
                speak("Okay.")
                speak("Thank You for usig me")
                sys.exit()

            elif "thank you" in self.query :
                speak("Its my plesure sir")
                speak("how may I help you?")

            elif 'internet speed' in self.query:
                st= speedtest.Speedtest()
                dl = st.download()
                ul = st.upload()
                speak(f"Sir we have {dl} bits per seconds downloading speed and {ul} bit per second uploading speed")


            else:
                try:
                    search(self.query)
                except Exception:
                    webbrowser.open("https://www.google.co.in/search?q=" + self.query)

startExecution = MainThread()

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.startTask)
        self.ui.pushButton_2.clicked.connect(self.close)

    def startTask(self):
        self.ui.movie = QtGui.QMovie("E:/Alexa Project With UI/d424ae049c8097d63d29e9931d8a1280.gif")
        self.ui.label.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("E:/Alexa Project With UI/012dfc3300856f39ecfad5ca682c1b37.gif")
        self.ui.label_2.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("E:/Alexa Project With UI/Choker _ NamGi.gif")
        self.ui.label_3.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("E:/Alexa Project With UI/5208caa56757e87a8282b1772fe96409.gif")
        self.ui.label_7.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("E:/Alexa Project With UI/be92f51ef908d53c0c74d5e06a59365e.gif")
        self.ui.label_8.setMovie(self.ui.movie)
        self.ui.movie.start()
        timer=QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)
        startExecution.start()

    def showTime(self):
        current_time = QTime.currentTime()
        current_date = QDate.currentDate()
        label_time = current_time.toString('hh:mm:ss')
        label_date = current_date.toString(Qt.ISODate)
        self.ui.textBrowser.setText(label_date)
        self.ui.textBrowser_2.setText(label_time)

app = QApplication(sys.argv)
alexa = Main()
alexa.show()
exit(app.exec_())
