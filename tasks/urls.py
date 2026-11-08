from django.urls import path
from tasks.views import CreateTaskView, ViewTaskView, CreateSubTaskView, ViewSubTaskView, EditTaskView, EditSubTaskView

urlpatterns = [
    path('createTask/', CreateTaskView.as_view()),
    path('viewTask/', ViewTaskView.as_view()),
    path('createSubTask/', CreateSubTaskView.as_view()),
    path('viewSubTask/', ViewSubTaskView.as_view()),
    path('editTask/', EditTaskView.as_view()),
    path('editSubTask/', EditSubTaskView.as_view())
]