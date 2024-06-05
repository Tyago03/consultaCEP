from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
from bs4 import BeautifulSoup

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

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}

@app.get("/ticker/{codigo_ticker}")
def get_ticker_info(codigo_ticker: str):
    url = f"https://www.fundamentus.com.br/detalhes.php?papel={codigo_ticker.upper()}"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    td = soup.find('td', class_='data destaque w3')
    if td:
        span = td.find('span', class_='txt')
        if span:
            cotacao = span.text.strip()
            return {
                "ticker": codigo_ticker.upper(),
                "cotacao": float(cotacao.replace(',', '.'))
            }
    return {"error": "Cotação não encontrada"}


@app.get("/moedas")
def get_moedas():
    url = "https://raw.githubusercontent.com/ourworldincode/currency/main/currencies.json"
    try:
        response = requests.get(url)
        all_currencies_dict = response.json()
        filtered_currencies = []

        for code, details in all_currencies_dict.items():
            filtered_currencies.append({
                "codigo": code,
                "nome": details["name"],
                "simbolo": details["symbol"]
            })

        return filtered_currencies
    except Exception as e:
        return {"error": str(e)}
