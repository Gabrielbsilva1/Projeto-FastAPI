from fastapi import APIRouter, Depends, HTTPException
from dependences import *
import jwt
from schemas import *
from sqlalchemy.orm import Session


auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/")
async def home():
    return {
        "mensagem": "Você acessou a rota de autenticação",
        "Autenticado": False
            }

@auth_router.post("/criar_conta") 
async def criarContaUsuario(usuarioSc=UsuarioSchema,sessao:Session = Depends(pegarSessao)):
    '''
        Rota de Criação de Usuario com Senha hash
    '''
    usuario = sessao.query(Usuario).filter_by(email=usuarioSc.email).first() # comando para encontrar o primeiro email que encontrar no banco de dados
    if usuario:
        # ja tem um email cadastrado! enviar erro
        raise HTTPException(status_code=400,detail="O Usuario ja esta cadastrado")
    else:
        senhaCriptografada = bcrypt_context.hash(usuarioSc.senha)
        sessao.add(Usuario(usuarioSc.nome,usuarioSc.email, senhaCriptografada,usuarioSc.ativo))
        sessao.commit()
        return {"Mensagem": "Usuario Cadastrado com sucesso!"}

@auth_router.post("/criar_conta_funcionario")
async def criarContaFuncionario(funcionario = FuncionarioSchema, sessao:Session = Depends(pegarSessao)):
    '''
        Rota de Criação de Funcionario com senha hash
    '''
    usuario = sessao.query(Funcionario).filter_by(email=funcionario.email).first()
    if usuario:
        raise HTTPException(status_code=400,detail="Funcionario ja esta cadastrado")
    else:
        senhaCriptografada = bcrypt_context.hash(funcionario.senha)
        sessao.add(Funcionario(funcionario.nome,funcionario.email,senhaCriptografada, funcionario.ativo,funcionario.admin))
        sessao.commit()
        return {"Mensagem": f"Funcionarios Cadastrado com sucesso! {funcionario.email}"}

@auth_router.post("/autenticacao")
async def autenticar(funcionarioSc = FuncionarioSchema,sessao=Depends(pegarSessao),hora=Depends(horarioFuncionario)):
    '''
        Rota de Autenticação, jwt Token
    '''
    funcionario = sessao.query(Funcionario).filter_by(email=funcionarioSc.email).first()
    if funcionario:
        matchSenha = bcrypt_context.verify(funcionarioSc.senha,funcionario.senha)
        if matchSenha:
            payload = {"sub": funcionario.id, "nome": funcionario.nome, "exp": hora}
            token = jwt.encode(payload, str(SECRET_KEY), algorithm="HS256")
            return {"Access_Token": token, "token_type": "bearer"}
        else:
            raise HTTPException(status_code=401,detail="Senha Incorreta!")
    else:
        raise HTTPException(status_code=404,detail="Usuario não encontrado!")

