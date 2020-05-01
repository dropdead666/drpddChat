import json

from django.shortcuts import redirect
from django.http import HttpResponse
from django.shortcuts import render
from .models import Message
import datetime
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth import logout
from .forms import RegisterForm
from django.contrib.auth.models import User


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']

        context = {'form': form,
                    'username': username,
                    'password1': password1,
                    'password2': password2,
                    'email': email}

        if form.is_valid():
            form.save()
            return redirect('/')

    else:
            form = RegisterForm()
            context = {'form': form}
    return render(request, 'registration/register.html', context)


def logout_view(request):
    request.user.profile.is_online = False
    request.user.save()
    logout(request)
    return redirect('login')


def main(request):
    if request.user.is_authenticated:
        online = []
        offline = []
        request.user.profile.is_online = True
        request.user.profile.last_seen = datetime.datetime.now()
        request.user.save()
        for user in User.objects.all():
            if datetime.datetime.now() - user.profile.last_seen > datetime.timedelta(seconds=300):
                user.profile.is_online = False
            if user.profile.is_online:
                online.append(user)
            else:
                offline.append(user)
        messages = Message.objects.all()
        return render(request, 'index.html', {'messages': messages, 'users_online': online, 'users_offline': offline})
    else:
        return redirect('login')


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