from sqlalchemy import create_engine, Column, String, Integer, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base


# cria a conexão do seu banco
db = create_engine("sqlite:///banco.db")

# cria a base do banco de dados  
Base = declarative_base()

class Funcionario(Base):
    __tablename__ = "funcionarios"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome",String)
    email = Column("email",String, nullable=False, unique=True)
    telefone = Column("telefone",Integer)
    senha = Column("senha",String, nullable=False)
    ativo = Column("ativo",Boolean, default=True)
    admin = Column("admin",Boolean, nullable=False, default=False)

    def __init__(self,nome,email,senha,ativo,admin):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.admin = admin
 
# criar as classes/Tabelas do banco 
class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column("id", Integer, primary_key=True, autoincrement=True) 
    nome = Column("nome", String)
    email = Column("email", String, nullable=False, unique=True) # nullable=False impede que se crie um usuario sem a coluna ativada com False
    telefone = Column("telefone", Integer)
    senha = Column("senha", String, nullable=False)
    ativo = Column("ativo", Boolean, default=True)

    def __init__(self, nome, email, senha, ativo):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo

class Pedido(Base):
    __tablename__ = "pedidos"
    
    id = Column("id", Integer, primary_key=True, autoincrement=True) 
    itens = Column("itens", ForeignKey("pizzas.id"))
    status = Column("status", String)
    usuario = Column("usuario", ForeignKey("usuarios.id"))
    preço = Column("preço", Float)

    def __init__(self, itens, usuario, status="PENDENTE", preço=0):
        self.itens = itens
        self.usuario = usuario
        self.preço = preço 
        self.status = status

class Pizza(Base):
    __tablename__ = "pizzas"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    sabor = Column("sabor", String, unique=True)
    tamanho = Column("tamanho", String)
    preço = Column("preço", Float, nullable=False)

    def __init__(self, sabor, tamanho, preço):
        self.sabor = sabor
        self.tamanho = tamanho 
        self.preço = preço

class Produtos(Base):
    __tablename__ = "produtos"
    
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    produto = Column("produto", String, nullable=False)
    tipo = Column("tipo", String, nullable=False)

    def __init__(self,produto,tipo):
        self.produto = produto
        self.tipo = tipo
# Executa a criação dos metadados do seu banco (cria efetivamente o banco de dados)

