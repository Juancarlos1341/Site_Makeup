from django.db import models
from datetime import datetime


class Categoria(models.Model):
    nome = models.CharField(max_length=240)
    publicada = models.BooleanField(default=True)

    def __str__(self):
        return self.nome


class Produtos(models.Model):
    nome_produto = models.CharField(max_length=240)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    preco = models.DecimalField(max_digits=100, decimal_places=2)
    descricao = models.TextField(max_length=240)
    estoque = models.IntegerField()
    imagem_produto = models.ImageField(upload_to='produtos/%d', blank=True)
    ativo = models.BooleanField(default=True)
    data_de_criacao = models.DateTimeField(default=datetime.now, blank=True)
    promocao = models.BooleanField(default=False)
    oferta = models.BooleanField(default=False)
    aparecer_no_desteque = models.BooleanField(default=False)

    def __str__(self):
        return self.nome_produto

class Dicas_produtos(models.Model):
    titulo_da_dica = models.CharField(max_length=100)
    produto = models.ForeignKey(Produtos, on_delete=models.CASCADE)
    imagem = models.ImageField(upload_to='dicas/%d', blank=True)
    descricao = models.TextField(max_length=255)
    publicar_dica = models.BooleanField(default=True)

    def __str__(self):
        return self.titulo_da_dica

class Carrossel(models.Model):
    nome_do_carrossel = models.CharField(max_length=100)
    carrosel_1 = models.ImageField(upload_to='Carrosel/%d', blank=False)
    carrosel_2 = models.ImageField(upload_to='Carrosel/%d', blank=False)
    carrosel_3 = models.ImageField(upload_to='Carrosel/%d', blank=False)
    publicar = models.BooleanField(default=True)

    def __str__(self):
        return self.nome_do_carrossel
