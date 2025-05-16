import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import requests
import random
import randfacts
import time
import os
import pyautogui
import webbrowser
from pathlib import Path

# Initialize Recognizer and pyttsx3 Engine
listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
try:
    engine.setProperty('voice', voices[1].id)  # Female voice
except IndexError:
    engine.setProperty('voice', voices[0].id)  # Default to first voice

# Basic talking function
def talk(text):
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()
    time.sleep(0.5)  # Prevent overlapping speech

# Listen to user's command
def listen_command():
    command = ''
    try:
        with sr.Microphone() as source:
            print("Listening...")
            listener.adjust_for_ambient_noise(source, duration=1)
            voice = listener.listen(source, timeout=6, phrase_time_limit=10)
            command = listener.recognize_google(voice)
            command = command.lower()
            print(f"You said: {command}")
            with open("command_log.txt", "a") as log:
                log.write(f"{datetime.datetime.now()}: {command}\n")
    except sr.WaitTimeoutError:
        print("Listening timed out while waiting for phrase")
        talk("I did not hear anything. Please try again.")
    except sr.UnknownValueError:
        print("Sorry, I could not understand audio")
        talk("I did not catch that. Please repeat.")
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        talk("Sorry, there seems to be a network error.")
    except Exception as e:
        print(f"Error recognizing voice: {e}")
    return command

# Play song functionality
def play_song(command):
    song = command.replace('play', '').strip()
    if song:
        talk(f"Playing {song}")
        pywhatkit.playonyt(song)
    else:
        talk("Sorry, I couldn't understand the song name.")

# Get current weather
def get_weather():
    city = "Hyderabad"
    api_key = 'cea9b5001e7972337b6f2931eb4e1d79'
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()
        if data['cod'] == 200:
            main_data = data['main']
            weather_data = data['weather'][0]
            temperature = main_data['temp']
            description = weather_data['description']
            talk(f"The current temperature in {city} is {temperature}°C with {description}.")
        else:
            talk("Sorry, I couldn't fetch the weather right now.")
    except Exception as e:
        print(f"Error fetching weather: {e}")
        talk("Error fetching weather data.")

# Motivation function
def motivate():
    quotes = [
        "The only way to do great work is to love what you do.",
        "Success is not the key to happiness. Happiness is the key to success.",
        "Believe in yourself and all that you are.",
        "The harder you work for something, the greater you'll feel when you achieve it."
    ]
    talk(random.choice(quotes))

# Fun fact function
def fun_fact():
    fact = randfacts.get_fact()
    talk(f"Did you know? {fact}")

def send_message_interactive():
    try:
        shortcut_path = str(Path.home() / "Desktop" / "WhatsApp.lnk")
        os.startfile(shortcut_path)
        talk("Opening WhatsApp Desktop...")

        time.sleep(10)

        # Loop until a valid contact name is received
        contact_name = ''
        while not contact_name:
            talk("Whom do you want to send the message to?")
            contact_name = listen_command()
            if not contact_name:
                talk("I didn't catch the contact name. Please try again.")

        talk(f"What message should I send to {contact_name}?")

        # Loop until a valid message is received
        message = ''
        while not message:
            message = listen_command()
            if not message:
                talk("I didn't catch the message. Could you repeat it?")

        # Proceed with sending message
        pyautogui.hotkey('ctrl', 'f')
        time.sleep(2)
        pyautogui.write(contact_name)
        time.sleep(3)
        pyautogui.press('down')
        time.sleep(1)
        pyautogui.press('enter')
        time.sleep(2)
        pyautogui.write(message)
        time.sleep(1)
        pyautogui.press('enter')

        talk(f"Message sent to {contact_name}!")

    except Exception as e:
        print(f"Error sending message: {e}")
        talk("Sorry, I couldn't send the message.")

# Open common websites
def open_website(command):
    websites = {
        "google": "https://www.google.com",
        "youtube": "https://www.youtube.com",
        "instagram": "https://www.instagram.com",
        "facebook": "https://www.facebook.com",
        "twitter": "https://www.twitter.com",
        "github": "https://www.github.com",
        "chrome": "https://www.google.com/chrome/"
    }
    for name in websites:
        if name in command:
            talk(f"Opening {name}")
            webbrowser.open(websites[name])
            return
    talk("Sorry, I couldn't recognize the website name.")

# Main assistant function (run_alexa)
def run_assistant():
    while True:
        command = listen_command()
        print(f"Command: {command}")

        if not command:
            talk("I didn't hear anything. Please try again.")
            continue

        if command.startswith('alexa'):
            command = command.replace('alexa', '', 1).strip()

            if 'play' in command:
                play_song(command)
            elif 'time' in command:
                time_now = datetime.datetime.now().strftime('%I:%M %p')
                talk(f"The current time is {time_now}")
            elif 'who is' in command:
                person = command.replace('who is ', '')
                try:
                    info = wikipedia.summary(person, sentences=1)
                    talk(info)
                except Exception as e:
                    talk("Sorry, I couldn't find any information on that person.")
            elif 'weather' in command:
                get_weather()
            elif 'motivate me' in command:
                motivate()
            elif 'tell a fun fact' in command:
                fun_fact()
            elif 'send a message' in command:
                send_message_interactive()
            elif 'joke' in command:
                talk(pyjokes.get_joke())
            elif 'open' in command:
                open_website(command)
            elif 'stop' in command or 'exit' in command:
                talk("Goodbye!")
                exit()
            else:
                talk("Sorry, I didn't understand the command. Please repeat.")
        else:
            talk("Please say 'Alexa' followed by your command.")

# Start
def greet():
    hour = datetime.datetime.now().hour
    if hour < 12:
        talk("Good morning! What can I do for you?")
    elif 12 <= hour < 18:
        talk("Good afternoon! What can I do for you?")
    else:
        talk("Good evening! What can I do for you?")

greet()

while True:
    run_assistant()
    time.sleep(2)
