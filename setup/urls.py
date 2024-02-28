from django.contrib import admin
from django.urls import path
from objetos.views import adicionar_materiais
from objetos.views import index
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('api/adicionar-materiais/', adicionar_materiais, name='adicionar_materiais'),
]
