from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('categoria/<int:id>', views.lista_produtos_categoria, name='listagem_podutos_por_categoria'),
    path('listagem', views.listagem, name='lista_de_categoria'),
    path('produto/<int:id>',views.produtos,name='produto'),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)