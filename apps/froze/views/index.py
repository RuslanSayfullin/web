from django.shortcuts import render


def index(request):
    return render(request, 'froze/index.html')


def receiver(request):
    return render(request, 'froze/_receiver.html')
