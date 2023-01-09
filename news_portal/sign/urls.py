from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import BaseRegisterView, upgrade_me, recipients_email, Subscribtion

urlpatterns = [
    path('login/', LoginView.as_view(template_name='sign/login.html'), name='login'),
    path('logout/',LogoutView.as_view(template_name='sign/logout.html'), name='logout'),
    path('signup/',BaseRegisterView.as_view(template_name='sign/signup.html'), name='signup'),
    path('upgrade/', upgrade_me, name='upgrade'),
    path('recipient/', recipients_email, name='recipient'),
    path('subscribe/', Subscribtion.as_view()),

]