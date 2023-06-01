from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from django.contrib.auth.models import User
from apps.api.serializer import FrozeSerializer, UserSerializer
from apps.dogovora.models import DogovorIndi, DogovorEntry


class FrozeAPICreate(generics.CreateAPIView):
    """Первый вариант"""
    serializer_class = FrozeSerializer


class FrozeAndDogovorIndiView(APIView):
    """Получаем JSON и создаем пару Заявка/ДоговорФЛ"""
    def post(self, request):
        froze_serializer = FrozeSerializer(data=request.data)
        if froze_serializer.is_valid():
            froze = froze_serializer.save()
            DogovorIndi.objects.create(froze=froze, )
            DogovorEntry.objects.create(froze=froze, )
            return Response({'status': 'success'}, status=status.HTTP_201_CREATED)
        return Response(froze_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)


