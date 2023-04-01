import os

from .dados_acesso import usuario, senha, servidor, DIRETORIO
from imap_tools import MailBox, AND, MailMessageFlags
from .arrecadacao_paulista import executar_paulista
from .arrecadacao_goiana import executar_goiana
from .arrecadacao_messias_targino import executar_messias_targino
from .arrecadacao_passa_e_fica import executar_passa_e_fica
from .arrecadacao_sao_bento_do_norte import executar_sao_bento_do_norte
from .arrecadacao_patu import executar_patu
from .arrecadacao_sao_miguel_do_gostoso import executar_sao_miguel_do_gostoso
from .arrecadacao_timbauba import executar_timbauba
from .arrecadacao_goianinha import executar_goianinha
from .arrecadacao_lagoa_danta import executar_lagoa_danta
from .arrecadacao_santa_cruz import executar_santa_cruz_do_capibaribe
from .arrecadacao_lucena import executar_lucena
from .arrecadacao_galinhos import executar_galinhos



if __name__ == '__main__':
    def baixar_arquivos(pasta):

        try:
            print("Entrei no Try do Baixar Arquivos")
            os.mkdir(pasta)
        except:
            print("Pasta existente")
        
        
        for anexo in msg.attachments:
            print("anexo", anexo)
            caminho_completo = os.path.join(pasta, anexo.filename)
        
            with open(caminho_completo, 'wb') as download:
                download.write(anexo.payload)
        
        #CONFIRMAR E-MAIL COMO LIDO APÓS BAIXAR RETORNO
        meu_email.flag(msg.uid, MailMessageFlags.SEEN, True)

    with MailBox(servidor).login(usuario, senha) as meu_email:
        for msg in meu_email.fetch(AND(seen=False), mark_seen=False):
            assunto = msg.subject.lower()
            remetente = msg.from_.lower()

            if 'paulista' in assunto:
                pasta_municipio = DIRETORIO + rf"\Paulista"
                baixar_arquivos(pasta_municipio)
                executar_paulista(pasta_municipio)
                continue

            if 'arquivo' in assunto:
                pasta_municipio = DIRETORIO + rf"\Goiana"
                baixar_arquivos(pasta_municipio)
                executar_goiana(pasta_municipio)
                continue

            if 'retorn' in assunto and 'willian' in remetente:
                pasta_municipio = DIRETORIO + rf"\Passa e Fica"
                baixar_arquivos(pasta_municipio)
                executar_passa_e_fica(pasta_municipio)
                continue

            if ('baixa' in assunto or 'retorno' in assunto) and 'semutsp@gmail.com' in remetente:
                pasta_municipio = DIRETORIO + rf"\Sao Bento do Norte"
                baixar_arquivos(pasta_municipio)
                executar_sao_bento_do_norte(pasta_municipio)
                continue

            if ('arquivo' in assunto or 'retorno' in assunto) and 'prefeiturapatu@gmail.com' in remetente:
                pasta_municipio = DIRETORIO + rf"\Patu"
                baixar_arquivos(pasta_municipio)
                executar_patu(pasta_municipio)
                continue

            if 'messias' in assunto and 'retorno' in assunto:
                pasta_municipio = DIRETORIO + rf"\Messias Targino"
                baixar_arquivos(pasta_municipio)
                executar_messias_targino(pasta_municipio)
                continue

            if 'retorno' in assunto and 'tributos.smg@gmail.com' in remetente:
                pasta_municipio = DIRETORIO + rf"\Sao Miguel do Gostoso"
                baixar_arquivos(pasta_municipio)
                executar_sao_miguel_do_gostoso(pasta_municipio)
                continue

            if 'timbauba' in assunto and 'tributacao2021tb@hotmail.com' in remetente:
                pasta_municipio = DIRETORIO + rf"\Timbauba dos Batistas"
                baixar_arquivos(pasta_municipio)
                executar_timbauba(pasta_municipio)
                continue

            if 'paga' in assunto and 'financeirolagoadantarn@gmail.com' in remetente:
                pasta_municipio = DIRETORIO + rf"\Lagoa Danta"
                baixar_arquivos(pasta_municipio)
                executar_lagoa_danta(pasta_municipio)
                continue

            if 'scc' in assunto:
                pasta_municipio = DIRETORIO + rf"\Santa Cruz do Capibaribe"
                baixar_arquivos(pasta_municipio)
                executar_santa_cruz_do_capibaribe(pasta_municipio)
                continue

            if 'arre' in assunto and ('tributacao@goianinha.rn.gov.br' in remetente or
                                      'carolinesemtri1@gmail.com' in remetente):
                pasta_municipio = DIRETORIO + rf"\Goianinha"
                baixar_arquivos(pasta_municipio)
                executar_goianinha(pasta_municipio)
                continue

            if ('arrecada' in assunto or 'baixa de arq' in assunto ) and ('suporte@tinus.com.br' in remetente):
                pasta_municipio = DIRETORIO + rf"\Lucena"
                baixar_arquivos(pasta_municipio)
                executar_lucena(pasta_municipio)
                continue
            
            if 'arquivo de retorno' in assunto:
                pasta_municipio = DIRETORIO + rf"\Galinhos"
                baixar_arquivos(pasta_municipio)
                executar_galinhos(pasta_municipio)
                continue

    # os.system('explorer c:\Temp')
