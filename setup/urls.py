from django.contrib import admin
from django.urls import path
from objetos.views import adicionar_materiais
from objetos.views import material_detail
from objetos.views import index
from objetos.views import MaterialListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('material/<int:pk>/', material_detail, name='material_detail'),
    path('api/materiais/', MaterialListView.as_view(), name='material-list'),
    path('api/adicionar-materiais/', adicionar_materiais, name='adicionar_materiais'),
]
