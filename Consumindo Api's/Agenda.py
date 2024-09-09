import requests

url = " https://projetofaculdadefiap-default-rtdb.firebaseio.com/contatos.json"

contato = {
    "nome" : "Alexandre",
    "email" : "Alexandre@.com",
    "telefone":"(13) 98786-7272"
}

response = requests.post(url , json=contato)
print(response) 
