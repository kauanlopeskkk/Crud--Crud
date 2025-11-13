from fastapi import FastAPI, HTTPException, Depends

import secrets
from pydantic import BaseModel
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI(
    title="Jogoteca API",
    description="API para gerenciar uma coleção de jogos.",
    version="1.0.0",
    contact={
        "name": "Kauan Lopes",
        "email": "kauanlopes2706@gmail.com"
    }
)

MEU_USUARIO = "Kauan Lopes"
MINHA_SENHA = "Pinto"

security = HTTPBasic()

def autenticar_usuario(credentials: HTTPBasicCredentials = Depends(security)):
    is_username_correct = secrets.compare_digest(credentials.username, MEU_USUARIO)
    is_password_correct = secrets.compare_digest(credentials.password, MINHA_SENHA)

    if not (is_username_correct and is_password_correct):
        raise HTTPException(
            status_code=401,
            detail="USUARIO OU SENHA INCORRETOS",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials
    

jogoteca = {}

class Jogo(BaseModel):
    nome_do_jogo: str
    genero: str
    ano_lancamento: int

@app.get("/")
def hello_world():
    return {"message": "Bem-vindo à jogoteca!"}

@app.get("/jogos")
def get_jogos(page: int = 1, limit: int = 5):
    if page < 1 or limit < 1:
        raise HTTPException(status_code=400, detail="Parâmetros inválidos. 'page' e 'limit' devem ser maiores que zero.")
    
    if not jogoteca:
        return {"message": "Nenhum jogo cadastrado."}
    
    jogos_paginados = sorted(jogoteca.items(),key=lambda x: x[0])

    start = (page - 1) * limit
    end = start + limit
    jogos_paginados =[
        {"id": id_jogo, "nome_do_jogo": jogo["nome_do_jogo"], "genero": jogo["genero"], "ano_lancamento": jogo["ano_lancamento"]}
        for id_jogo, jogo in list(jogoteca.items())[start:end]
    ]
    
    return {
        "page": page,
        "limit": limit,
        "total_jogos": len(jogoteca),
        "jogos": jogos_paginados    
    }

@app.post("/adicionar_jogo/{id_jogo}")
def post_jogo(id_jogo: int, jogo: Jogo, contentials: HTTPBasicCredentials = Depends(autenticar_usuario) ):
    if id_jogo in jogoteca:
        raise HTTPException(status_code=400, detail="Jogo já cadastrado.")
    jogoteca[id_jogo] = jogo.dict()
    return {"message": "Jogo adicionado com sucesso."}

@app.put("/atualizar_jogo/{id_jogo}")
def put_jogo(id_jogo: int, jogo: Jogo, contentials: HTTPBasicCredentials = Depends(autenticar_usuario)):
    meu_jogo = jogoteca.get(id_jogo)
    if not meu_jogo:
        raise HTTPException(status_code=404, detail="Jogo não encontrado.")
    jogoteca[id_jogo] = jogo.dict()
    return {"message": "Jogo atualizado com sucesso."}

@app.delete("/deletar_jogo/{id_jogo}")
def delete_jogo(id_jogo: int, contentials: HTTPBasicCredentials = Depends(autenticar_usuario)):
    if id_jogo not in jogoteca:
        raise HTTPException(status_code=404, detail="Jogo não encontrado.")
    else:
        del jogoteca[id_jogo]
        return {"message": "Jogo deletado com sucesso."}
