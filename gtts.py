from gtts import gTTS

text = "Hello, this is a sample text to convert to speech."
tts = gTTS(text=text, lang='en')
tts.save("output.mp3")
