"""
Script destinado a obter valores manuais informados em um arquivo csv para criar um arquivo retorno 
bancário pra inserir na arrecadação, obedecendo o layout padrão do banco
"""

DIRETORIO = rf"C:\temp"

# Conteúdo da primeira linha do arquivo a ser gerado
HEADER = 'A0000000              NOME DO MUNICIPIO BR001BANCO DO BRASIL  S/A2026000000000000                                                                     '


################################################ Partes fixas do detalhe que ficam entre os dados variáveis. ################################################
# Do início até data do pagamento e regime de caixa
SEGUIMENTO_1 ='G_______________     '

# Das datas até o nosso número
SEGUIMENTO_2 ='___________________________'

# Do valor pago, até o final do arquivo
SEGUIMENTO_3 ='___________________    3________________       1         '

def carregar_arquivo_origem() -> list:
    """
    Carrega o arquivo com as informações de pagamentos a serem criados
    """
    with open(rf"{DIRETORIO}\inserir_pagamentos.csv", "r") as pagamentos_informados:
        linha_0 =pagamentos_informados.readline() 
        linhas = pagamentos_informados.readlines() 

    detalhe = [linha.strip().split(';') for linha in linhas]
    return detalhe

def converter_pagamentos_layout_agz(pagamentos_para_inserir) -> list:
    """
    Formata os pagamentos lidos no arquivo csv para o layout do retorno bancário que será incluído na arrecadação
    Retorna lista com os pagamento e o valor total pago pra ser inserido no trailer do arquivo
    """

    # Lista com todos os registros formatados pra incluir no arquivo a ser gerado
    pagamentos_com_layout_agz = []
    data_retorno = ''
    valor_total = 0

    for pagamento in pagamentos_para_inserir:
        
        # grava data pra nomear retorno
        data_retorno = pagamento[0][2:]

        # Normaliza o valor pago e retorna total numérico para o total do trailer e como string ajustar detalhe do retorno
        valor_numerico, pagamento[-1] = normalizar_valor(pagamento[-1])
        valor_total += valor_numerico

        # Concatena os seguimentos fixos com os valores variaveis:
        # [0] = Data do pagamento
        # [1] = Data do regime de caixa (repete o valor da data do pagamento [0]). Se for usar, adicionar coluna e trocar o índice pra 1
        # [2] = Nosso número
        # [3] = Valor (incrementando '0' à esquerda até completar 18 casas)
        pagamentos_com_layout_agz.append(
            SEGUIMENTO_1+
            pagamento[0]+
            pagamento[0]+
            SEGUIMENTO_2+
            pagamento[1]+
            pagamento[-1].zfill(18)+
            SEGUIMENTO_3
            )

    return pagamentos_com_layout_agz, str(valor_total).replace('.',''), data_retorno
        
def criar_trailer(pagamentos, valor_total) -> str:
    """
    Cria a última linha do arquivo retorno
    """
    trailer = 'Z'
    
    total_de_linhas = str(len(pagamentos)).zfill(6)

    total_pago = str(valor_total).zfill(17)

    trailer += total_de_linhas+total_pago

    return trailer

def normalizar_valor(valor_str: str):
    """
    Converte uma string representando um valor monetário para float,
    tratando diferentes formatos de entrada e retornando também a versão
    sem ponto para o layout bancário.
    """
    valor_str = valor_str.strip()

    # Substitui vírgula por ponto
    if "," in valor_str:
        valor_str = valor_str.replace(",", ".")
    elif "." not in valor_str:
        valor_str = valor_str + ".00"

    # Converte para float
    valor_float = float(valor_str)

    # Garante duas casas decimais na string
    valor_str_formatado = f"{valor_float:.2f}"

    # Remove o ponto para o layout
    valor_sem_ponto = valor_str_formatado.replace(".", "")

    return valor_float, valor_sem_ponto

    """
    Converte uma string representando um valor monetário para float,
    tratando diferentes formatos de entrada.

    Regras de conversão:
    - Se a string contiver vírgula, ela é substituída por ponto.
      Exemplo: "688,54" -> 688.54
    - Se a string contiver ponto, é usada diretamente.
      Exemplo: "688.54" -> 688.54
    - Se a string não contiver vírgula nem ponto, assume-se que é um valor inteiro em reais
      e são adicionadas duas casas decimais (.00).
      Exemplo: "123" -> 123.00
    """

    # Remove espaços
    valor_str = valor_str.strip()
    # Se tiver vírgula, troca por ponto
    if "," in valor_str:
        valor_str = valor_str.replace(",", ".")
    # Se não tiver vírgula nem ponto, assume que é inteiro em reais
    elif "." not in valor_str:
        valor_str = valor_str + ".00"

    return float(valor_str), valor_str.replace('.','')

def montar_retorno_final():
    """
    Executa todas as funções e gera o retorno final
    """

    pagamentos_para_inserir = carregar_arquivo_origem()
    pagamentos_com_layout_agz, valor_total, data_retorno = converter_pagamentos_layout_agz(pagamentos_para_inserir)
    trailer = criar_trailer(pagamentos_com_layout_agz, valor_total)


    with open(rf"{DIRETORIO}\MR{data_retorno}.ret", "w+") as criar_arquivo:
        criar_arquivo.write(HEADER + "\n")
        for linha in pagamentos_com_layout_agz:
            criar_arquivo.write(linha + "\n")
        criar_arquivo.write(trailer)

    
if __name__ == '__main__':
    montar_retorno_final()