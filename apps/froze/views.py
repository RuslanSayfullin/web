from django.shortcuts import render

from apps.froze.models import Froze


def index(request):
    return render(request, 'froze/index.html')
