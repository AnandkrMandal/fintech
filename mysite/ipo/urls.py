from django.urls import path ,include # type: ignore
from ipo import views
from .views import  CustomLoginView, GoogleLogin,  IPOListView, IPOListCreateView, IPODetailView , IPODeleteView
from django.conf import settings # type: ignore
from django.conf.urls.static import static # type: ignore

from rest_framework_simplejwt.views import ( TokenRefreshView, TokenVerifyView)  # type: ignore



urlpatterns = [

    # login page
    path('user/login/', views.login , name='userlogin'),
    # signup page
    path('user/signup/', views.signup , name='usersignup'),
    #foget password
    path('user/forget_password/', views.forgetpassword , name='forgetpassword'),
    # ipo page
    path('upcoming/ipo', views.ipo, name='ipo'),
    #user dashboard
    path('user-dashboard/', views.Userdashboard, name='UserDashboard'),
    #user dashboard
    path('admin-dashboard/', views.admindashboard, name='AdminDashboard'),


    # django rest auth urls
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),
    path('api/auth/customlogin/', CustomLoginView.as_view(), name='custom_login'),
    path('api/rest/auth/', include('dj_rest_auth.urls')),
    path('accounts/', include('allauth.urls')),
    path('api/v1/rest/auth/', include('django.contrib.auth.urls')),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'), 
    path('api/auth/google/', GoogleLogin.as_view(), name='google_login'),
  
     
    #ipo api urls
    path('api/ipos/data/', IPOListView.as_view(), name='ipos_data'),
    path('api/ipos/',IPOListCreateView.as_view(), name='ipo-list-create'),
    path('api/ipos/<int:pk>', IPODetailView.as_view(), name='ipo-detail'),
    path('api/ipos/<int:pk>/delete', IPODeleteView.as_view(), name='ipo-delete'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)