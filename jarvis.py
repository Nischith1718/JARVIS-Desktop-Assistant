import pyttsx3
import datetime
import speech_recognition as sr
import webbrowser
import wikipedia
import pywhatkit
import pyautogui
from pygame import mixer
from bardapi import BardCookies
import tkinter as tk
from tkinter import ttk
from plyer import notification

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


def start_listening():
    def speak(audio):
        engine.say(audio)
        response_text.set(audio)
        engine.runAndWait()

    def wishMe():
        hour = int(datetime.datetime.now().hour)

        if 0 < hour < 12:
            speak("Good Morning Sir")
        elif 12 <= hour <= 18:
            speak("Good Afternoon Sir")
        else:
            speak("Good Night Sir")

        speak("How may I help you?")

    def takeCommand():
        r = sr.Recognizer()
        m = sr.Microphone()

        try:
            with m as source:
                print("Listening... ")
                r.pause_threshold = 1
                audio = r.listen(source)
                print("Recognizing...")
                query = r.recognize_google(audio, language='en-in')
                print(f'User said: {query}')


        except:
            print("Say that again...")
            return "None"

        return query

    def searchGoogle(query):
        if "google" in query:
            import wikipedia as googleScarp
            query = query.replace('jarvis', "")
            query = query.replace('search', "")
            query = query.replace('google', "")
            query = query.replace('on', "")
            query = query.replace('open', "")
            speak("This is what I found on google...")

            try:
                pywhatkit.search(query)
                result = googleScarp.summary(query, 2)
                speak(result)

            except:
                speak("No output...")

    def searchYoutube(query):
        if "youtube" in query:
            speak("This is what I found online...")
            query = query.replace('jarvis', "")
            query = query.replace('youtube search', "")
            query = query.replace('youtube', "")
            query = query.replace('search', "")
            query = query.replace('on', "")
            query = query.replace('open', "")
            web = "https://www.youtube.com/results?search_query=" + query
            webbrowser.open(web)
            pywhatkit.playonyt(query)

    def searchWikipedia(query):
        if "wikipedia" in query:
            speak("Here's what I found from wikipedia...")
            query = query.replace('jarvis', "")
            query = query.replace('search', "")
            query = query.replace('wikipedia', "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to wikipedia...")
            print(results)
            speak(results)


    def ai(command):
        cookie_dict = {
            "__Secure-1PSID": "dAhYQy8t1hSYMD-D_EEEwO4kpufAjN3HyLRbzwruSHQZq3S8RyKhhpeoku6gc7CfuiVpAg.",
            "__Secure-1PSIDTS": "sidts-CjIBNiGH7qXFDYsrTYddhT1G3yErRakUalK-RRMDuXVqBu6jxDy2lEnx9NW81BEqBzd0CxAA",
            "__Secure-1PSIDCC": "ACA-OxM1S2mA84p7oNlcMt4-QBze1v3XD7fOO-JX8e5iBQJs7OCJqi-gpqQlbWkbd1jfoM8v1g"
        }

        bard = BardCookies(cookie_dict=cookie_dict)

        def split_and_save_paragraphs(data, filename):
            paragraphs = data.split('\n\n')
            with open(filename, 'w') as file:
                file.write(data)
            data = paragraphs[:2]
            separator = ', '
            joined_string = separator.join(data)
            return joined_string

        # Main Execution

        RealQuestion = str(command)
        results = bard.get_answer(RealQuestion)['content']
        current_datetime = datetime.datetime.now()
        formatted_time = current_datetime.strftime("%H%M%S")
        filenamedate = str(formatted_time) + str(".txt")
        filenamedate = "C:\\Users\\nisch\\PycharmProjects\\Jarvis\\DataBase\\" + filenamedate
        speak(split_and_save_paragraphs(results, filename=filenamedate))

    if __name__ == "__main__":

        speak('Hello I am Jarvis')
        wishMe()
        while True:
            command = takeCommand()
            command1 = command.lower()

            if 'the time' in command1:
                strfTime = datetime.datetime.now().strftime("%H:%M:%S")
                speak(f'Sir the time is {strfTime}')

            elif 'google' in command1:
                searchGoogle(command1)

            elif 'youtube' in command1:
                searchYoutube(command1)

            elif 'wikipedia' in command1:
                searchWikipedia(command1)

            elif 'open' in command1:
                command1 = command1.replace('open', "")
                command1 = command1.replace('jarvis', "")
                pyautogui.press('super')
                pyautogui.typewrite(command1)
                pyautogui.sleep(2)
                pyautogui.press('enter')

            elif 'using artificial intelligence' in command1:
                ai(command1)


            elif 'alarm' in command1:
                speak("Enter the time: ")
                time = input("Enter time in HH:MM:SS format")

                while True:
                    Time_Ac = datetime.datetime.now()
                    now = Time_Ac.strftime("%H:%M:%S")

                    if now == time:
                        speak("Time to wake up sir!!")
                        mixer.init()
                        mixer.music.load("give a song file path from your computer")
                        mixer.music.play()

                    elif now > time:
                        break

            elif 'schedule my day' in command1:
                tasks = []
                speak("Do you want to clear previous tasks (Answer in YES or NO)")
                answer = takeCommand().lower()
                if 'yes' in answer:
                    file = open("tasks.txt", "w")
                    file.write(f"")
                    file.close()
                    speak("Enter the no. of tasks: ")
                    no_tasks = int(input("Enter the no. of tasks: "))

                    for i in range(no_tasks):
                        tasks.append(input("Enter the task: "))
                        file = open("tasks.txt", "a")
                        file.write(f"{i}. {tasks[i]}\n")
                        file.close()
                elif 'no' in answer:
                    speak("Enter the no. of tasks: ")
                    no_tasks = int(input("Enter the no. of tasks: "))

                    for i in range(no_tasks):
                        tasks.append(input("Enter the task: "))
                        file = open("tasks.txt", "a")
                        file.write(f"{i}. {tasks[i]}\n")
                        file.close()

            elif 'show my schedule' in command1:
                file = open("tasks.txt", 'r')
                content = file.read()
                notification.notify(
                    title="My schedule: ",
                    message=content,
                    timeout=15
                )



            elif 'shutdown' in command1:
                speak("Going offline sir...")
                break


def exit_application():
    root.destroy()


root = tk.Tk()
root.title("JARVIS")
root.configure(bg="black")
root.geometry("1440x900")


image_path = "Give image path from your computer"
img = tk.PhotoImage(file=image_path)


image_label = tk.Label(root, image=img, bg="black")
image_label.image = img
image_label.place(relx=0.5, rely=0.5, anchor="center")

response_text = tk.StringVar()
response_label = tk.Label(root, textvariable=response_text, fg="black", bg="white", font=("Arial", 18))
response_label.place(relx=0.5, rely=0.9, anchor='center')


start_button = ttk.Button(root, text="Start Listening", command=start_listening)
start_button.place(relx=0.3, rely=0.8, anchor="center")


exit_button = ttk.Button(root, text="Exit", command=exit_application)
exit_button.place(relx=0.7, rely=0.8, anchor="center")

root.mainloop()
