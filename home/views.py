from django.shortcuts import render, redirect
from django.contrib import messages
from imap_tools import MailBox, AND, MailMessageFlags
import os
from datetime import datetime
from .executaveis.dados_acesso import usuario, senha, servidor, DIRETORIO
from .executaveis import utilitarios
from .executaveis.arrecadacao_arez import executar_arez
from .executaveis.arrecadacao_bananeiras import executar_bananeiras
from .executaveis.arrecadacao_bodo import executar_bodo
from .executaveis.arrecadacao_paulista import executar_paulista
from .executaveis.arrecadacao_goiana import executar_goiana
from .executaveis.arrecadacao_messias_targino import executar_messias_targino
from .executaveis.arrecadacao_passa_e_fica import executar_passa_e_fica
from .executaveis.arrecadacao_sao_bento_do_norte import executar_sao_bento_do_norte
from .executaveis.arrecadacao_patu import executar_patu
from .executaveis.arrecadacao_sao_miguel_do_gostoso import executar_sao_miguel_do_gostoso
from .executaveis.arrecadacao_timbauba import executar_timbauba
from .executaveis.arrecadacao_goianinha import executar_goianinha
from .executaveis.arrecadacao_lagoa_danta import executar_lagoa_danta
from .executaveis.arrecadacao_santa_cruz import executar_santa_cruz_do_capibaribe
from .executaveis.arrecadacao_lucena import executar_lucena
from .executaveis.arrecadacao_nisia import executar_nisia
from .executaveis.arrecadacao_georgino_avelino import executar_georgino_avelino
from .executaveis.adicionar_iss_nisia import adicionar_iss
from .executaveis.adicionar_irrf_bananeiras import adicionar_irrf
from .executaveis import adicionar_iss_nisia
from .executaveis import adicionar_irrf_bananeiras
from .executaveis.transferencia_itbi import transferir_itbi
from .executaveis.transferencia_mdinin import transferir_pagamento, listar_pagamentos
from .executaveis.salvar_valores_de_globais import listar_regitros, executar_salvar_global
from .executaveis.de_para_pagamento import carregar_situacao_atual_do_imovel_para, gravar_globais_com_pagamentos
from .executaveis.funcoes_compensacao_de_pagamento import unidades_fiscais, configurando_extrato, configurando_pagamentos
from .executaveis.funcoes_compensacao_de_pagamento import multa_juros, cruzando_dados_extrato_pagamento
from .executaveis.funcoes_compensacao_de_pagamento import extrato_com_valores_em_aberto, executar_compensacao#, salvar_compensacao
from .executaveis.juncao_agz import unir_agz

def renomear(request, municipio):
    if municipio in 'pau':
        executar_paulista(DIRETORIO)
    elif municipio in 'scc':
        executar_santa_cruz_do_capibaribe(DIRETORIO)
    elif municipio in 'are':
        executar_arez(DIRETORIO)
    elif municipio in 'ban':
        executar_bananeiras(DIRETORIO)
    elif municipio in 'bod':
        executar_bodo(DIRETORIO)
    elif municipio in 'goi':
        executar_goiana(DIRETORIO)
    elif municipio in 'goh':
        executar_goianinha(DIRETORIO)
    elif municipio in 'lda':
        executar_lagoa_danta(DIRETORIO)
    elif municipio in 'luc':
        executar_lucena(DIRETORIO)
    elif municipio in 'mta':
        executar_messias_targino(DIRETORIO)
    elif municipio in 'nis':
        executar_nisia(DIRETORIO)
    elif municipio in 'pef':
        executar_passa_e_fica(DIRETORIO)
    elif municipio in 'pat':
        executar_patu(DIRETORIO)
    elif municipio in 'sbn':
        executar_sao_bento_do_norte(DIRETORIO)
    elif municipio in 'smg':
        executar_sao_miguel_do_gostoso(DIRETORIO)
    elif municipio in 'tdb':
        executar_timbauba(DIRETORIO)
    elif municipio in 'gav':
        executar_georgino_avelino(DIRETORIO)

    else:
        messages.error(request, f'Função pra o município "{municipio}" não implementada')
    return redirect('index')


def index(request):
    return render(request, 'home/index.html')


def baixar_retorno(request):
    def baixar_arquivos(pasta):
        try:
            os.mkdir(pasta)
        except Exception as e:
            print("Pasta existente", e)
        for anexo in msg.attachments:
            caminho_completo = os.path.join(pasta, anexo.filename)
            with open(caminho_completo, 'wb') as download:
                download.write(anexo.payload)
        # CONFIRMAR E-MAIL COMO LIDO APÓS BAIXAR RETORNO
        meu_email.flag(msg.uid, MailMessageFlags.SEEN, True)

    tem_retorno = False

    try:
        with MailBox(servidor).login(usuario, senha) as meu_email:
            for msg in meu_email.fetch(AND(seen=False), mark_seen=False):
                assunto = msg.subject.lower()
                remetente = msg.from_.lower()

                if 'retorno' in assunto and 'paulista' in assunto:
                    pasta_municipio = DIRETORIO + rf"\Paulista"
                    baixar_arquivos(pasta_municipio)
                    executar_paulista(pasta_municipio)
                    tem_retorno = True
                    continue

                if 'goiana' in assunto:
                    pasta_municipio = DIRETORIO + rf"\Goiana"
                    baixar_arquivos(pasta_municipio)
                    executar_goiana(pasta_municipio)
                    tem_retorno = True
                    continue

                if 'arq' in assunto and 'retorn' in assunto and 'willian' in remetente:
                    pasta_municipio = DIRETORIO + rf"\Passa e Fica"
                    baixar_arquivos(pasta_municipio)
                    executar_passa_e_fica(pasta_municipio)
                    tem_retorno = True
                    continue

                if ('baixa' in assunto or 'retorno' in assunto) and 'semutsp@gmail.com' in remetente:
                    pasta_municipio = DIRETORIO + rf"\Sao Bento do Norte"
                    baixar_arquivos(pasta_municipio)
                    executar_sao_bento_do_norte(pasta_municipio)
                    tem_retorno = True
                    continue

                if ('arquivo' in assunto or 'retorno' in assunto) and 'prefeiturapatu@gmail.com' in remetente:
                    pasta_municipio = DIRETORIO + rf"\Patu"
                    baixar_arquivos(pasta_municipio)
                    executar_patu(pasta_municipio)
                    tem_retorno = True
                    continue

                if 'messias' in assunto and 'retorno' in assunto:
                    pasta_municipio = DIRETORIO + rf"\Messias Targino"
                    baixar_arquivos(pasta_municipio)
                    executar_messias_targino(pasta_municipio)
                    tem_retorno = True
                    continue

                if 'retorno' in assunto and 'tributos.smg@gmail.com' in remetente:
                    pasta_municipio = DIRETORIO + rf"\Sao Miguel do Gostoso"
                    baixar_arquivos(pasta_municipio)
                    executar_sao_miguel_do_gostoso(pasta_municipio)
                    tem_retorno = True
                    continue

                if ('timba' in assunto or 'retor' in assunto) and 'tributacao2021tb@hotmail.com' in remetente:
                    pasta_municipio = DIRETORIO + rf"\Timbauba dos Batistas"
                    baixar_arquivos(pasta_municipio)
                    executar_timbauba(pasta_municipio)
                    tem_retorno = True
                    continue

                if 'paga' in assunto and 'financeirolagoadantarn@gmail.com' in remetente:
                    pasta_municipio = DIRETORIO + rf"\Lagoa Danta"
                    baixar_arquivos(pasta_municipio)
                    executar_lagoa_danta(pasta_municipio)
                    tem_retorno = True
                    continue

                if 'scc' in assunto and 'suporte@tinus.com.br' in remetente:
                    pasta_municipio = DIRETORIO + rf"\Santa Cruz do Capibaribe"
                    baixar_arquivos(pasta_municipio)
                    executar_santa_cruz_do_capibaribe(pasta_municipio)
                    tem_retorno = True
                    continue

                if 'arre' in assunto and ('tributacao@goianinha.rn.gov.br' in remetente or
                                          'carolinesemtri1@gmail.com' in remetente):
                    pasta_municipio = DIRETORIO + rf"\Goianinha"
                    baixar_arquivos(pasta_municipio)
                    executar_goianinha(pasta_municipio)
                    tem_retorno = True
                    continue

                if ('arrecada' in assunto or 'baixa' in assunto or 'luc' in assunto) and ('suporte@tinus.com.br' in remetente):
                    pasta_municipio = DIRETORIO + rf"\Lucena"
                    baixar_arquivos(pasta_municipio)
                    executar_lucena(pasta_municipio)
                    tem_retorno = True
                    continue

                if ('retorno' in assunto or 'baixa de arq' in assunto) and ('datbananeiras@gmail.com' in remetente):
                    pasta_municipio = DIRETORIO + rf"\Bananeiras"
                    baixar_arquivos(pasta_municipio)
                    executar_bananeiras(pasta_municipio)
                    tem_retorno = True
                    continue

        # os.system('explorer c:\Temp')


    except Exception as e:
        print(e)

    if not tem_retorno:
        messages.error(request, 'Nenhum e-mail com retorno encontrado')
        return redirect('index')
    else:
        messages.success(request, 'Arquivos baixados com sucesso em "c:/temp"')
    # os.system('explorer c:\Temp')
    os.system(f'explorer {pasta_municipio}')

    return redirect('index')


def iss_nisia(request):
    if request.method != 'POST':
        return render(request, 'home/adicionar_iss_nisiafloresta.html', {"namespace": adicionar_iss_nisia.url})

    data = datetime.strptime(request.POST.get('data').replace('-', ''), '%Y%m%d')
    valor = int(request.POST.get('valor'))
    messages.success(request, f"Adicionado o valor de R${(float(valor) / 100)} no dia "
                              f"{data.strftime('%d/%m/%y')}")

    adicionar_iss(data, valor)
    return render(request, 'home/adicionar_iss_nisiafloresta.html', {"namespace": juncao_agz.url})

def juncao_agz(request):
    unir_agz(DIRETORIO)
    return redirect('index')

def irrf_bananeiras(request):
    if request.method != 'POST':
        return render(request, 'home/adicionar_irrf_bananeiras.html', {"namespace": adicionar_irrf_bananeiras.url})

    data = datetime.strptime(request.POST.get('data').replace('-', ''), '%Y%m%d')
    valor = int(request.POST.get('valor'))
    messages.success(request, f"Adicionado o valor de R${(float(valor) / 100)} no dia "
                              f"{data.strftime('%d/%m/%y')}")

    adicionar_irrf(data, valor)
    return render(request, 'home/adicionar_irrf_bananeiras.html', {"namespace": adicionar_irrf_bananeiras.url})


def transferencia_itbi(request):
    if request.method != 'POST':
        return render(request, 'home/transferencia_itbi.html')

    sequencial_de = request.POST.get('sequencial_de')
    processo_itbi = request.POST.get('processo_itbi')
    sequencial_para = request.POST.get('sequencial_para')
    namespace = request.POST.get('namespace').upper()

    messages.success(request, f"Transferido o ITBI {processo_itbi} do sequencial {sequencial_de} "
                              f"para o sequencial {sequencial_para} em {namespace}.")
    transferir_itbi(sequencial_de, processo_itbi, sequencial_para, namespace)

    return redirect('listar_pagamentos')


def transferencia_pagamento(request):
    if request.method != 'POST':
        return render(request, 'home/listar_pagamento.html')
    sequencial_de = request.POST.get('sequencial_de')
    sequencial_para = request.POST.get('sequencial_para')
    namespace = request.POST.get('namespace')
    pagamentos_para_transferir = request.POST.get('pagamentos_para_transferir')

    messages.success(request, f"Transferido o(s) pagamento(s) do sequencial {sequencial_de} "
                              f"para o sequencial {sequencial_para} em {namespace}")
    transferir_pagamento(namespace, sequencial_de, sequencial_para, pagamentos_para_transferir)

    return render(request, 'home/index.html')


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
