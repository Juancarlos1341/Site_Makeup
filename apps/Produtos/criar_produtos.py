from .models import Produtos,Categoria
from datetime import datetime


def chamar():
    for i in range(51,61):
        produto = f'Produto Teste {i}'
        categoria = Categoria.objects.get(id=6)
        lista_compra = Produtos.objects.create(
            nome_produto = produto,
            categoria = categoria,
            preco = 10.00,
            descricao = 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Amet modi ullam, repellat cupiditate minima',
            estoque = 100,
            imagem_produto = '',
            ativo = True,
            data_de_criacao = str(datetime.now()),
            promocao = False,
            oferta = False,
            aparecer_no_desteque = False,
        )
        lista_compra.save()