from fastapi import APIRouter, HTTPException, Depends
from dependences import *

order_router = APIRouter(prefix="/pedidos", tags=["pedidos"])

@order_router.post("/criar_pedido")
async def criarPedidos():
    '''
        Cria Pedido de vendas
    '''
    pass