from pydantic import BaseModel
from typing import Optional

class FuncionarioSchema(BaseModel):
    nome:str
    email:str
    telefone:Optional[int]
    senha:str
    ativo:Optional[bool]
    admin:Optional[bool]

    class config:
        from_atributes = True

class UsuarioSchema(BaseModel):
    nome:str
    email:str
    telefone:Optional[int]
    senha:str
    ativo:Optional[bool]

    class config:
        from_atributes = True

class PedidoSchema(BaseModel):
    itens:str
    status:Optional[str]
    usuario:str
    preço:float

    class config:
        from_atributes = True

class PizzaSchema(BaseModel):
    sabor:str
    tamanho:str
    preço:float

    class config:
        from_atributes = True

class ProdutoSchema(BaseModel):
    produto:str
    tipo:str

    class config:
        from_atributes = True