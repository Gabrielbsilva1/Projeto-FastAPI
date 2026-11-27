from datetime import datetime, timedelta
from models import *
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def pegarSessao():
    try:
        Session = sessionmaker(bind=db)
        sessao = Session()
        yield sessao
    finally:    
        sessao.close()

def horarioFuncionario():
    horaFuncional = timedelta(hours=10)
    horaAtual = datetime.now()
    return horaAtual + horaFuncional

