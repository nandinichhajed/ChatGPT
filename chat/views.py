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
        prompt = "A smart personal Assistant that is located in India"
        print(text)

        openai.api_key = os.environ['openai.api_key']
        
        # create list for messages
        messages = []
        messages.append({"role": "system", "content": f"{prompt}"})
        
        def CustomChatGPT():
            messages.append({"role": "user", "content": f"{text}"})
            res = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
            )
        
            response = res.choices[0].message["content"]
            messages.append({"role": "assistant", "content": f"{response}"})
            
            chat = Chat.objects.create(
            text = text,
            gpt = response
        )
            
            print(messages)
            # print(response)
            return response
        


        return JsonResponse({'data': CustomChatGPT(),})
    return JsonResponse({})