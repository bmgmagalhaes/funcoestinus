import pandas as pd
import re

def mascarar_documento(doc):
    doc = str(doc)
    numeros = re.sub(r'\D', '', doc)
    
    if len(numeros) == 11:  # CPF
        # Exemplo: 035.753.224-49 → ***.753.224-**
        return f"***.{numeros[3:6]}.{numeros[6:9]}-**"
    elif len(numeros) == 14:  # CNPJ
        # Exemplo: 08.332.785/0001-01 → **.332.785-****-**
        return f"**.{numeros[2:5]}.{numeros[5:8]}-{numeros[8:10]}**-**"
    else:
        return doc

# Lendo o CSV com separador correto e encoding Latin-1
df = pd.read_csv(r"c:/temp/BasePortaldaTransparenciaDividaAtiva.csv", 
                 encoding="latin1", sep=";")

# Mantendo apenas as colunas desejadas
df = df[["CpfCnpjDevedor", "NomeDevedor", "ValorTotal"]]

# Aplicando a máscara
df["CpfCnpjDevedor"] = df["CpfCnpjDevedor"].apply(mascarar_documento)

# Salvando resultado em UTF-8
df.to_csv(r"c:\temp\arquivo_final.csv", index=False, encoding="utf-8", sep=';')
