from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/hello")
def read_root():
    return {"msg": "Hello World!"}

@app.get("/hello/{nome}")
def hello(nome: str):
    return {"msg": f"Hello {nome}!"}

@app.get("/cep/{cep}")
def get_cep_info(cep: str):
    url = f"https://viacep.com.br/ws/{cep}/json"
    response = requests.get(url)
    data = response.json()
    if "erro" in data:
        return {"error": "CEP não encontrado"}
    filtered_data = {
        "cep": data.get("cep", ""),
        "logradouro": data.get("logradouro", ""),
        "complemento": data.get("complemento", ""),
        "bairro": data.get("bairro", ""),
        "localidade": data.get("localidade", ""),
        "uf": data.get("uf", "")
    }
    return filtered_data
