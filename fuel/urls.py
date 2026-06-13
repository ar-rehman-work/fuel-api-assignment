from django.urls import path
from fuel.views import RegisterView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register')
]
