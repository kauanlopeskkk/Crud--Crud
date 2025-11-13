from fastapi import FastAPI, HTTPException, Depends
from secrets import compare_digest
from pydantic import BaseModel
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()


class Conta(BaseModel):
    nome: str
    saldo: float

conta = [
Conta(nome="Usuário Exemplo", saldo=1000.0),
Conta(nome="Outro Usuário", saldo=2500.5),
Conta(nome="Terceiro Usuário", saldo=300.75),
Conta(nome="Quarto Usuário", saldo=150.0),
Conta(nome="Quinto Usuário", saldo=5000.0),
] 
USUARIO = "Admin"
SENHA = "123456"
security = HTTPBasic()

def autenticar_usuario(credentials: HTTPBasicCredentials = Depends(security)):
    is_username_correct = compare_digest(credentials.username, USUARIO)
    is_password_correct = compare_digest(credentials.password, SENHA)
    if not (is_username_correct and is_password_correct):
        raise HTTPException(
            status_code=401,
            detail="USUARIO OU SENHA INCORRETOS",
            headers={"WWW-Authenticate": "Basic"},
        )
@app.get("/")
def read_root():
    return {"message": "Bem-vindo ao sistema de contas!"}



@app.get("/contas", response_model=list[Conta])
def get_contas(page: int = 1, limit: int = 5, credentials: HTTPBasicCredentials = Depends(autenticar_usuario)):
    if page < 1 or limit < 1:
        raise HTTPException(status_code=400, detail="Parâmetros inválidos. 'page' e 'limit' devem ser maiores que zero.")
    contas_paginadas = sorted(conta, key=lambda x: x.nome)
    start = (page - 1) * limit
    end = start + limit
    contas_paginadas = conta[start:end]
    
    return{
        "page": page,
        "limit": limit,
        "total_contas": len(conta),
        "contas": contas_paginadas
    }