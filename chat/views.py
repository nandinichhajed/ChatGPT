from django.shortcuts import render
from .models import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import openai
import os

def chat(request):
    chats = Chat.objects.all()
    return render(request, 'chat.html', {
        'chats': chats,
    })

@csrf_exempt
def Ajax(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':

        text = request.POST.get('text')
        prompt = "A sassy and tired personal Assistant that is located in london"
        print(text)

        openai.api_key = os.environ['openai.api_key']

        res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",

        messages=[
            {"role": "user", "content": f"{text}"},
            {"role": "system", "content": f"{prompt}"}
        ],
    )

        response = res.choices[0].message["content"]
        print(response)
        
        chat = Chat.objects.create(
            text = text,
            gpt = response
        )

        return JsonResponse({'data': response,})
    return JsonResponse({})