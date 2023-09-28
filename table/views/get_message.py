from django.views.decorators.csrf import csrf_exempt
from table.backendAndTelegram.telegram import requests_list
from django.shortcuts import HttpResponse
import json


@csrf_exempt
def get_message(request):
    '''URL to get data(from request) from Telegram server'''
    print('\n\nCOME HERE НАХУЙn\n\n')
    try:
        if request.method == 'POST':
            formatted_request = HttpResponse(request).content.decode('utf-8')
            formatted_request = json.loads(formatted_request)
            message = formatted_request['message']['text']
            chat_id = formatted_request['message']['chat']['id']
            requests_list(message, chat_id)
            return HttpResponse(status=200)
    except Exception as ex:
        return HttpResponse("Bot Don't Work, Look At views.get_message."
                            f"Exception: {ex}")
