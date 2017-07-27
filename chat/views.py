from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login

from .models import Room
from .forms import RegistrationForm


def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect(reverse('chat_room'))
    else:
        form = RegistrationForm
    return render(request, "registration/registration.html", {'form': form})


def chat_room(request):
    room, created = Room.objects.get_or_create(label='chat')
    messages = reversed(room.messages.order_by('-timestamp')[:50])

    return render(request, "room.html", {
        'room': room,
        'messages': messages,
    })
