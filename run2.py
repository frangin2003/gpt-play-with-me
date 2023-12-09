import pyttsx3
import speech_recognition as sr

def say(text):
    # text to speech
    
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    for voice in voices:
        print(voices)
    voice = engine.getProperty('voices')[0] # the english voice
    # voice = engine.getProperty('voices')[3] # the french voice
    engine.setProperty('voice', voice.id)
    engine.say(text)
    engine.runAndWait()
    engine.stop()

def transcribe_sr(filename):
    # speech recognition
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
    try:
        # language="en-US"
        # return recognizer.recognize_google(audio, language="fr-FRA", show_all=True)
        return recognizer.recognize_google(audio, show_all=True)
    except:
        print("Skipping unknown error")

def generate_response(prompt):
    # return agent.run(prompt)
    # print(memory.buffer)
    # return conversational_agent.run(input=prompt)
    return prompt

def start_speech_recog():
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))
    filename = "input.wav"
    while True:
        print("Say something")
        # with sr.Microphone(device_index=1) as source:
            # recognizer = sr.Recognizer()
            # recognizer.adjust_for_ambient_noise(source)
            # audio = recognizer.listen(source)

            # try:
            #     transcription = recognizer.recognize_google(audio)
            #     # if transcription.lower() == "morgan":
            #         # record audio
            #         filename = "input.wav"
            #         print("Ask me anything")
        with sr.Microphone(device_index=3) as source:
            recognizer = sr.Recognizer()
            recognizer.adjust_for_ambient_noise(source)
            source.pause_threshold = 1
            audio = recognizer.listen(source, phrase_time_limit=None, timeout=None)
            with open("input.wav", "wb") as f:
                f.write(audio.get_wav_data())
        result = transcribe_sr(filename)
        if result:
            if 'language' in result:
                detected_lang = result['language']
                print(f"Detected Language: {detected_lang}")
            else:
                print("Language detection failed.")

            if 'alternative' in result:
                alternatives = result['alternative']
                for alternative in alternatives:
                    transcript = alternative['transcript']
                    print(f"Transcript: {transcript}")
                    confidence = alternative.get('confidence')  # Check if confidence is provided
                    if confidence is not None:
                        print(f"Confidence: {confidence}")
                        response = generate_response(transcript)
                        say(response)
                    else:
                        print("Confidence not available.")
            else:
                print("Speech recognition failed.")
            # except Exception as e:
            #     print(f"Error: {e}")

