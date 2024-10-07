import requests
import json
import sqlite3




def Escolha_Da_Cidade():
    dicio_cidade ={}
    cidade =  input("Qual cidade deseja : ")
    res = requests.get(f"https://api.weatherapi.com/v1/timezone.json?key=a62f6ad9c5e74a809c9120338240710&q={cidade}&aqi=no" )
    dicio_cidade = json.loads(res.content)
    a1 = dicio_cidade['location']['localtime']
    a2 = dicio_cidade['location']['name']
    a3 = dicio_cidade['location']['country']
    print(f"\n {a3} : {a2} : {a1}\n")



    
    

Escolha_Da_Cidade() 