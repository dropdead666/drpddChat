import json

from django.contrib.sessions import serializers
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from .models import Message
import datetime
from django.core.serializers.json import DjangoJSONEncoder

def main(request):
    messages = Message.objects.all()
    return render(request, 'index.html', {'messages': messages})


def create_message(request):
    if request.method == 'POST':
        message_text = request.POST.get('the_message')
        response_data = {}

        message = Message(text=message_text, author=request.user)
        message.publish()

        response_data['result'] = 'Create message successful!'
        response_data['message_pk'] = message.pk
        response_data['text'] = message.text
        response_data['created'] = datetime.datetime.now()
        response_data['author'] = message.author.username

        return HttpResponse(
            json.dumps(
                response_data,
                sort_keys=True,
                indent=1,
                cls=DjangoJSONEncoder
            ),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )

