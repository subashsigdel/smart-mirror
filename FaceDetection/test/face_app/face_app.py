import face_recognition
import cv2
import numpy as np
import json
import os
from PIL import Image
import threading
import time
from datetime import datetime
from playsound import playsound
from pydub import AudioSegment

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "voice-assistant-319108-af676312c70d.json"

credentials = {
  "type": "service_account",
  "project_id": "voice-assistant-319108",
  "private_key_id": "af676312c70d8378f715bf78c3e0cf62a8a70666",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDgnrijnsxZUdF8\njrflz2OyFLomCJldqUUl9QgK7fZo40RlWgdcMEbknuQGHd24h6VbT+TlUYCNpi3U\nzql0tynYFBNeAHrLxA/24U6Rq7PmKbICDpJ6wUidkY3E2oD9dH9VOcA2yZBJ6GGx\nDh9QraS4rcRa0ZbPxzknlb+8uIsoRkK43IBZW5MJnGbLegYh0VdGrOUuu8ERuOiS\nvDNzzCK5dIxFIEAAXvBXU2hufMlTWzMrJs7Zq6sUvW5GXY1sY0wbQFylflqeDg1V\nHpM990esPU1UCJPBQH69TaUxeDLOIZq5z7Pdqn+5Spo++jCfa2hIYJoiBYliGsZi\nijpM2R6xAgMBAAECggEAIM4dkkv5dVwVN9dSNV6WJWaQj0h3Oa4kmrgQLiR19fin\nPxQoegbU+8PW8qu++5nYBR+EgxdlqopoLCnoptKvak74SyTPyl2+pSRfyLemhQl2\n5YUCUKpU9CpTZbox15KBnE1cbMQAbkLhra2t1iceJRi/0jHFEGB80PK2d5YOQNnH\n8FImSt8Y8mmBFtpc53gct8fqEpLUzvpiLry4eE9HmD7hbcHl6XH7fh9g/cDxQMgf\nR4oZASrTTLhb0Hjeg9dOYQwENJA7hj0LsfVeA8rUKOPNO1fK12I/vP6y90oBTTuY\nugGTc1HboVqqlLNUD4chWptnPPbdoJZZ0xXmpWQyVwKBgQD+HJBRC5BDRDwqibBn\nLFh/gsYlNr7h0n7/5534o0qt5l42w8DAq45seDyGdVwiTjrF8bb+rBFuNGeuFwzI\nzFX8wiohzbJU8bo1YAPayW5R3TXMrkghedzanEA/lKOBuZQ/6Ie/6oghlUlBLMSm\npeEpkmTlJNkIaw6fYWCIBYqsUwKBgQDiSg0TC80bw1TGT4XhL8ctVCqHQQU/KdnY\nlz+TmOTY6F1JYr1zqSyoMJaNUXwmig7W6DnCGkUGlKBAP+E5U3grAQc388ZnNBa0\nLzjPgY0X/2n6cfiAUNrbxI1/jn7muf4hccawue31zG5CeWlJHpCZrmg/Jjnth1D8\nWKSrK22IawKBgQCiZmblJNrB4q4BEZYnmfPFKjKwPdioQfrgWYpgCRwFH6E+psRd\nXkbbk8w6sm57jjuJnf0xrY5GPD+2xwxomA6sRvreN7OtDf/PdNmBzhIvR4zGjuuS\nWWuIWyvEdp44nf3dCiMXyC/QJrR2bsIPLxxDkUfiGjaKZsElovoqdEA3+QKBgCgQ\nOj5cAYVf0NuHasmSnu3sj9cAcQBc1X/eT1g/YozwnsuGWspmckyYxZ7hhVyBZt0v\nokI2SnA+0hxt8t8mYwkiFngWhdLxyu89yQ4b/rH3+3hmwztclVMBepfRz6/j0BV1\nwlq5oGK7Pe4w9q4GZk1/Ll+30du28GStAQJ5HtxfAoGBAKjRJAB+eQ5SXmnQlZDG\nZqloPsK/CIG2gG0gQq3IPAs0gWR/vuCt6pP78MGGb1w7JSvAnP7rBp/GwO4xWqtR\nSIR9Hg4PZPFu6Oplgr5IFbQhGFEqnsT9ZXR31clnTEB9ypXnwT0uVCHQyXaTFqg/\nsFfq6UWF3FdQiTuiyK57be+T\n-----END PRIVATE KEY-----\n",
  "client_email": "voice-assistant@voice-assistant-319108.iam.gserviceaccount.com",
  "client_id": "117202096327498252251",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/voice-assistant%40voice-assistant-319108.iam.gserviceaccount.com"
}


def encode_photo():
    """encodes photo and save to data.json"""
    print('Begining encoding')
    if os.path.getsize('data.json') != 0:
        with open('data.json') as json_file:
            jsonData = json.load(json_file)
    newData = []
    for i, cl in enumerate(myList):
        found = False
        for data in jsonData:
            if cl.split('.')[0] in data['name']:
                found = True

        if not found:
            data = {}
            curImg = cv2.imread(f'{path}/{cl}')
            images.append(curImg)
            img = cv2.cvtColor(curImg, cv2.COLOR_BGR2RGB)
            encodes = face_recognition.face_encodings(img)
            if encodes:
                encode = encodes[0]
                data['name'] = cl.split('.')[0]
                data['encoding'] = encode.tolist()
                data['i'] = i
                nepali_name = input(f'Enter nepali name for {data["name"]}====> ')
                data['nepali_name'] = nepali_name
                for nep_word,eng_word in zip(data['nepali_name'].split(' '),data['name'].split(' ')):
                    if not eng_word+'.mp3' in voices:
                        save_sound(eng_word,nep_word)
                newData.append(data)
            else:
                print(f"Couldnot find face in {path}/{cl}")
    jsonData = jsonData+newData
    with open('data.json', 'w') as outfile:
        json.dump(jsonData, outfile)
    print('Encoding has been completed')
    return jsonData

def recognize_face(known_face_encodings,known_face_names,jsonData):
    print('Begining face recognition')
    cap = cv2.VideoCapture(0)
    while True:
        for data in recognized_face_name:
            if (datetime.now()-data['time']).seconds>60:
                recognized_face_name.remove(data)
        
        # Grab a single frame of video
        ret, frame = cap.read()
        rgb_frame = frame[:, :, ::-1]

        # Find all the faces and face enqcodings in the frame of video
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        print(face_locations)
        # Loop through each face in this frame of video
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(
                known_face_encodings, face_encoding)
            name = "Unknown"
            # the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(
                known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
                if not search_dictionaries('i',best_match_index,recognized_face_name):
                    recognized_face_name.append({'i':best_match_index,'name':name,'time':datetime.now()})
                    nepali_name = search_dictionaries('i',best_match_index,jsonData)['nepali_name']
                    print(f'{name} has been recognized')
                    if not f'{name.split(" ")[0]}.mp3' in voices:
                        save_sound(name.split(" ")[0],f'नमस्ते {nepali_name.split(" ")[0]} जी')
                    playsound(f'voices/{name.split(" ")[0]}.mp3')
                    playsound('C:/Users/HTP/Desktop/face_app/voices/welcome_museum.mp3')
                    time.sleep(1)

def save_sound(eng_word,nep_word):
    """Synthesizes speech from the input string of text."""
    from google.cloud import texttospeech

    client = texttospeech.TextToSpeechClient()
    input_text = texttospeech.SynthesisInput(text=nep_word)

    # Note: the voice can also be specified by name.
    # Names of voices can be retrieved with client.list_voices().
    voice = texttospeech.VoiceSelectionParams(
        language_code="hi-IN",
        name="hi-IN-Wavenet-D",
        # ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    
    response = client.synthesize_speech(
        request={"input": input_text, "voice": voice,
                 "audio_config": audio_config}
    )

    # The response's audio_content is binary.
    with open(f"voices/{eng_word}.mp3", "wb") as out:
        out.write(response.audio_content)
        out.close()
    # playsound(f'voices/{text}.mp3')
            

def search_dictionaries(key, value, list_of_dictionaries):
    for data in list_of_dictionaries:
        if data[key] == value:
            return data
    return None

if __name__ == '__main__':
    path = 'image'
    images = []
    classNames = []
    myList = os.listdir(path)
    encodeList = []
    recognized_face_name = []
    voices = os.listdir('voices')
    jsonData = encode_photo()
    # Create arrays of known face encodings and their names
    known_face_encodings = [data['encoding'] for data in jsonData]
    known_face_names = [data['name'] for data in jsonData]
    recognize_face(known_face_encodings,known_face_names,jsonData)
