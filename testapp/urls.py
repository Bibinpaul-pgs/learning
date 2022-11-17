from testapp import views
from django.urls import path

urlpatterns = [
    path('student',views.StudentGeneric.as_view()),
    path('student/<id>',views.StudentGeneric.as_view()),
    path('filter',views.FilterView.as_view()),
]