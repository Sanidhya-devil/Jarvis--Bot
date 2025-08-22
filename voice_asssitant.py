import speech_recognition as sr
import pyttsx3
from datetime import datetime
import wikipedia

# Initialize text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    """Speak the given text"""
    engine.say(text)
    engine.runAndWait()

def get_time():
    """Get and speak current time"""
    time = datetime.now().strftime("%I:%M %p")
    speak(f"The current time is {time}")
    print(f"Current time: {time}")

def search_wikipedia(query):
    """Search Wikipedia and speak result"""
    try:
        result = wikipedia.summary(query, sentences=2)
        speak(result)
        print(result)

    except wikipedia.exceptions.DisambiguationError:
        speak("There are multiple results. Please be more specific.")
        print("Disambiguation Error: Multiple results found.")

    except wikipedia.exceptions.PageError:
        speak("Sorry, I could not find any results for your query.")
        print("PageError: No page found.")

def recognize_speech():
    """Recognize speech from microphone"""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print(f"User said: {text}")
        return text.lower()
    except sr.UnknownValueError:
        print("Sorry, I could not understand.")
        speak("Sorry, I could not understand.")
        return None
    except sr.RequestError:
        print("Could not connect to Google Speech Recognition.")
        speak("Could not connect to Google Speech Recognition.")
        return None

# Main program loop
speak("Hello! How can I assist you today?")

while True:
    command = recognize_speech()

    if command:
        if "time" in command:
            get_time()
        elif "wikipedia" in command:
            speak("What should I search on Wikipedia?")
            query = recognize_speech()
            if query:
                search_wikipedia(query)
        elif "exit" in command or "quit" in command or "stop" in command:
            speak("Goodbye! Have a nice day.")
            print("Assistant stopped.")
            break
        else:
            speak("Sorry, I can only tell time or search Wikipedia right now.")
            print("Unrecognized command.")
