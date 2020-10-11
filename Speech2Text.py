# azure-ai-textanalytics azure-cognitiveservices-speech moviepy

__all__ = ['Speech2Text']

import tempfile
import time
import math
from moviepy.editor import VideoFileClip
import azure.cognitiveservices.speech as speechsdk
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential


def Text2KeyPhrases(client, documents):
    phrases = []
    try:
        response = client.extract_key_phrases(documents = documents)[0]
        if not response.is_error:
            #print("Key Phrases:")
            for phrase in response.key_phrases:
                phrases.append(phrase)
                #print("\t", phrase)
        else:
            pass
            #print(response.id, response.error)
    except Exception as err:
        print("Encountered exception. {}".format(err))
    
    return phrases


'''
Speech2Text(input_file)

Arg
- input_file: 입력 동영상

Return
- results: 입력 동영상에 포함된 말들을 인식한 결과(result)들을 list로 저장
    - result
        - timestr: HH:MM:SS 형태로 저장된 텍스트 시작시간
        - seconds: 초로 저장된 텍스트 시작시간
        - text: 결과로 반환된 텍스트
'''
def Speech2Text(input_file, config):
    # Make tempfile for extracted audio
    tf = tempfile.NamedTemporaryFile(suffix='.wav')
    
    # Extract audio from video
    video = VideoFileClip(input_file)
    video.audio.write_audiofile(tf.name)
    
    # Build speech recognizer
    speech_key = config.get('AZURE_SPEECH_KEY', '')
    region = config.get('AZURE_REGION', 'koreacentral')
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=region)
    audio_config = speechsdk.audio.AudioConfig(filename=tf.name)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    
    # Build text analaytics client
    ta_key = config.get('AZURE_TEXT_ANALYSIS_KEY', '')
    endpoint = config.get('AZURE_ENDPOINT', '')
    ta_credential = AzureKeyCredential(ta_key)
    ta_client = TextAnalyticsClient(endpoint=endpoint, credential=ta_credential)
    
    # Loop to get transcription and key phrases
    time_unit = 1e-7
    results = []
    while True:
        result = speech_recognizer.recognize_once()
        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            row = {
                "timestr": time.strftime('%H:%M:%S', time.gmtime(math.floor(result.offset * time_unit))),
                "seconds": math.floor(result.offset * time_unit),
                "text": result.text,
                "key_phrases": Text2KeyPhrases(ta_client, [result.text]),
            }
            #print("Recognized: {}".format(result.text))
            results.append(row)
        elif result.reason == speechsdk.ResultReason.NoMatch:
            #print("No speech could be recognized: {}".format(result.no_match_details))
            break
        elif result.reason == speechsdk.ResultReason.Canceled:
            #cancellation_details = result.cancellation_details
            #print("Speech Recognition canceled: {}".format(cancellation_details.reason))
            #if cancellation_details.reason == speechsdk.CancellationReason.Error:
            #    print("Error details: {}".format(cancellation_details.error_details))
            break
    
    return results


# Example
if __name__ == "__main__":
    results = Speech2Text("out.mov")