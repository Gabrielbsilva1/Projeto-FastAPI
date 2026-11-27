from fastapi import APIRouter, Depends, HTTPException
from dependences import *
import jwt


auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/")
async def home():
    return {
        "mensagem": "Você acessou a rota de autenticação",
        "Autenticado": False
            }

@auth_router.post("/criar_conta") 
async def criarContaUsuario(nome:str,email:str,senha:str,sessao = Depends(pegarSessao)):
    '''
        Rota de Criação de Usuario com Senha hash
    '''
    usuario = sessao.query(Usuario).filter_by(email=email).first() # comando para encontrar o primeiro email que encontrar no banco de dados
    if usuario:
        # ja tem um email cadastrado! enviar erro
        raise HTTPException(status_code=400,detail="O Usuario ja esta cadastrado")
    else:
        senhaCriptografada = bcrypt_context.hash(senha)
        sessao.add(Usuario(nome,email, senhaCriptografada,))
        sessao.commit()
        return {"Mensagem": "Usuario Cadastrado com sucesso!"}

@auth_router.post("/criar_conta_funcionario")
async def criarContaFuncionario(nome:str, email:str, senha:str, sessao = Depends(pegarSessao)):
    '''
        Rota de Criação de Funcionario com senha hash
    '''
    usuario = sessao.query(Funcionario).filter_by(email=email).first()
    if usuario:
        raise HTTPException(status_code=400,detail="Funcionario ja esta cadastrado")
    else:
        senhaCriptografada = bcrypt_context.hash(senha)
        sessao.add(Funcionario(nome,email,senhaCriptografada))
        sessao.commit()
        return {"Mensagem": "Funcionarios Cadastrado com sucesso!"}

@auth_router.post("/adminCreate")
async def criarAdmin(nome:str,email:str,senha:str,admin=True,sessao=Depends(pegarSessao)):
    '''
        Rota de Criação de Administrador com senha hash
    '''
    admin = sessao.query(Funcionario).filter_by(email=email).first()
    if admin:
        raise HTTPException(status_code=400,detail="O Administrador ja esta cadastrado")
    else:
        senhaHash = bcrypt_context.hash(senha)
        sessao.add(Funcionario(nome,email,senhaHash,admin))
        sessao.commit()
        return {"Mensagem": "Administrador registrado com sucesso"}

@auth_router.post("/autenticacao")
async def autenticar(email:str,senha:str,sessao=Depends(pegarSessao),hora=Depends(horarioFuncionario)):
    '''
        Rota de Autenticação, jwt Token
    '''
    funcionario = sessao.query(Funcionario).filter_by(email=email).first()
    if funcionario:
        matchSenha = bcrypt_context.verify(senha,funcionario.senha)
        if matchSenha:
            payload = {"sub": funcionario.id, "nome": funcionario.nome, "exp": hora}
            token = jwt.encode(payload, str(SECRET_KEY), algorithm="HS256")
            return {"Access_Token": token, "token_type": "bearer"}
        else:
            raise HTTPException(status_code=401,detail="Senha Incorreta!")
    else:
        raise HTTPException(status_code=404,detail="Usuario não encontrado!")

