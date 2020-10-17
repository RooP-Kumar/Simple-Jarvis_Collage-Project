import os
from datetime import datetime
import webbrowser
import time
import wikipedia
import smtplib
import json
hour = datetime.now().hour

def speak(audio):
    import pyttsx3
    computer = pyttsx3.init('sapi5') # you in windows then replace'expeak' to 'sapi5'.
    rate = computer.getProperty('rate')
    computer.setProperty('rate', 140)
    voices = computer.getProperty('voices')
    computer.setProperty('voice', voices[1].id)
    computer.say(audio)
    computer.runAndWait()

def greeting():
    if hour >= 0 and hour < 12:
        speak('Good Morning everyone.')

    elif hour >= 12 and hour < 15:
        speak('Good Afternoon everyone.')

    elif hour >= 15 and hour < 18:
        speak('Good Evening everyone')

def get_json():
    with open('main.json', 'r') as f:
        data = json.load(f)

    return data

def shut_down():
    if hour < 20:
        speak('Good Bye.')
        exit()
    elif hour >= 20:
        speak('Good Night.')
        exit()

def send_email(sender, password, to, context):
    s = smtplib.SMTP('smtp.gmail.com', 587)

    s.starttls()
    s.ehlo()
    s.login(sender, password)
    s.sendmail(sender, [to], context)
    print('email sent')
    speak('Email sent')

def wait():
    time.sleep(15)

def recognize_voice():
    import speech_recognition as sr
    r = sr.Recognizer()
    with sr.Microphone() as user_audio:
        print('Listening ..................')
        audio = r.listen(user_audio)

    try:
        print('Recognition ..................')
        query = r.recognize_google(audio).capitalize() # query is string which containing you voice.
        print(f'you said :- {query}')
        return query

    except sr.UnknownValueError as e:
        print('Can not understand what are you saying..')
        speak('Sorry. speak again')
        recognize_voice()

    except sr.RequestError as e:
        print('Unknown Request by you.')
        speak('Sorry. speak again')
        recognize_voice()


if __name__ == "__main__":
    while (True):
        query = recognize_voice()        

        if 'Google' in query:
            speak('Google.com is opening.')
            webbrowser.open('google.com')
            time.sleep(3)

        elif 'Youtube' in query:
            speak('Youtube.com is opening.')
            webbrowser.open('youtube.com')
            time.sleep(3)

        elif ('Facebook' or 'facebood') in query:
            speak('Facebook.com is opening.')
            webbrowser.open('facebook.com')
            time.sleep(3)

        elif 'Search' in query:
            final_query = query[6:]
            speak('wait. Searching is in progress')
            result = wikipedia.summary(final_query, sentences = 2)
            speak('Founded.')
            print(result)
            speak(result)

        elif 'Send' in query:
            try:
                data = get_json()
                something_hide = query.replace(" ", "")
                n = something_hide.index('o')
                main_reciver = something_hide[n:]
                speak('Now. What do you want to tell him or her')
                context = recognize_voice()
                reciever = (f"{main_reciver}@gmail.com") 
                send_email(data['user_name'], data['password'], reciever, context)

            except Exception as e:
                speak(r"Sorry. Don't Recongnize")


        elif 'Wait' in query:
            speak('OK')
            wait()

        elif 'Down' in query:
            speak('OK')
            shut_down()

        elif 'down' in query:
            speak('OK')
            shut_down()


