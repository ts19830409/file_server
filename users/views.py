from rest_framework import generics
from rest_framework.permissions import AllowAny

from users.models import User
from users.serializers import UserSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings

from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.shortcuts import redirect
from django.shortcuts import redirect, render

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class UserDetailView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

class ContactView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        email = request.data.get('email')
        message = request.data.get('message')
        send_mail(
            subject=f'Сообщение от {email}',
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.DEFAULT_FROM_EMAIL],
            fail_silently=False,
        )
        return Response({'ok': True})


def login_view(request):
    if request.method == 'POST':
        login_name = request.POST.get('login')
        password = request.POST.get('password')
        user = authenticate(request, username=login_name, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('/files/')
    return render(request, 'login.html')


def logout_view(request):
    auth_logout(request)
    return redirect('/login/')