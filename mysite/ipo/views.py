from rest_framework import generics
from .models import IPO
from .serializers import IPOSerializer , CustomLoginSerializer
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated 
from .permissions import IsAdminUser

# from dj_rest_auth.views import LoginView 
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter # type: ignore
from allauth.socialaccount.providers.oauth2.client import OAuth2Client # type: ignore
from dj_rest_auth.registration.views import SocialLoginView # type: ignore
from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken # type: ignore
from rest_framework import serializers

#auth
from rest_framework.permissions import AllowAny


def ipo(request):
    return render(request, 'ipo.html')

def login(request):
    return render(request, 'registration/login.html')

def signup(request):
    return render(request, 'registration/signup.html')

def forgetpassword(request):
    return render(request, 'registration/forget_password.html')

def Userdashboard(request):
    return render(request, 'user/dashboard.html')

def admindashboard(request):
    return render(request, 'admin/dashboard.html')


class CustomLoginView(APIView):
    permission_classes = ()
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = CustomLoginSerializer(data=request.data, context={'request': request})
        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError as e:
             return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.validated_data['user']
        is_admin = serializer.validated_data['is_admin']

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        # Conditional response based on is_admin
        response_data = {
            'access_token': access_token,
            'refresh_token': refresh_token,
        }

        if is_admin:
            response_data['is_admin'] = is_admin

        return Response(response_data, status=status.HTTP_200_OK)
    



class GoogleLogin(SocialLoginView): 
    adapter_class = GoogleOAuth2Adapter
    callback_url =  'http://127.0.0.1:8000/account/dashboard'
    client_class = OAuth2Client


class IPOListView(generics.ListAPIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    queryset = IPO.objects.all()
    serializer_class = IPOSerializer

class IPOListCreateView(generics.ListCreateAPIView):
    queryset = IPO.objects.all()
    serializer_class = IPOSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

class IPODetailView(generics.RetrieveUpdateAPIView):
    queryset = IPO.objects.all()
    serializer_class = IPOSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

class IPODeleteView(generics.RetrieveDestroyAPIView):
    queryset = IPO.objects.all()
    serializer_class = IPOSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


