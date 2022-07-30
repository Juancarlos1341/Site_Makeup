from .models import *
from django.shortcuts import get_object_or_404
from decimal import Decimal
from Produtos.models import Produtos


def salvar_pedido(quantidade, produto, id):
    '''Salva um Pedido no banco de dados'''
    lista_compra = Items.objects.create(
        numero_carrinho = id,
        produtos= produto.nome_produto,
        preco= produto.preco,
        quantidade= quantidade,
        preco_final= str(int(quantidade) * float(produto.preco))
    )
    lista_compra.save()
    try:
        carrinho = Carrinho.objects.get(numero=id)
    except:
        criar_carrinho(id)
    carrinho.valor_total += Decimal(lista_compra.preco_final)
    carrinho.save()


def criar_carrinho(id):
    '''Cria um novo carrinho caso precise'''
    nova_id = int(id) + 1
    carrinho = Carrinho.objects.create(
        numero = nova_id,
        valor_total = 0.00,
        status = "Andamento",
        pertence_a = "Pessoa",
        endereco = 'null',
        telefone = 'null'
    )
    carrinho.save()


def revomer(id, request):
    '''Remove o item do banco de dados e na lista'''
    item = get_object_or_404(Items, pk=id)
    quantidade = item.quantidade
    nome = item.produtos
    valor = item.preco_final
    item.delete()
    lista = request.session['lista_de_compras']
    lista.remove(id)
    request.session['lista_de_compras'] = lista
    return quantidade, nome, valor


def preco_total():
    """Soma o preço do carrinho"""
    item = Items.objects.get()
    valor_anterior = 0
    for novo_valor in item:
        valor_total = valor_anterior + float(novo_valor)
        valor_anterior = float(novo_valor)
    
    return valor_total


def verifica_item(produto, id):
    try:
        items = Items.objects.get(produtos=produto, numero_carrinho=id)
        if items.produtos != produto :
            return True
        else :
            return False
    except :
        return False


def alterar_produto_no_carrinho(nome, id, id_carrinho, nova_quantidade, request):
    '''Aletera o produto selecionado, excluindo o antigo e adicionando um novo.'''
    produto = get_object_or_404(Produtos, nome_produto=nome)
    quantidade, nome, valor = revomer(id, request)
    produto = Produtos.objects.get(nome_produto=nome)
    aumentar_estoque(quantidade, produto.id)
    carrinho = Carrinho.objects.get(numero=id_carrinho)
    carrinho.valor_total -= valor
    carrinho.save()
    salvar_pedido(nova_quantidade, produto, id_carrinho)
    diminuir_estoque(nova_quantidade, produto.id)
    listar_item(request, id_carrinho, nome)


def diminuir_estoque(quantidade, id):
    '''Diminui o estoque do produto selecionado'''
    produto = Produtos.objects.get(pk=id)
    produto.estoque -= int(quantidade)
    produto.save()


def aumentar_estoque(quantidade, id):
    '''Aumenta o estoque do produto selecionado'''
    produto = Produtos.objects.get(pk=id)
    produto.estoque += int(quantidade)
    produto.save()


def deletar_todos_os_itens(request, id_carrinho):
    '''zera todo o carrinho'''
    lista = request.session['lista_de_compras']
    lista_2 = lista
    for id_item in lista_2:
        quantidade, nome, valor = remover_item(id_item)
        produto = Produtos.objects.get(nome_produto=nome)
        aumentar_estoque(quantidade, produto.id)
        carrinho = Carrinho.objects.get(numero=id_carrinho)
        carrinho.valor_total -= valor
        carrinho.save()
    request.session['lista_de_compras'] = None
    carrinho = get_object_or_404(Carrinho, numero=request.session.get('id_carrinho'))
    carrinho.delete()
    request.session['id_carrinho'] = None
    request.session.modified = True


def listar_item(request, id_carrinho, produto):
    '''Adciona id do item na sessao de lista'''
    item = Items.objects.get(numero_carrinho=id_carrinho, produtos=produto)
    lista = request.session['lista_de_compras']
    lista.append(item.id)
    request.session['lista_de_compras'] = lista


def remover_item(id):
    '''Remove o id do item na sessao de lista'''
    item = get_object_or_404(Items, pk=id)
    quantidade = item.quantidade
    nome = item.produtos
    valor = item.preco_final
    item.delete()
    return quantidade, nome, valor


def verifica_id_carrinho(request):
    '''Verifica se existe o id do carrinho no banco de dados, evitando erros'''
    id_carrinho = request.session.get('id_carrinho')
    try:
        carrinho = Carrinho.objects.get(numero=id_carrinho)
        request.session['id_carrinho'] = carrinho.numero
        request.session.modified = True
    except:
        recriar_carrinho(request)
    

def verifica_lista_de_compras(request):
    '''Verifica se existe o id do produto no banco de dados, evitando erros'''
    lista = request.session['lista_de_compras']
    for id_item in lista:
        try:
            Items.objects.get(id=id_item)
        except:
            lista.remove(id_item)
            redefinir_valor_carrinho(request)
            request.session['lista_de_compras'] = lista
            request.session.modified = True
            

def verifica_estoque():
    '''Verifica se o estoque do produto está zerado e ele inativa por este motivo'''
    for i in range(1, len(Produtos.objects.order_by())):
        produto = Produtos.objects.get(pk=i)
        if produto.estoque == 0:
            produto.ativo = False
            produto.save()


def recriar_carrinho(request):
    id_carrinho = request.session.get('id_carrinho')
    lista = request.session['lista_de_compras']
    valor = 0
    for id_item in lista:
        produto = Items.objects.get(id=id_item)
        valor += produto.preco_final

    carrinho = Carrinho.objects.create(
        numero = id_carrinho,
        valor_total = valor,
    )
    carrinho.save()

def redefinir_valor_carrinho(request):
    lista = request.session['lista_de_compras']
    carrinho = Carrinho.objects.get(numero=request.session.get('id_carrinho'))
    for id_item in lista:
        produto = Items.objects.get(id=id_item)
        carrinho.valor_total -= produto.preco_final
        carrinho.save()

def add_informacoes_do_usuario(nome, endereco, telefone, status, request):
    id_carrinho = request.session.get('id_carrinho')
    carrinho = Carrinho.objects.get(numero=id_carrinho)
    carrinho.pertence_a = nome
    carrinho.endereco = endereco
    carrinho.telefone = telefone
    carrinho.status = status
    carrinho.save()
