from fastapi import APIRouter, HTTPException, Depends
from dependences import *
from schemas import PedidoSchema
from sqlalchemy.orm import Session

order_router = APIRouter(prefix="/pedidos", tags=["pedidos"])

