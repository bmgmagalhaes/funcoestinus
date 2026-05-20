from django.shortcuts import render, redirect
from django.contrib import messages
from imap_tools import MailBox, AND, MailMessageFlags
import os
import imaplib
import email
from datetime import datetime
from .executaveis.dados_acesso import usuario, senha, servidor, DIRETORIO
from .executaveis.retorno_config import lista_municipios_renomear_off_line
from .executaveis import utilitarios
from .executaveis.transferencia_mdinin import transferir_pagamento, listar_pagamentos, transferir_md
from .executaveis.salvar_valores_de_globais import listar_regitros, executar_salvar_global
from .executaveis.de_para_pagamento import carregar_situacao_atual_do_imovel_para, gravar_globais_com_pagamentos
from .executaveis.funcoes_compensacao_de_pagamento import unidades_fiscais, configurando_extrato, configurando_pagamentos
from .executaveis.funcoes_compensacao_de_pagamento import multa_juros, cruzando_dados_extrato_pagamento
from .executaveis.funcoes_compensacao_de_pagamento import extrato_com_valores_em_aberto, executar_compensacao
from .executaveis.juncao_agz import unir_agz
from .executaveis.gerar_relatorio_divida_ativa_sjm import funcao_ajustar_relario_da_sjm
from .executaveis.mascara_relatorio_da_transparencia import mascarar_dados_da_divida_ativa
from .executaveis.juncao_agz_de_um_dia import unir_agz_de_um_dia
from .executaveis.renomear_arquivo_retorno import renomear_retorno
from email.header import decode_header

def decode_subject(subject_raw):
    decoded_parts = decode_header(subject_raw)
    subject = ""
    for part, encoding in decoded_parts:
        if isinstance(part, bytes):
            subject += part.decode(encoding or "utf-8", errors="ignore")
        else:
            subject += part
    return subject


def renomear(request, municipio):
    
    municipio = lista_municipios_renomear_off_line.get(municipio)
    
    if municipio:
        renomear_retorno(DIRETORIO, municipio)
    else:
        messages.error(request, f'Função pra o município "{municipio}" não implementada')
    return redirect('index')

def index(request):
    return render(request, 'home/index.html')


def bb_sia_config(request):
    return render(request, 'home/bb_sia_configuracao.html')

def globais_e_manuais(request):
    return render(request, 'home/globais_e_manuais.html')

def juncao_agz(request):
    unir_agz(DIRETORIO)
    return redirect('index')

def estoque_divida_ativa_sao_jose_de_mipibu(request):
    funcao_ajustar_relario_da_sjm(DIRETORIO)
    return redirect('index')

def mascarar_dados_para_portal_transparencia(request):
    mascarar_dados_da_divida_ativa(DIRETORIO)
    return redirect('index')

def juncao_agz_de_um_dia(request):
    unir_agz_de_um_dia(DIRETORIO)
    return redirect('index')

def transferencia_pagamento(request):
    if request.method != 'POST':
        return render(request, 'home/listar_pagamento.html')
    sequencial_de = request.POST.get('sequencial_de')
    sequencial_para = request.POST.get('sequencial_para')
    namespace = request.POST.get('namespace')
    pagamentos_para_transferir = request.POST.get('pagamentos_para_transferir')

    messages.success(request, f"Transferido o(s) pagamento(s) do sequencial {sequencial_de} "
                              f"para o sequencial {sequencial_para} em {namespace}")
    md_completo = transferir_pagamento(namespace, sequencial_de, sequencial_para, pagamentos_para_transferir)

    # return render(request, 'home/index.html')
    return render(request, 'home/transferencia_pagamento_md.html', 
                  {
                      'md': md_completo,
                      'contribuinte_de':sequencial_de,
                      'contribuinte_para':sequencial_para,
                      'namespace': namespace,
                  }
                  )

def transferencia_pagamento_md(request):
    if request.method != 'POST':
        return render(request, 'home/transferencia_pagamento_md.html')
    contribuinte_para = request.POST.get('contribuinte_para')
    namespace = request.POST.get('namespace')
    md_completo = request.POST.get('md')

    modelo_para = request.POST.get('modelo_para')
    parcela_para = request.POST.get('parcela_para')

    print("Onde estou? VIEW")
    print(__name__)

    print(f'contribuinte_para: {contribuinte_para}')
    print(f'namespace: {namespace}')
    print(f'md_completo: {md_completo}')
    print(f'modelo_para: {modelo_para}')
    print(f'parcela_para: {parcela_para}')

    return render(request, 'home/transferencia_pagamento_md.html')

def exibir_pagamentos(request):
    if request.method != 'POST':
        return render(request, 'home/listar_pagamento.html')
    sequencial_de = request.POST.get('sequencial_de')
    namespace = request.POST.get('namespace')

    pagamentos = listar_pagamentos(namespace, sequencial_de)
    pagamentos = pagamentos.replace(f'^MDININ(1{sequencial_de}', '')
    pagamentos = pagamentos.replace(',101', 'IPTU Atual: ')
    pagamentos = pagamentos.replace(',102', 'Alvará Atual: ')
    pagamentos = pagamentos.replace(',103', 'ITBI: ')
    pagamentos = pagamentos.replace(',104', 'ISSQN: ')
    pagamentos = pagamentos.replace(',106', 'IPTU Anterior: ')
    pagamentos = pagamentos.replace(',107', 'Alvará Ant: ')
    pagamentos = pagamentos.replace(',108', 'Modelo 08: ')
    pagamentos = pagamentos.replace(',110', 'ISS (NFS/NFA): ')
    pagamentos = pagamentos.replace(',112', 'Outros Créditos: ')

    corte = pagamentos.find(')')
    tem_data = True

    while tem_data:
        data = pagamentos[corte - 13:corte - 7]
        try:
            pagamentos = pagamentos.replace(data, datetime.strptime(data, "%y%m%d").strftime("%d/%m/%y") + " NREG ")
        except:
            pass
        corte = pagamentos.find(')', corte + 4)
        if corte == -1:
            tem_data = False

    return render(request, 'home/listar_pagamento.html',
                  {"pagamentos": pagamentos, "sequencial_de": sequencial_de, "namespace": namespace})

def listar_global(request):
    if request.method != 'POST':
        return render(request, 'home/salvar_global.html')
    namespace = request.POST.get('namespace')
    mascara = request.POST.get('mascara')
    registros = listar_regitros(namespace, mascara)

    return render(request, 'home/salvar_global.html',
                  {
                      "registros": registros, "namespace": namespace, "mascara": mascara,
                  })

def salvar_global(request):
    if request.method != 'POST':
        return render(request, 'home/salvar_global.html')
    namespace = request.POST.get('namespace')
    mascara = request.POST.get('mascara')
    linha = request.POST.get('linha')
    excluir = False
    if request.POST.get('excluir') == 'excluir':
        excluir = True

    executar_salvar_global(namespace, mascara, linha, excluir)
    return render(request, 'home/salvar_global.html')

def de_para_pagamentos(request):
    if request.method != 'POST':
        return render(request, 'home/de_para_pagamento.html')

    sequencial = request.POST.get('sequencial')
    namespace = request.POST.get('namespace')

    extrato_anterior, pagamentos_anterior, extrato_atual, pagamentos_atual, uf, parametros_acrescimos = carregar_situacao_atual_do_imovel_para(
        sequencial, namespace)


    extrato_anterior = configurando_extrato(extrato_anterior)
    extrato_atual = configurando_extrato(extrato_atual)
    extrato_geral = {}
    extrato_geral.update(extrato_anterior)
    extrato_geral.update(extrato_atual)

    pagamentos_anterior = configurando_pagamentos(pagamentos_anterior)
    pagamentos_atual = configurando_pagamentos(pagamentos_atual)
    pagamentos_formatados_geral = []
    if pagamentos_anterior:
        pagamentos_formatados_geral = pagamentos_anterior
    if pagamentos_atual:

        for cada_pagamento_atual in pagamentos_atual:

            pagamentos_formatados_geral.append(cada_pagamento_atual)

    uf = unidades_fiscais(uf)
    multa, limite_multa, juros = multa_juros(parametros_acrescimos)

    extrato_detalhado = cruzando_dados_extrato_pagamento(extrato_geral, pagamentos_formatados_geral)

    debitos_em_aberto = extrato_com_valores_em_aberto(extrato_detalhado)

    return render(request, 'home/escolher_parcelas.html',
                  {"extrato": debitos_em_aberto, "sequencial": sequencial, "namespace": namespace,
                   "multa":multa, "limite_multa":limite_multa, "juros":juros, "uf": uf})

def escolher_parcelas(request):

    if request.method != 'POST':
        return render(request, 'home/escolher_parcelas.html')

    sequencial = request.POST.get('sequencial')
    namespace = request.POST.get('namespace')
    extrato = request.POST.get('extrato')
    multa = request.POST.get('multa')
    limite_multa = request.POST.get('limite_multa')
    juros = request.POST.get('juros')
    uf = request.POST.get('uf')

    # MÉTODO PRA GERAR UMA LISTA COM TODOS OS 'VALUES' (EXERCÍCIO PARCELA) DE CHECKBOX SELECIONADOS
    parcelas = request.POST.getlist('compensar')

    # TRASFORMANDO VALORES DO CHECKBOX EM LISTAS
    for ind in range(0, len(parcelas)):
        parcelas[ind] = parcelas[ind].split(" ")

    # TRASFORMANDO LISTAS EM UM DICIONÁRIO
    compensar = {}
    for item in parcelas:
        if compensar.get(item[0]):
            compensar[item[0]].append(item[1])
        else:
            compensar[item[0]] = [item[1]]


    return render(request, 'home/informar_creditos.html',
    {"extrato": extrato, "sequencial": sequencial, "namespace": namespace,
     "multa": multa, "limite_multa": limite_multa, "juros": juros, "uf": uf,
     "compensar":compensar})

def informar_creditos(request):
    if request.method != 'POST':
        return render(request, 'home/informar_creditos.html')

    sequencial = request.POST.get('sequencial')
    namespace = request.POST.get('namespace')
    extrato = request.POST.get('extrato')
    multa = request.POST.get('multa')
    limite_multa = request.POST.get('limite_multa')
    juros = request.POST.get('juros')
    uf = request.POST.get('uf')
    compensar = request.POST.get('compensar')

    data = request.POST.get('data')
    valor = utilitarios.converter_string_float_valor(request.POST.get('valor'))
    orgao = request.POST.get('orgao')

    credito = utilitarios.converter_string_lista_credito(request.POST.get('credito'))


    credito.append([data,valor,orgao])

    return render(request, 'home/informar_creditos.html',
                  {
                   "extrato": extrato, "sequencial": sequencial, "namespace": namespace,
                   "multa": multa, "limite_multa": limite_multa, "juros": juros, "uf": uf,
                   "compensar": compensar, "credito": credito,
                   })

def resumo_compensacao(request):
    if request.method != 'POST':
        return render(request, 'home/resumo_compensacao.html')

    sequencial = request.POST.get('sequencial')
    namespace = request.POST.get('namespace')
    extrato = request.POST.get('extrato')
    multa = request.POST.get('multa')
    limite_multa = request.POST.get('limite_multa')
    juros = request.POST.get('juros')
    uf = request.POST.get('uf')

    credito = utilitarios.converter_string_lista_credito(request.POST.get('credito'))
    compensar = utilitarios.converter_string_dicionario_compensar(request.POST.get('compensar'))



    return render(request, 'home/resumo_compensacao.html',
                  {
                      "extrato": extrato, "sequencial": sequencial, "namespace": namespace,
                      "multa": multa, "limite_multa": limite_multa, "juros": juros, "uf": uf,
                      "compensar": compensar, "credito": credito,
                  })

def gerar_globais_pagamentos(request):
    if request.method != 'POST':
        return render(request, 'home/gerar_globais_pagamentos.html')

    sequencial = request.POST.get('sequencial')
    namespace = request.POST.get('namespace')
    multa = request.POST.get('multa')
    limite_multa = request.POST.get('limite_multa')
    juros = request.POST.get('juros')

    extrato = utilitarios.converter_string_dicionario_extrato(request.POST.get('extrato'))
    uf = utilitarios.converter_string_dicionario_uf(request.POST.get('uf'))
    credito = utilitarios.converter_string_lista_credito(request.POST.get('credito'))
    compensar = utilitarios.converter_string_dicionario_compensar(request.POST.get('compensar'))

    registrar_global, credito_restante, debito_restante = \
        executar_compensacao(extrato, uf, multa, limite_multa, juros, compensar, credito, namespace, sequencial)

    return render(request, 'home/gerar_globais_pagamentos.html',
                  {
                      "sequencial": sequencial, "namespace": namespace,
                      "globais" : registrar_global, "saldo_credito": credito_restante,
                      "saldo_debito": debito_restante
                  })

def gravar_globais_pagamentos(request):
    if request.method != 'POST':
        return render(request, 'home/gerar_globais_pagamentos.html')

    namespace = request.POST.get('namespace')
    globais = request.POST.get('globais')

    globais = utilitarios.converter_string_dicionario_globais(globais)

    gravar_globais_com_pagamentos(namespace, globais)

    return render(request, 'home/gerar_globais_pagamentos.html')

def baixar_retorno_beta(request):
    # Configurações do servidor IMAP
    IMAP_SERVER = servidor
    EMAIL = usuario
    PASSWORD = senha

    # Conecta-se ao servidor IMAP
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL, PASSWORD)

    # Seleciona a caixa de entrada (ou outra pasta se preferir)
    mail.select('inbox')

    # Pesquisa por e-mails não lidos (ou outros critérios de pesquisa)
    status, email_ids = mail.search(None, '(UNSEEN)')

    # Itera sobre os e-mails encontrados
    for email_id in email_ids[0].split():
        status, email_data = mail.fetch(email_id, '(RFC822)')
        raw_email = email_data[0][1]
        msg = email.message_from_bytes(raw_email)

        # Remetente
        remetente = (msg['From'] or "").lower()

        # Assunto decodificado
        assunto_raw = msg['Subject'] or ""
        assunto = decode_subject(assunto_raw).lower()

        # Marca como não lido
        mail.store(email_id, '-FLAGS', '\\Seen')

        if msg.get_content_maintype() == 'multipart':
            print(f"De: {remetente} | Assunto: {assunto}")
            municipio = ''
            
            if ('arquivo' in assunto or 'retorno' in assunto) and 'prefeiturapatu@gmail.com' in remetente:
                municipio = 'Patu'
                
            elif 'tributacao@serranegra.rn.gov.br' in remetente:
                municipio = 'Serra Negra do Norte'

            elif ('goiani' in assunto or 'arreca' in assunto) and ('tributacao@goianinha.rn.gov.br' in remetente or
                                    'carolinesemtri1@gmail.com' in remetente):
                municipio = 'Goianinha'
            
            elif ('arrec' in assunto) and ('receita.lucena.pb@gmail.com' in remetente or 'suporte' in remetente):
                municipio = 'Lucena'     
       
            elif ('retor' in assunto or 'baixa de arq' in assunto) and ('luiz' in remetente or 'datbananeiras@gmail.com' in remetente):
                municipio = 'Bananeiras'   
            
            elif ('goiana' in assunto and 'baixa' in assunto) and ('suporte' in remetente):
                municipio = 'Goiana'    
    
            
            if municipio:            
                pasta_municipio = DIRETORIO + rf"\{municipio}"                    
                try:
                    os.mkdir(pasta_municipio)
                except FileExistsError:
                    print("Pasta Existente não pode ser criada: ")
                
                for part in msg.walk():
                    if part.get_content_maintype() == 'multipart' or part.get('Content-Disposition') is None:
                        continue
                    # Baixa o anexo para um diretório
                    filename = part.get_filename()
                    if filename:
                        filepath = os.path.join(pasta_municipio, filename)
                        with open(filepath, 'wb') as f:
                            f.write(part.get_payload(decode=True))

                renomear_retorno(pasta_municipio, municipio)
                tem_retorno, municipio = True, ''
                messages.success(request, f'Arquivos baixados com sucesso em "{pasta_municipio}"')
                os.system(f'explorer {pasta_municipio}')

    # Fecha a conexão com o servidor IMAP
    mail.close()
    mail.logout()
    


    return redirect('index')