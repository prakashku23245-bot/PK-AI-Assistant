import customtkinter as ctk
import ollama
import pyttsx3
import webbrowser
import threading
import queue
import sounddevice as sd
import json
from vosk import Model, KaldiRecognizer

# =========================
# VOICE ENGINE
# =========================
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

# =========================
# GUI SETUP
# =========================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("PK AI - Jarvis Mode")
app.geometry("900x600")

title = ctk.CTkLabel(app, text="PK AI - Jarvis Assistant", font=("Arial", 24, "bold"))
title.pack(pady=10)

chat_box = ctk.CTkTextbox(app, width=800, height=400)
chat_box.pack(pady=10)

entry = ctk.CTkEntry(app, width=700, placeholder_text="Ask PK AI...")
entry.pack(pady=10)

# =========================
# GOOGLE SEARCH
# =========================
def google_search(query):
    chat_box.insert("end", "PK AI: Searching Google...\n\n")
    webbrowser.open(f"https://www.google.com/search?q={query}")

# =========================
# OLLAMA CHAT
# =========================
def ai_reply(msg):
    response = ollama.chat(
        model="phi3:mini",
        messages=[{"role": "user", "content": msg}]
    )
    return response["message"]["content"]

# =========================
# SEND MESSAGE
# =========================
def send_message():

    user = entry.get()
    if not user.strip():
        return

    chat_box.insert("end", f"You: {user}\n\n")

    msg = user.lower()

    # Google search
    if "search" in msg or "google" in msg:
        google_search(user.replace("search", "").replace("google", ""))
        entry.delete(0, "end")
        return

    # AI response
    try:
        answer = ai_reply(user)
        chat_box.insert("end", f"PK AI: {answer}\n\n")
        speak(answer)
    except:
        chat_box.insert("end", "Error in AI response\n\n")

    entry.delete(0, "end")

# =========================
# BUTTONS
# =========================
send_btn = ctk.CTkButton(app, text="Send", command=send_message)
send_btn.pack(pady=5)

# =========================
# VOICE ENGINE (WAKE WORD)
# =========================
q = queue.Queue()
model = Model("vosk-model-small-en-us-0.15")
recognizer = KaldiRecognizer(model, 16000)

def callback(indata, frames, time, status):
    q.put(bytes(indata))

def listen_for_wake_word():
 with sd.RawInputStream(
    device=6,
    samplerate=16000,
    blocksize=8000,
    dtype='int16',
    channels=1,
    callback=callback
):


        chat_box.insert("end", "PK AI: Listening for 'Hey PK'...\n\n")

        while True:
            data = q.get()

            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                text = result.get("text", "")

                if "hey pk" in text.lower():
                    chat_box.insert("end", "PK AI: Yes Prakash?\n\n")
                    speak("Yes Prakash")

# =========================
# START WAKE WORD THREAD
# =========================
#threading.Thread(target=listen_for_wake_word, daemon=True).start()

# =========================
# ENTER KEY
# =========================
entry.bind("<Return>", lambda e: send_message())

# =========================
# WELCOME
# =========================
chat_box.insert("end", "PK AI: Jarvis Mode Activated\n\n")
speak("Jarvis mode activated")

# =========================
# RUN APP
# =========================
app.mainloop()