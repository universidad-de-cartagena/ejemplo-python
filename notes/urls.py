from django.urls import path

from notes import views

urlpatterns = [
    path('', views.index, name='notes.index'),
    path('<uuid:note_uuid>', views.index, name='notes.uuid')
]
