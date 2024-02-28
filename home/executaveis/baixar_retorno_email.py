from imap_tools import MailBox, AND, MailMessageFlags
import os

from renomear_arquivo_retorno import renomear_retorno
from dados_acesso import usuario, senha, servidor, DIRETORIO


if __name__ == '__main__':
    def baixar_arquivos(pasta):

        try:
            os.mkdir(pasta)
        except:
            print("Pasta existente")
        

        for anexo in msg.attachments:
            caminho_completo = os.path.join(pasta, anexo.filename)
        
            with open(caminho_completo, 'wb') as download:
                download.write(anexo.payload)
        
        #CONFIRMAR E-MAIL COMO LIDO APÓS BAIXAR RETORNO
        meu_email.flag(msg.uid, MailMessageFlags.SEEN, True)

    with MailBox(servidor).login(usuario, senha) as meu_email:
        for msg in meu_email.fetch(AND(seen=False), mark_seen=False):
            assunto = msg.subject.lower()
            remetente = msg.from_.lower()
            
            
            if 'retorno' in assunto and 'paulista' in assunto and 'suporte@tinus.com.br' in remetente:
                    municipio = 'Paulista'

            elif 'goiana' in assunto and 'suporte@tinus.com.br' in remetente:
                municipio = 'Goiana'

            elif 'arq' in assunto and 'retorn' in assunto and 'willian' in remetente:
                municipio = 'Passa e Fica'
                
            elif ('baixa' in assunto or 'retorno' in assunto) and 'semutsp@gmail.com' in remetente:
                municipio = 'Sao Bento do Norte'
                
            elif ('arquivo' in assunto or 'retorno' in assunto) and 'prefeiturapatu@gmail.com' in remetente:
                municipio = 'Patu'
                
            elif 'messias' in assunto and 'retorno' in assunto:
                municipio = 'Messias Targino'
                
            elif ('retorno' in assunto or 'remessa' in assunto) and 'tributos.smg@gmail.com' in remetente:
                municipio = 'Sao Miguel do Gostoso'
                
            elif ('timba' in assunto or 'retor' in assunto) and 'tributacao2021tb@hotmail.com' in remetente:
                municipio = 'Timbauba dos Batistas'
                
            elif 'paga' in assunto and 'financeirolagoadantarn@gmail.com' in remetente:
                municipio = 'Lagoa Danta'
            
            elif 'tributacao@serranegra.rn.gov.br' in remetente or ('negra' in assunto and 'suporte@tinus.com.br' in remetente):
                municipio = 'Serra Negra do Norte'

            elif 'scc' in assunto and 'ret' in assunto and 'suporte@tinus.com.br' in remetente:
                municipio = 'Santa Cruz do Capibaribe'

            elif 'goiani' in assunto and ('tributacao@goianinha.rn.gov.br' in remetente or
                                    'carolinesemtri1@gmail.com' in remetente or
                                    'suporte@tinus.com.br' in remetente):
                municipio = 'Goianinha'
            
            elif ('arrecada' in assunto or 'baixa' in assunto or 'luc' in assunto) and ('suporte@tinus.com.br' in remetente):
                municipio = 'Lucena'
            
            elif ('ret' in assunto or 'arq' in assunto) and ('sectributos@galinhos.rn.gov.br' in remetente):
                municipio = 'Galinhos'

            elif ('retorno' in assunto or 'baixa de arq' in assunto) and ('datbananeiras@gmail.com' in remetente):
                municipio = 'Bananeiras'

            elif 'tributacao@pmsenadorgeorginoavelino.rn.gov.br' in remetente:
                municipio = 'Georgino'

            elif ('Serra do Mel' in assunto or 'arq' in assunto):
                municipio = 'Serra do Mel'
            

            if municipio:            
                pasta_municipio = DIRETORIO + rf"\{municipio}"
                baixar_arquivos(pasta_municipio)
                renomear_retorno(pasta_municipio, municipio)
                tem_retorno, municipio = True, ''
                os.system(f'explorer {pasta_municipio}')
        
    temp = ("Pressione enter pra encerrar:")
