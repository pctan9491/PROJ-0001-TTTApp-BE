from django.urls import path
from tasks.views import CreateTaskView, ViewTaskView

urlpatterns = [
    path('createTask/', CreateTaskView.as_view()),
    path('viewTask/', ViewTaskView.as_view()),
]