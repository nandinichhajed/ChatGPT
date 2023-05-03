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

# create list for messages
messages = []
prompt = "You are a hotel assistant for Wynn Las Vegas and answer all the queries asked by guests. Your task is to assist the guest and make their stay luxurious and memorable, while constantly asking questions before you answer to better grasp what the guest is looking for. Add a welcome letter of for the guest in every new conversation."

messages.append({"role": "system", "content": f"{prompt}"})


@csrf_exempt
def Ajax(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        text = request.POST.get('text')
        print(text)

        openai.api_key = os.environ['openai.api_key']

        messages.append({"role": "user", "content": f"{text}"})
        res = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature = 0.7,
        )

        response = res.choices[0].message["content"]
        messages.append({"role": "assistant", "content": f"{response}"})

        chat = Chat.objects.create(
            text=text,
            gpt=response
        )
        print(messages)

        return JsonResponse({'data': response})
    return JsonResponse({})
