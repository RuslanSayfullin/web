from django.shortcuts import render
from rest_framework import generics

from apps.api.serializer import FrozeSerializer


class FrozeAPICreate(generics.CreateAPIView):
    serializer_class = FrozeSerializer
