import speech_recognition as sr
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import subprocess
import os
from django.conf import settings


def home(request):
    return render(request, 'speech/home.html')


@csrf_exempt
def convert_audio_to_text(request):
    if request.method == 'POST' and 'audio_data' in request.FILES:
        audio_file = request.FILES['audio_data']

        # Ensure media directory exists
        media_directory = settings.MEDIA_ROOT
        if not os.path.exists(media_directory):
            os.makedirs(media_directory)

        # Save the uploaded webm file
        webm_path = os.path.join(media_directory, 'speech.webm')
        with open(webm_path, 'wb') as f:
            for chunk in audio_file.chunks():
                f.write(chunk)

        # Convert webm to wav
        wav_path = os.path.join(media_directory, 'speech.wav')
        convert_command = f"ffmpeg -i {webm_path} -acodec pcm_s16le -ar 16000 {wav_path}"
        subprocess.run(convert_command, shell=True)

        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_path) as source:
            audio_data = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio_data)
                return JsonResponse({'text': text})
            except sr.UnknownValueError:
                return JsonResponse({'error': 'Could not understand audio'}, status=400)
            except sr.RequestError:
                return JsonResponse({'error': 'Could not request results'}, status=500)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request'}, status=400)
