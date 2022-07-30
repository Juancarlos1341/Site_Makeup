from django.contrib import admin
from .models import *


class Listando_produtos(admin.ModelAdmin):
    #Add nome ou outras informaçoes
    list_display = ('id', 'nome_produto', 'ativo', 'oferta', 'promocao','aparecer_no_desteque','estoque')
    #Cria links para acessar a receita
    list_display_links = ('id', 'nome_produto')
    #Cria um campo de busca
    search_fields = ('nome_produto',)
    #Cria um flitro
    list_filter = ('categoria',)
    #limite de exbição da pagina e add paginação
    list_per_page = 10
    # Editar sem presisar entrar no campo
    list_editable = ('ativo', 'oferta','promocao','aparecer_no_desteque','estoque')

class Listando_categoria(admin.ModelAdmin):
    #Add nome ou outras informaçoes
    list_display = ('id', 'nome', 'publicada')
    #Cria links para acessar a receita
    list_display_links = ('id', 'nome')
    #Cria um campo de busca
    search_fields = ('nome',)
    #Cria um flitro
    list_filter = ('nome',)
    #limite de exbição da pagina e add paginação
    list_per_page = 10
    # Editar sem presisar entrar no campo
    list_editable = ('publicada',)


class Listando_dicas(admin.ModelAdmin):
    #Add nome ou outras informaçoes
    list_display = ('id', 'titulo_da_dica', 'publicar_dica')
    #Cria links para acessar a receita
    list_display_links = ('id', 'titulo_da_dica')
    #Cria um campo de busca
    search_fields = ('titulo_da_dica',)
    #limite de exbição da pagina e add paginação
    list_per_page = 10
    # Editar sem presisar entrar no campo
    list_editable = ('publicar_dica',)


admin.site.register(Categoria, Listando_categoria)
admin.site.register(Produtos, Listando_produtos)
admin.site.register(Dicas_produtos, Listando_dicas)
admin.site.register(Carrossel)
