from accounts.views.signin import Signin
from django.urls import path 

urlpatterns = [
    path('signin', Signin.as_view()),
]