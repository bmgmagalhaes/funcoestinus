from zipfile import ZipFile, is_zipfile
# from rarfile import RarFile, is_rarfile
import os

#VERIFICANDO SE TEM ARQUIVO ZIP
def verificar_arquivo_zip(diretorio, lista_arquivos):

    for arquivo in lista_arquivos:
        caminho_completo = os.path.join(diretorio, arquivo)
        if is_zipfile(caminho_completo):
            return True
    return False

#VERIFICANDO SE TEM ARQUIVO RAR
# def verificar_arquivo_rar(diretorio, lista_arquivos):
#
#     for arquivo in lista_arquivos:
#         caminho_completo = os.path.join(diretorio, arquivo)
#         if is_rarfile(caminho_completo):
#             return True
#     return False

# DESCOMPACTANDO ARQUIVOS ZIP
def descompactar_arquivo(diretorio, lista_arquivos):
    tem_zip = verificar_arquivo_zip(diretorio, lista_arquivos)
    while tem_zip:
        for arquivo in lista_arquivos:
            caminho_completo = os.path.join(diretorio, arquivo)
            if is_zipfile(caminho_completo):
                with ZipFile(caminho_completo, 'r') as retornos:
                    retornos.extractall(diretorio)

                os.remove(caminho_completo)

        lista_arquivos = os.listdir(diretorio)
        tem_zip = verificar_arquivo_zip(diretorio, lista_arquivos)


# DESCOMPACTANDO ARQUIVOS RAR
# def descompactar_arquivo_rar(diretorio, lista_arquivos):
#     tem_rar = verificar_arquivo_rar(diretorio, lista_arquivos)
#     print('tem rar',tem_rar)
#     print('diretorio',diretorio, 'lista_arquivos',lista_arquivos)
#     while tem_rar:
#         for arquivo in lista_arquivos:
#             print('arquivo',arquivo)
#             caminho_completo = os.path.join(diretorio, arquivo)
#             print('caminho_completo',caminho_completo)
#             if is_rarfile(caminho_completo):
#                 print('eh rar. Vai entrar em RarFile')
#                 with RarFile(caminho_completo, 'r') as retornos:
#                     print('Dentro RarFile')
#                     print('diretorio',diretorio)
#                     retornos.extractall(diretorio)
#                     print('Extraido')
#
#                 os.remove(caminho_completo)
#
#         lista_arquivos = os.listdir(diretorio)
#         tem_rar = verificar_arquivo_rar(diretorio, lista_arquivos)
#
