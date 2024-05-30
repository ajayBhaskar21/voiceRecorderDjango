import speech_recognition as sr
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def home(request):
    return render(request, 'home.html')

@csrf_exempt  # Add this line to exempt the view from CSRF verification for testing
def convert_audio_to_text(request):
    if request.method == 'POST' and 'audio_data' in request.FILES:
        recognizer = sr.Recognizer()
        audio_file = request.FILES['audio_data']
        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio_data)
                return JsonResponse({'text': text})
            except sr.UnknownValueError:
                return JsonResponse({'error': 'Could not understand audio'}, status=400)
            except sr.RequestError:
                return JsonResponse({'error': 'Could not request results'}, status=500)
    return JsonResponse({'error': 'Invalid request'}, status=400)
