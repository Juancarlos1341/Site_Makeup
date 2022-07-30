from unicodedata import name
from django import urls
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('carrinho',views.pagina_do_carrinho_de_compra, name='carrinho'),
    path('add-carrinho/<int:id>', views.adicionar_item, name='adicionar'),
    path('remover/<int:id_item>', views.remover_item, name='remover'),
    path('alterar/<str:nome>/<int:id>',views.alterar_item, name='alterar'),
    path('pagina/<str:nome>/<int:id>', views.pagina_alterar, name='pagina_alterar'),
    path('deletar/', views.deletar_carrinho, name='apagar_tudo'),
    path('finalizar/', views.finalizar_compra, name='finalizar'),
    ]