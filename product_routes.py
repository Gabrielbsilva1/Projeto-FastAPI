from fastapi import APIRouter, Depends, HTTPException
from dependences import Produtos, Pizza, pegarSessao
from sqlalchemy import select
from sqlalchemy.orm import Session
from schemas import PizzaSchema, ProdutoSchema

product_router = APIRouter(prefix="/products", tags=["produtos"])

@product_router.get("/")
async def lista(sessao=Depends(pegarSessao)):
    '''
        Lista os resultados da tabela de produtos  
    '''
    prod=sessao.scalars(select(Pizza)).all()
    return prod

@product_router.post('/add_pizza')
async def addPizza(pizza=PizzaSchema,sessao:Session=Depends(pegarSessao)):
    '''
        Registrar nova pizza na tabela
    '''
    produto = sessao.query(Pizza).filter_by(sabor=pizza.sabor).first()
    if produto:
        raise HTTPException(status_code=400, detail="[ERRO] Pizza Ja Cadastrada!")
    else:
        sessao.add(Pizza(pizza.sabor,pizza.tamanho,pizza.preço))
        sessao.commit()
        return {"Mensagem": "Pizza Cadastrada com Sucesso!"}

@product_router.post("/add_produto")
async def addProduto(produtoSc=ProdutoSchema,sessao:Session=Depends(pegarSessao)):
    '''
        Registrar novo produto na tabela
    '''
    prod = sessao.query(Produtos).filter_by(produto=produtoSc.produto).first()
    if prod:
        raise HTTPException(status_code=400,detail="[ERRO] Produto Ja Cadastrado!")
    else:
        sessao.add(Produtos(produtoSc.produto,produtoSc.tipo))
        sessao.commit()
        return {"Mensagem": "Produto Cadastrado com Sucesso!"}

