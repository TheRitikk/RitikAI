import pyttsx3
import speech_recognition as sr
import os
import webbrowser
import openai
from config import apikey
import datetime
import ecapture as ec
import time
import wikipedia
import random
import requests
import subprocess

chatstr = ""


def chat(qs):
    global chatstr
    openai.api_key = apikey
    chatstr += f"Ritik: {qs}\n AI: "
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=chatstr,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    # todo : Wrap this inside of a try catch block
    say(response["choices"][0]["text"])
    chatstr += f"{response['choices'][0]['text']}\n"
    return response["choices"][0]["text"]


def ai(prompt):
    openai.api_key = apikey
    text = f"OpenAI response for prompt: {prompt}\n*****************************\n\n"

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=1,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    # todo : Wrap this inside of a try catch block
    print(response["choices"][0]["text"])
    text += response["choices"][0]["text"]
    if not os.path.exists("Openai"):
        os.mkdir("Openai")

    with open(f"Openai/{''.join(prompt.split('intelligence')[1:]).strip()}.txt", "w") as f:
        f.write(text)


def say(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        print("\nListening....")
        r.pause_threshold = 1  # Waiting time to take command
        audio = r.listen(source)
        try:
            print("Recognizing......")
            query = r.recognize_google(audio, language="en-in")
            # print(f"User said : {query}")
            return query

        except Exception as e:
            say("Some Error Occurred. Sorry Please try again!")
            return "None"


if __name__ == '__main__':
    print('Instruction : ')
    print("1. Need text file - using artificial intelligence")
    print("1. Reset chat - reset the cat")
    print("2. Close - close this program\n")
    say("Hello Sir, How can i help you?")
    while True:
        query = takecommand()
        # todo : add more sites
        sites = [["youtube", "https://youtube.com"], ["wikipedia", "https://wikipedia.com"],
                 ["google", "https://google.com"]]
        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                say(f"Opening {site[0]}.....")
                webbrowser.open(site[1])

        if "time" in query:
            strfTime = datetime.datetime.now().strftime("%H:%M:%S")
            say(f"The time is {strfTime}")

        elif "using artificial intelligence".lower() in query.lower():
            ai(prompt=query)

        elif "news".lower() in query.lower():
            news = webbrowser.open_new_tab("https://timesofindia.indiatimes.com/home/headlines")
            say('Here are some headlines from the Times of India,Happy reading')
            time.sleep(6)

        elif "camera" in query.lower() or "take a photo" in query.lower() or "take picture" in query.lower() or "take a picture" in query.lower():
            ec.capture(0, "frame", f"Openai/{random.randint(0,99)}img.png")

        elif "weather".lower() in query.lower():
            api_key = "Enter your api kay"
            base_url = "http://api.weatherapi.com/v1"
            say("what is the city name")
            city_name = takecommand()
            complete_url = base_url + "/current.json?key=" + api_key + "&q=" + city_name
            response = requests.get(complete_url)
            x = response.json()
            a = x.keys()
            a = list(a)
            if a[0] != "error":
                y = x["current"]
                current_temperature = y["temp_c"]
                current_humidiy = y["humidity"]
                z = x["current"]
                weather_description = z["condition"]["text"]
                say(" Temperature is " +
                      str(current_temperature) +"degree celcius" +
                      "\n humidity is " +
                      str(current_humidiy) +"percentage" +
                      "\n description  " +
                      str(weather_description))
            
            else:
                say("Some error accured.\n Please check my code and api kay,\n try again?")
        
        elif 'wikipedia' in query.lower():
            say('Searching Wikipedia...')
            statement =query.replace("wikipedia", "")
            results = wikipedia.summary(statement)
            say("According to Wikipedia")
#             print(results)
            say(results)
            
        elif "Close".lower() in query.lower():
            quit()

        elif "clear chat" in query.lower() or "reset chat" in query.lower():
            chatstr = ""
            say("Chat has been reset.")
            
        elif "log off" in query.lower() or "sign out" in query.lower():
            say("Ok , your pc will log off, make sure you exit from all applications")
            subprocess.call(["shutdown", "/l"])
            
        elif "shut down my pc" in query.lower():
            say("Ok , your pc will shut down, make sure you exit from all applications")
            subprocess.call(["shutdown", "/s"])
            
        elif "restart my pc" in query.lower():
            say("Ok , your pc will restart, make sure you exit from all applications")
            subprocess.call(["shutdown", "/r"])

        else:
            print("Chating.....")
            chat(qs=query)
