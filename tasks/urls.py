from django.urls import path
from tasks.views import CreateTaskView, ViewTaskView, CreateSubTaskView, ViewSubTaskView

urlpatterns = [
    path('createTask/', CreateTaskView.as_view()),
    path('viewTask/', ViewTaskView.as_view()),
    path('createSubTask/', CreateSubTaskView.as_view()),
    path('viewSubTask/', ViewSubTaskView.as_view()),
]