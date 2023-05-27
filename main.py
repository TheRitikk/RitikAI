import pyttsx3
import speech_recognition as sr
import os
import webbrowser
import openai
from config import apikey
import datetime

chatstr = ""


def chat(query):
    global chatstr
    openai.api_key = apikey
    chatstr += f"Ritik: {query}\n AI: "
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


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1 #Waiting time to take command
        audio = r.listen(source)
        try:
            print("Recognizing......")
            query = r.recognize_google(audio, language="en-in")
            # print(f"User said : {query}")
            return query
        except Exception as e:
            return "Some Error Occurred. Sorry Please try again!"


if __name__ == '__main__':
    print('Instruction : ')
    print("1. Need text file - using artificial intelligence")
    print("1. Reset chat - reset the cat")
    print("2. Close - close this program\n\n")
    say("Hello Sir, How can i help you?")
    while True:
        print("\nListening....")
        query = takeCommand()
        # todo : add more sites
        sites = [["youtube", "https://youtube.com"], ["wikipedia", "https://wikipedia.com"],
                 ["google", "https://google.com"]]
        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                say(f"Opening {site[0]}e.....")
                webbrowser.open(site[1])

        if "the time" in query:
            strfTime = datetime.datetime.now().strftime("%H:%M:%S")
            say(f"The time is {strfTime}")

        elif "using artificial intelligence".lower() in query.lower():
            ai(prompt=query)

        elif "Close".lower() in query.lower():
            quit()

        elif "reset chat".lower() in query.lower():
            chat += ""

        else:
            print("Chating.....")
            chat(query)
