import time
import math
from moviepy.editor import *
import azure.cognitiveservices.speech as speechsdk
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

def Mp4ToMp3(input_file, output_file):
    video = VideoFileClip(input_file)
    video.audio.write_audiofile(output_file)

def ta_authenticate_client():
    key = "REMOVED"
    endpoint = "https://REMOVED.cognitiveservices.azure.com/"

    ta_credential = AzureKeyCredential(key)
    text_analytics_client = TextAnalyticsClient(
            endpoint=endpoint, 
            credential=ta_credential)
    return text_analytics_client

'''
Speech2Text(input_file)

Arg
- input_file: 입력 동영상

Return
- results: 입력 동영상에 포함된 말들을 인식한 결과(result)들을 list로 저장
    - reult
        - timestr: HH:MM:SS 형태로 저장된 텍스트 시작시간
        - seconds: 초로 저장된 텍스트 시작시간
        - text: 결과로 반환된 텍스트
'''

def Speech2Text(speech_key, service_region, input_file, output_file):
    Mp4ToMp3(input_file, output_file)

    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    audio_config = speechsdk.audio.AudioConfig(filename=output_file)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    # text analaytics client
    ta_client = ta_authenticate_client()

    time_unit = 1e-7
    results = []

    done = False
    while not done:
        result = speech_recognizer.recognize_once()
        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            temp = {
                "timestr": time.strftime('%H:%M:%S', time.gmtime(math.floor(result.offset * time_unit))),
                "seconds": math.floor(result.offset * time_unit),
                "text": result.text,
                "ket_phrases": Text2KeyPhrases(ta_client, [result.text]),
            }
            print("Recognized: {}".format(result.text))
            results.append(temp)
        elif result.reason == speechsdk.ResultReason.NoMatch:
            print("No speech could be recognized: {}".format(result.no_match_details))
            done = True
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print("Speech Recognition canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("Error details: {}".format(cancellation_details.error_details))
            done = True
    
    return results

def Text2KeyPhrases(client, documents):
    phrases = []
    try:
        # documents = ["My cat might need to see a veterinarian."]
        response = client.extract_key_phrases(documents = documents)[0]
        if not response.is_error:
            print("Key Phrases:")
            for phrase in response.key_phrases:
                phrases.append(phrase)
                print("\t", phrase)
        else:
            print(response.id, response.error)
    except Exception as err:
        print("Encountered exception. {}".format(err))
    
    return phrases
        

# Example
if __name__ == "__main__":
    speech_key, service_region = "REMOVED", "koreacentral"
    results = Speech2Text(speech_key, service_region, "out.mov", "out.wav")