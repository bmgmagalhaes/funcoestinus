import os
import shutil

# Variáveis globais
ORIGEM_PREFIXO = r"H:\Arqs"
ORIGEM_SUFIXO = r"\arquivoretorno"

DESTINO_PREFIXO = r"D:\Prefeituras"
DESTINO_SUFIXO = r"\ARRECADA"

# Lista de municípios (adicione mais siglas conforme necessário)
municipios = ["PAR", "RDF", "SMG", "GAV", "CEA", "CAI", "EXT", "ANG", 
              "CRV", "EQU", "GAL", "JDS", "LAJ", "NIS", "OUR", "PAV",
              "PUR", "STM"]

def copiar_simples():
    pastas_sem_copia = []

    for sigla in municipios:
        origem = f"{ORIGEM_PREFIXO}\\{sigla}{ORIGEM_SUFIXO}"
        destino = f"{DESTINO_PREFIXO}\\{sigla}{DESTINO_SUFIXO}"

        if not os.path.exists(origem):
            print(f"A pasta de origem {origem} não existe!")
            pastas_sem_copia.append(sigla)
            continue

        os.makedirs(destino, exist_ok=True)

        print(f"\nVerificando subpastas de {sigla} em {origem}...")

        copiou_algum = False
        for item in os.listdir(origem):
            caminho_item = os.path.join(origem, item)
            destino_item = os.path.join(destino, item)

            # Verifica se é uma pasta cujo nome é só números (ex.: 260224)
            if os.path.isdir(caminho_item) and item.isdigit():
                shutil.copytree(caminho_item, destino_item, dirs_exist_ok=True)
                print(f"Copiado: {caminho_item} -> {destino_item}")
                copiou_algum = True

        if not copiou_algum:
            pastas_sem_copia.append(sigla)

    # Aviso final
    if pastas_sem_copia:
        print("\nAviso: Nenhuma subpasta do Simples Nacional foi copiada para:")
        for sigla in pastas_sem_copia:
            print(f"- {sigla}")
    else:
        print("\nTodas as pastas tiveram subpastas copiadas com sucesso.")

if __name__ == "__main__":
    copiar_simples()
