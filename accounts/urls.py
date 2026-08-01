from django.urls import path

from accounts.views import LoginView, MeView, RegisterView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('me/', MeView.as_view()),
]
