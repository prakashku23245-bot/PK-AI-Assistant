import pyttsx3
import datetime
import os
import ollama

engine = pyttsx3.init()

def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()

speak("Hello Prakash,  PK AI is ready")

while True:

    user = input("You: ").lower()

    if user == "exit":
        speak("Goodbye")
        break

    elif "time" in user:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {current_time}")

    elif "calculator" in user:
        speak("Opening Calculator")
        os.system("calc")

    elif "notepad" in user:
        speak("Opening Notepad")
        os.system("notepad")

    elif "chrome" in user:
        speak("Opening Chrome")
        os.system("start chrome")

    else:
        try:
            response = ollama.chat(
                model="phi3:mini",
                messages=[
                    {"role": "user", "content": user}
                ]
            )

            answer = response["message"]["content"]
            speak(answer)

        except Exception as e:
            speak("Sorry, AI is not available")
            print(e)