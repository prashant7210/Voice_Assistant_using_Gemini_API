import speech_recognition as sr
import pyttsx3
import requests
import webbrowser
import json
from config import apikey, weatherapi
import google.generativeai as genai
import pyautogui
from colorama import Fore, Style, init

init(autoreset=True)
engine = pyttsx3.init()

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("\r" + Fore.BLUE + "Listening...", end="", flush=True)
        try:
            audio = recognizer.listen(source, timeout=None)
            print("\r" + Fore.WHITE + "Recognizing...", end="", flush=True)
            text = recognizer.recognize_google(audio)

            print("\n" + Fore.GREEN + f"You said: {text}", flush=True)
            print(Style.RESET_ALL, end="", flush=True)
            return text.lower()
        except sr.UnknownValueError:
            print("\r" + Fore.RED + "Sorry, I did not understand that.", flush=True)
            print(Style.RESET_ALL, end="", flush=True)
            speak("Sorry, I did not understand that.")
            return recognize_speech()
        except sr.RequestError:
            print("\r" + Fore.RED + "Request error from Google Speech Recognition service.", flush=True)
            print(Style.RESET_ALL, end="", flush=True)
            speak("\r" + "Request error from Google Speech Recognition service.")
            return ""

def speak(text):
    engine.say(text)
    engine.runAndWait()

def open_application(app_name):
    pyautogui.press("super")
    pyautogui.typewrite(app_name)
    pyautogui.sleep(1)
    pyautogui.press("enter")

def get_weather(city):
    api_key = weatherapi
    base_url = f"https://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"
    response = requests.get(base_url)
    weather_data = json.loads(response.text)

    if "error" in weather_data:
        temperature = "City Not Found!"
    else:
        temperature = str(weather_data["current"]["temp_c"]) + "degree celcius"
    return temperature

def open_website(website):
    if "google" in website:
        webbrowser.open("https://www.google.com")
    elif "youtube" in website:
        webbrowser.open("https://www.youtube.com")
    elif "facebook" in website:
        webbrowser.open("https://www.facebook.com")
    elif "superset" in website:
        webbrowser.open("https://app.joinsuperset.com/students")
    elif "leetcode" in website:
        webbrowser.open("https://leetcode.com/problemset/")
    else:
        speak("Website not available in the list.")

def ai(prompt):
    genai.configure(api_key=apikey)
    model = genai.GenerativeModel("gemini-1.5-flash")

    response = model.generate_content(prompt)
    new_res = response.text
    new_res = new_res.replace("*", "")
    new_res = new_res.replace("#", "")

    print(new_res)
    return new_res


def image_info(image):
    genai.configure(api_key=apikey)
    myfile = genai.upload_file(image)

    model = genai.GenerativeModel("gemini-1.5-flash")
    result = model.generate_content(
        [myfile, "\n\n", "Can you tell me about the instruments in this photo?"]
    )

    return str(result.text)


def main():
    print(Fore.CYAN + "Prashant's A.I , How can I help you?")
    speak("Prashant's A..I , How can I help you?")
    while True:
        command = recognize_speech()
        if "open" in command:
            app_or_website = command.replace("open ", "")
            if any(keyword in app_or_website for keyword in ["google", "youtube", "facebook", "superset", "leetcode"]):
                open_website(app_or_website)
            else:
                open_application(app_or_website)
        elif "temperature" in command:
            city = command.replace("temperature in ", "")
            weather_info = get_weather(city)
            speak(weather_info)
        elif "exit" in command or "quit" in command:
            print(Fore.MAGENTA + "Goodbye!, Have a Nice Day")
            speak("Goodbye!, Have a Nice Day")
            break
        elif "image" in command:
            image = "instrument.jpg"
            description = image_info(image)
            speak(description)
        else:
            text = ai(command)
            if "write" in command:
                print("\r" + Fore.YELLOW + text, flush = True)
            else:
                speak(text)


if __name__ == "__main__":
    main()