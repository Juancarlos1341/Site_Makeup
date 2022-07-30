from django.shortcuts import render, get_object_or_404, redirect
from Produtos.models import Produtos
from django.contrib import messages
from .models import *
from .funcoes import *


def adicionar_item(request, id):
    produto = Produtos.objects.get(pk=id)
    if request.session.get('id_carrinho') is None:
        carrinho = Carrinho.objects.last()
        carrinho_id = carrinho.numero
        criar_carrinho(carrinho_id)
        request.session['id_carrinho'] = int(carrinho_id) + 1
    verifica_id_carrinho(request)
    if 'quantidade' in request.GET:
        id_carrinho = request.session.get('id_carrinho')
        item_igual = verifica_item(produto, id_carrinho)
        if not item_igual:
            quantidade = request.GET['quantidade']
            diminuir_estoque(quantidade, produto.id)
            salvar_pedido(quantidade, produto, id_carrinho)
            listar_item(request, id_carrinho, produto.nome_produto)
            messages.success(request, f'O { produto.nome_produto } foi adicionado com sucesso')
            return redirect('carrinho')
        else:
            messages.error(request, 'Este produto já tem em seu carrinho, tente alterar !')
            return redirect('carrinho')


def remover_item(request, id_item):
    quantidade, nome, valor = revomer(id_item, request)
    produto = Produtos.objects.get(nome_produto=nome)
    aumentar_estoque(quantidade,produto.id)
    carrinho = Carrinho.objects.get(numero=request.session.get('id_carrinho'))
    carrinho.valor_total -= valor
    if carrinho.valor_total <= 0:
        carrinho.valor_total = 0.00
    carrinho.save()
    messages.error(request, 'Produto foi retirado do seu carrinho com sucesso.')
    return redirect('carrinho')


def pagina_alterar(request, nome, id):
    produto = get_object_or_404(Produtos, nome_produto=nome)
    dados = {
        'produto': produto,
        'id': id
    }
    return render(request,'produtos/produto-alterar.html', dados)


def alterar_item(request, nome, id):
    if 'quantidade' in request.GET:
        quantidade = request.GET['quantidade']
        id_carrinho = request.session.get('id_carrinho')
        alterar_produto_no_carrinho(nome, id, id_carrinho, quantidade, request)
        messages.warning(request, f'o {nome} foi alterado com suscesso no seu carrinho.')
        return redirect('carrinho')


def pagina_do_carrinho_de_compra(request):
    if request.session.get('id_carrinho') is None:
        dados = {
        'carrinho': ''
        }
        return render(request, 'carrinho/carrinho.html', dados)
    verifica_lista_de_compras(request)
    verifica_id_carrinho(request)
    id = request.session.get('id_carrinho')
    lista_do_carrinho = Items.objects.order_by().filter(numero_carrinho=id)
    carrinho_de_compra = Carrinho.objects.order_by().filter(numero=id)

    dados = {
        'carrinho': lista_do_carrinho,
        'preco': carrinho_de_compra
    }
    return render(request, 'carrinho/carrinho.html', dados)


def deletar_carrinho(request):
    deletar_todos_os_itens(request, request.session.get('id_carrinho'))
    messages.success(request, f'Seu Carrinho foi esvaziado com sucesso')
    return redirect("index")

def finalizar_compra(request):
    if request.method == 'POST':
        nome = request.POST['pessoa-nome']
        endereco = request.POST['endereco']
        telefone = request.POST['telefone']
        add_informacoes_do_usuario(nome, endereco, telefone, 'Finalizado', request)
        id = request.session.get('id_carrinho')
        lista_do_carrinho = Items.objects.order_by().filter(numero_carrinho=id)
        carrinho_de_compra = Carrinho.objects.order_by().filter(numero=id)
        dados = {
            'carrinho': lista_do_carrinho,
            'preco': carrinho_de_compra
            }
        request.session['lista_de_compras'] = None
        request.session['id_carrinho'] = None
        return render(request, 'finalizar.html', dados)
    id_carrinho = request.session.get('id_carrinho')
    carrinho = Carrinho.objects.get(numero=id_carrinho)
    dados = {
        'carrinho': carrinho,
    }
    return render(request, 'usuarios/cadastro.html', dados)