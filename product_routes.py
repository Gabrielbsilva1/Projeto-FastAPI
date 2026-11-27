from fastapi import APIRouter, Depends, HTTPException
from dependences import Produtos, Pizza, pegarSessao
from sqlalchemy import select

product_router = APIRouter(prefix="/products", tags=["produtos"])

@product_router.get("/")
async def lista(sessao=Depends(pegarSessao)):
    '''
        Lista os resultados da tabela de produtos  
    '''
    prod=sessao.scalars(select(Pizza)).all()
    return prod

@product_router.post('/add_pizza')
async def addPizza(sabor:str,tamanho:str,preço:float,sessao=Depends(pegarSessao)):
    '''
        Registrar nova pizza na tabela
    '''
    produto = sessao.query(Pizza).filter_by(sabor=sabor).first()
    if produto:
        raise HTTPException(status_code=400, detail="[ERRO] Pizza Ja Cadastrada!")
    else:
        sessao.add(Pizza(sabor,tamanho,preço))
        sessao.commit()
        return {"Mensagem": "Pizza Cadastrada com Sucesso!"}

@product_router.post("/add_produto")
async def addProduto(produto:str,tipo:str,sessao=Depends(pegarSessao)):
    '''
        Registrar novo produto na tabela
    '''
    prod = sessao.query(Produtos).filter_by(produto=produto).first()
    if prod:
        raise HTTPException(status_code=400,detail="[ERRO] Produto Ja Cadastrado!")
    else:
        sessao.add(Produtos(produto,tipo))
        sessao.commit()
        return {"Mensagem": "Produto Cadastrado com Sucesso!"}

