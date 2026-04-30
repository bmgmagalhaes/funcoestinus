import os
import shutil
import time

municipios = {
    "CEA": [r"H:\Arqs\DamReg\Retorno TIVIT\CEA\ARRECADACAO"],
    "EXT": [r"H:\Arqs\DamReg\Retorno TIVIT\EXT\ARRECADACAO"],
    "GAV": [r"H:\Arqs\DamReg\Retorno TIVIT\GAV\ARRECADACAO"],
    "SMG": [r"H:\Arqs\DamReg\Retorno TIVIT\SMG\ARRECADACAO"],
    "PAR": [
        r"H:\Arqs\DamReg\Retorno TIVIT\PAR\ARRECADACAO",
        r"H:\Arqs\DamReg\Retorno TIVIT\PAR\COBRANCA_IPTU\RETORNO",
        r"H:\Arqs\DamReg\Retorno TIVIT\PAR\FMS\RETORNO",
        r"H:\Arqs\DamReg\Retorno TIVIT\PAR\TRASPORTE\RETORNO"
    ]
}

destino_base = r"D:\Prefeituras"

# Quantos dias considerar como "recentes"
dias_recentes = 5
limite_tempo = time.time() - (dias_recentes * 86400)

def eh_definitivo(caminho_arquivo):
    """Verifica se o arquivo é definitivo pelo conteúdo da segunda linha"""
    try:
        with open(caminho_arquivo, "r", encoding="utf-8", errors="ignore") as f:
            linhas = f.readlines()
            if len(linhas) >= 2:
                segunda_linha = linhas[1].rstrip("\n\r")
                
                if segunda_linha.startswith("G"):
                    # pega o caractere logo após o G
                    prox_char = segunda_linha[1] if len(segunda_linha) > 1 else " "
                    if prox_char == " ":
                        return False  # temporário
        return True
    except Exception as e:
        print(f"Erro ao ler {caminho_arquivo}: {e}")
        return False




def copiar_retornos():
    for sigla, origens in municipios.items():
        destino = os.path.join(destino_base, sigla)
        os.makedirs(destino, exist_ok=True)
        
        for origem in origens:
            if os.path.exists(origem):
                print(f"\nVerificando pasta: {origem}")
                arquivos = os.listdir(origem)

                for arquivo in arquivos:
                    if arquivo.lower().endswith(".ret"):
                        caminho_origem = os.path.join(origem, arquivo)
                        mod_time = os.path.getmtime(caminho_origem)

                        if mod_time >= limite_tempo and eh_definitivo(caminho_origem):
                            caminho_destino = os.path.join(destino, arquivo)
                            shutil.copy(caminho_origem, caminho_destino)
                            print(f"Copiado: {caminho_origem} -> {caminho_destino}")
                        else:
                            print(f"Ignorado (antigo ou temporário): {caminho_origem}")
            else:
                print(f"A pasta {origem} não existe!")

if __name__ == "__main__":
    copiar_retornos()
