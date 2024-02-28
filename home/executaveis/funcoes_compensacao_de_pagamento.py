from math import ceil
from datetime import datetime

def executar_compensacao(debitos_em_aberto_no_extrato, uf, multa, limite_multa, juros, debitos_a_compensar, credito,
                         namespace, sequencial):
    """
    USAR CRÉDITO A COMPENSAR (ADICIONANDO OS PAGAMENTOS NO IMÓVEL 'PARA')
    """
    exercicio_atual = datetime.strftime(datetime.today(),'%y')
    registrar_global = {}
    ainda_tem_credito_a_compensar = True

    while ainda_tem_credito_a_compensar:

        reiniciar_loop_com_novo_credito = False

        # Percorre os débitos em aberto
        for exercicio_em_aberto_no_extrato, parcelas_abertas_por_exercicio_extrato in debitos_em_aberto_no_extrato.items():

            # VERIFICA SE O EXERCÍCIO EM ABERTO NO EXTRATO ESTÁ NA LISTA DOS EXERCÍCIOS A COMPENSAR
            if exercicio_em_aberto_no_extrato in debitos_a_compensar.keys():

                # DATA DO PAGAMENTO DO CRÉDITO (O PRIMEIRO DA LISTA)
                data_credito_disponivel = datetime.strptime(credito[0][0],"%d%m%y")

                data_credito_disponivel_aammdd = datetime.strftime(data_credito_disponivel, '%y%m%d')
                uf_pagamento_crédito = uf[datetime.strftime(data_credito_disponivel, '%y')]
                orgao = credito[0][2]

                for detalhe_parcela_em_aberto in parcelas_abertas_por_exercicio_extrato:

                    # VERIFICA SE A PARCELA DO EXERCÍCIO EM ABERTO ESTÁ NA LISTA DAS PARCELAS DO EXERCÍCIO A COMPENSAR
                    if not debitos_a_compensar.get(exercicio_em_aberto_no_extrato):
                        break

                    if detalhe_parcela_em_aberto[0] in debitos_a_compensar.get(exercicio_em_aberto_no_extrato):

                        vencimento_original = detalhe_parcela_em_aberto[1]
                        valor_original_uf = detalhe_parcela_em_aberto[4]
                        valor_original_real_corrigido = round(detalhe_parcela_em_aberto[4] * uf_pagamento_crédito, 2)

                        # CALCULANDO JUROS
                        data_vencimento_original = datetime.strptime(vencimento_original, '%d%m%Y')
                        # print("*"*80)
                        # print("Pago",data_credito_disponivel)
                        # print("Venc",data_vencimento_original)
                        if data_credito_disponivel <= data_vencimento_original:
                            adicional_por_atraso = 0
                        else:
                            dias_atraso = abs(data_credito_disponivel - data_vencimento_original).days
                            # print('dias_atraso',dias_atraso)
                            meses_atraso = ceil(dias_atraso / 30)
                            # print('meses_atraso',meses_atraso)
                            juros = float(juros)
                            multa = float(multa)
                            limite_multa = float(limite_multa)
                            adicional_por_atraso = calcular_total_acrescimos(dias_atraso, meses_atraso, juros, multa,
                                                                             limite_multa,
                                                                             valor_original_real_corrigido,
                                                                             namespace)
                            # print('adicional_por_atraso',adicional_por_atraso)


                        credito_necessario_pra_compensar = round(valor_original_real_corrigido + adicional_por_atraso,3)

                        # if adicional_por_atraso == 0: adicional_por_atraso=''
                        # print("*"*88)
                        #
                        # print("credito",credito)
                        # print("Tamanho",len(credito))
                        # print("Valor [0][1] R$",credito[0][1])
                        # print("Em aberto R$",credito_necessario_pra_compensar)

                        valor_credito_disponivel_em_real = round(credito[0][1],3)

                        # print("*"*88)


                        # MONTANDO A GLOBAL PRA SALVAR NO CACHÉ
                        if exercicio_atual == exercicio_em_aberto_no_extrato:
                            global_da_parcela = f'^SCICD({sequencial},{exercicio_em_aberto_no_extrato},{detalhe_parcela_em_aberto[0]})'
                        else:
                            global_da_parcela = f'^SCIDA({sequencial},{exercicio_em_aberto_no_extrato},{detalhe_parcela_em_aberto[0]})'

                        # VALOR DO CRÉDITO QUITANDO O DÉBITO DA PARCELA EM ABERTO
                        if valor_credito_disponivel_em_real >= credito_necessario_pra_compensar:

                            if adicional_por_atraso > 0:
                                adicional_por_atraso = str(f'{adicional_por_atraso:.2f}').replace('.', '')
                            else:
                                adicional_por_atraso = ''

                            if not registrar_global.get(global_da_parcela):
                                if exercicio_atual == exercicio_em_aberto_no_extrato:
                                    registrar_global[
                                        global_da_parcela] = f'{valor_original_uf}#{adicional_por_atraso}#{data_credito_disponivel_aammdd[2:]}{orgao}'
                                else:
                                    registrar_global[
                                        global_da_parcela] = f'{valor_original_uf}#{adicional_por_atraso}#{data_credito_disponivel_aammdd}{orgao}'

                            # ADICIONANDO UM SEGUNDO PAGAMENTO NA MESMA PARCELA (CASOS DE PAGAMENTO COMPLEMENTAR DE SALDO DEVEDOR)
                            else:
                                if exercicio_atual == exercicio_em_aberto_no_extrato:
                                    registrar_global[
                                        global_da_parcela] += f'#{valor_original_uf}#{adicional_por_atraso}#{data_credito_disponivel_aammdd[2:]}{orgao}'
                                else:
                                    registrar_global[
                                        global_da_parcela] += f'#{valor_original_uf}#{adicional_por_atraso}#{data_credito_disponivel_aammdd}{orgao}'

                            # ATUALIZANDO LISTA DOS CRÉDITOS PRA COMPENSAÇÃO
                            saldo_credito = round(credito[0][1] - credito_necessario_pra_compensar, 2)

                            if saldo_credito > 0:
                                credito[0][1] = saldo_credito
                            else:
                                credito.pop(0)

                            debitos_a_compensar[exercicio_em_aberto_no_extrato].pop(0)
                            if not debitos_a_compensar[exercicio_em_aberto_no_extrato]:
                                del debitos_a_compensar[exercicio_em_aberto_no_extrato]
                                if not debitos_a_compensar:
                                    ainda_tem_credito_a_compensar = False

                        # VALOR DO CRÉDITO MENOR QUE O DÉBITO EM ABERTO (vai gerar saldo devedor)
                        else:
                            # print("VALOR DO CRÉDITO MENOR QUE O DÉBITO EM ABERTO (vai gerar saldo devedor)")
                            # print("len(credito) =",len(credito))
                            # VERIFICA SE TEM MAIS CRÉDITO PRA CONTINUAR OU SE É A ÚLTIMA COMPENSAÇÃO.
                            if len(credito) > 1:
                                reiniciar_loop_com_novo_credito = True
                                ainda_tem_credito_a_compensar = True
                            else:
                                ainda_tem_credito_a_compensar = False
                                reiniciar_loop_com_novo_credito = False

                            percentual_pago = round(valor_credito_disponivel_em_real * 100 / credito_necessario_pra_compensar,4)

                            adicional_por_atraso = f'{adicional_por_atraso:.2f}'
                            adicional_por_atraso = float(adicional_por_atraso)
                            # PARA FORÇAR DOIS DÍGITOS, MATENDO '0's À DIREITA DA VÍRGULA E RETIRANDO O PONTO
                            if adicional_por_atraso > 0:
                                adicional_por_atraso = f'{adicional_por_atraso / 100 * percentual_pago:.2f}'.replace(".","")
                            else:
                                adicional_por_atraso = ''

                            # DEFININDO O VALOR PRINCIPAL PAGO PROPORCIONAMENTE
                            valor_original_uf = round(valor_original_uf*percentual_pago/100,4)

                            if not registrar_global.get(global_da_parcela):
                                if exercicio_atual == exercicio_em_aberto_no_extrato:
                                    registrar_global[
                                        global_da_parcela] = f'{valor_original_uf}#{adicional_por_atraso}#{data_credito_disponivel_aammdd[2:]}{orgao}*'
                                else:
                                    registrar_global[
                                        global_da_parcela] = f'{valor_original_uf}#{adicional_por_atraso}#{data_credito_disponivel_aammdd}{orgao}*'

                            # ADICIONANDO UM SEGUNDO PAGAMENTO NA MESMA PARCELA (CASOS DE PAGAMENTO COMPLEMENTAR DE SALDO DEVEDOR)
                            else:
                                if exercicio_atual == exercicio_em_aberto_no_extrato:
                                    registrar_global[
                                        global_da_parcela] += f'#{valor_original_uf}#{adicional_por_atraso}#{data_credito_disponivel_aammdd[2:]}{orgao}*'
                                else:
                                    registrar_global[
                                        global_da_parcela] += f'#{valor_original_uf}#{adicional_por_atraso}#{data_credito_disponivel_aammdd}{orgao}*'

                            # ATUALIZANDO LISTA DOS CRÉDITOS PRA COMPENSAÇÃO
                            # print("# ATUALIZANDO LISTA DOS CRÉDITOS PRA COMPENSAÇÃO****************************************************************")
                            # print("debitos_a_compensar",debitos_a_compensar)
                            # print("debitos_a_compensar[exercicio_em_aberto_no_extrato]",debitos_a_compensar[exercicio_em_aberto_no_extrato])
                            # print("credito[0][1]",credito[0][1])
                            # print("credito_necessario_pra_compensar",credito_necessario_pra_compensar)
                            # saldo_credito = round(credito[0][1] - credito_necessario_pra_compensar, 2)
                            # print("saldo_credito",saldo_credito)

                            # if saldo_credito > 0:
                            #     credito[0][1] = saldo_credito
                            # else:
                            #     credito.pop(0)
                            # print("detalhe_parcela_em_aberto",detalhe_parcela_em_aberto)
                            # print("valor_original_uf",valor_original_uf)
                            # print("detalhe_parcela_em_aberto[4]",detalhe_parcela_em_aberto[4])
                            # detalhe_parcela_em_aberto[4] -= valor_original_uf
                            # print("detalhe_parcela_em_aberto[4]",detalhe_parcela_em_aberto[4])
                            # print("detalhe_parcela_em_aberto",detalhe_parcela_em_aberto)

                            detalhe_parcela_em_aberto[4] -= valor_original_uf

                            credito.pop(0)
                            # ainda_tem_credito_a_compensar = True
                            if len(credito) == 0:
                                break

                            break

                if reiniciar_loop_com_novo_credito:
                    break
            if not ainda_tem_credito_a_compensar:
                break

    return registrar_global, credito, debitos_a_compensar


def calcular_total_acrescimos(dias_atraso, meses_atraso, juros, multa, limite_multa, valor_original_real_corrigido,
                              namespace):
    """
    Calcula os acréscimos com base na legislação de cada município.
    :param dias_atraso:
    :param meses_atraso:
    :param juros:
    :param multa:
    :param limite_multa:
    :param valor_original_real_corrigido:
    :param namespace:
    :return:
    """

    # SEPARAÇÃO DOS MUNICÍPIOS A PARTIR DAS REGRAS DE CÁLCULOS DE ACRÉSCIMOS EM COMUM.
    multa_limite_multa_juros = ['EXTREMOZ', 'TESTEEXT', 'GARANHUNS' , 'TESTEGAR', 'CAICO', 'TESTECAI']
    multa_limite_multa_juros += ['MOSSORO', 'TESTEMOS','SAOGONCALO','TESTEGON','OLINDA','TESTEOLI']
    multa_limite_multa_juros += ['PARNAMIRIM', 'TESTEPAR', 'CATOLEDOROCHA','TESTECDR', 'CAMARAGIBE']
    multa_limite_multa_juros += ['TANGARA', 'NISIAFLORESTA', 'TESTENIS', 'CEARAMIRIM', 'ALEXANDRIA']
    duas_faixas_limite_multa_juros = ['CABO']
    tres_faixas_limite_multa_juros = []

    # 1.000#2.0#5.0#8.0#10.0#1.0
    quatro_faixas_limite_multa_juros = ['SANTACRUZDOCAPIBARIBE', 'TESTESCC']

    # MUNICÍPIOS QUE CONSIDERAM APENAS JUROS (PERCENTUAL SEM LIMITE) E MULTA COM LIMITADOR DE PERCENTUAL MÁXIMO
    if namespace in multa_limite_multa_juros:
        total_juros = round(meses_atraso * juros / 100 * valor_original_real_corrigido, 2)
        if dias_atraso * multa > limite_multa:
            percentual_multa = limite_multa
        else:
            percentual_multa = dias_atraso * multa
        total_multa = round(percentual_multa / 100 * valor_original_real_corrigido, 2)


    elif namespace in duas_faixas_limite_multa_juros:
        print(f'{namespace} é cálculo de multa com 2 faixas')
    elif namespace in tres_faixas_limite_multa_juros:
        print(f'{namespace} é cálculo de multa com 3 faixas')
    elif namespace in quatro_faixas_limite_multa_juros:
        print(f'{namespace} é cálculo de multa com 4 faixas')
    else:
        print(f'{namespace} sem parâmetros de acréscimos encontrado')
        # temp = input("Encerre o programa!!!!!")

    return total_multa + total_juros

def configurando_extrato(extrato):


    # EXECUTA SE FOR EXERCÍCIO ANTERIOR
    if 'SCIDA' in extrato:
        # AJUSTANDO CARACTERES PRA SEPARAR OS PIECES
        extrato = extrato.replace('*', '').replace('"0', '0').replace('")', ')').replace('"#', '#').replace('"1', '#1')
        extrato_lancamento_fragmentado = extrato.split('"')
        extrato_lancamento_detalhado = []

        situacao_imovel = {}

        # SEPARANDO OS PIECES DE CADA LANÇAMENTO
        for i in extrato_lancamento_fragmentado:
            extrato_lancamento_detalhado.append(i.split("#"))

        for i in extrato_lancamento_detalhado:
            valor = 0.0
            i.pop()
            contador = 0
            eh_acordo = False

            for j in i:

                if ":" in j:
                    exercicio_esta_parcelado = False

                    if len(j) < 30:
                        exercicio = j.find(",")
                        exercicio = j[exercicio + 1:exercicio + 3]
                        parcelas_lancadas = []
                    else:
                        exercicio = j.find(",")
                        exercicio = j[exercicio + 1:exercicio + 10]
                        parcelas_lancadas = []
                        eh_acordo = True

                #  IDENTIFICAÇÃO DAS PARCELAS
                elif ("T" in j or "P" in j):
                    valor = 0.0
                    contador = 0

                    # SE NÃO FOR PARCELA DE PARCELAMENTO
                    if not len(j) > 7:
                        parcela = j[5:]
                        vencimento = j[1:3] + j[3:5] + "20" + exercicio

                    # SE FOR PARCELA DE PARCELAMENTO
                    else:
                        parcela = j[7:]
                        vencimento = j[5:7] + j[3:5] + "20" + j[1:3]

                # ENTRA SE O EXERCÍCIO ESTIVER PARCELADO
                elif len(j) > 8 and not exercicio_esta_parcelado:
                    valor = 0.0
                    contador = 0
                    parcela = j
                    vencimento = "P"
                    exercicio_esta_parcelado = True
                    parcelas_lancadas.append(['PARCELADO', parcela])

                #  SOMAR IMPOSTO + TAXAS (3 PIECES SEGUINTES)
                elif contador < 3 and not exercicio_esta_parcelado and not eh_acordo:

                    # SE O PIECE ESTIVER EM BRANCO, ATRIBUI VALOR 0.0 (PARA CASOS DE PARCELAMENTO)
                    if not j: j = 0
                    valor = valor + round(float(j),4)
                    valor = round(valor, 4)

                    contador += 1
                    if contador == 3:
                        parcelas_lancadas.append([parcela, vencimento, valor, 0.0, valor, "A"])

                elif eh_acordo:

                    # SE O PIECE ESTIVER EM BRANCO, ATRIBUI VALOR 0.0 (PARA CASOS DE PARCELAMENTO)
                    if not j: j = 0

                    valor = valor + round(float(j),4)
                    valor = round(valor, 4)
                    contador += 1
                    if contador == 1:
                        parcelas_lancadas.append([parcela, vencimento, valor, 0.0, valor, "A"])

                situacao_imovel[exercicio] = parcelas_lancadas

    # EXECUTA SE FOR EXERCÍCIO ATUAL
    elif 'SCICD' in extrato:
        situacao_imovel = {}

        extrato_lancamento_detalhado = []
        extrato_lancamento_fragmentado = extrato.split('"')

        # SEPARANDO OS PIECES
        for i in extrato_lancamento_fragmentado:
            extrato_lancamento_detalhado.append(i.split("#"))

        extrato_lancamento_detalhado.pop()

        # PEGAR CARACTERES QUE DEFINEM O EXERCÍCIO
        exercicio = extrato_lancamento_detalhado[0][0]
        fatia1 = exercicio.find(',') + 1
        fatia2 = fatia1 + 2
        exercicio = exercicio[fatia1:fatia2]

        # LIMPANDO LISTA DEIXANDO APENAS OS INDICES COM OS DADOS DO LANÇAMENTO
        # REMOVENDO PRIMEIRO ÍNDICE COM OS DADOS DO EXERCÍCIO E DESEMPACOTANDO A LISTA
        extrato_lancamento_detalhado.pop(0)
        extrato_lancamento_detalhado = extrato_lancamento_detalhado[0]

        valor_unica_com_desconto = float(extrato_lancamento_detalhado[0]) + float(extrato_lancamento_detalhado[1])
        valor_unica_sem_desconto = float(extrato_lancamento_detalhado[3]) + float(extrato_lancamento_detalhado[4])
        valor_parcelas = float(extrato_lancamento_detalhado[9]) + float(extrato_lancamento_detalhado[10])
        quantidade_parcelas = int(extrato_lancamento_detalhado[8])
        vencimentos = extrato_lancamento_detalhado[-1]

        situacao_imovel[exercicio] = []
        parcelas_lancadas = []

        # SEPARANDO AS DATAS DE VENCIMENTOS
        for parcela in range(1, quantidade_parcelas + 1):
            data = f"{vencimentos[(parcela - 1) * 4: parcela * 4]}20{exercicio}"
            if parcela == 1:
                parcelas_lancadas.append(['0', data, valor_unica_sem_desconto, 0.0, valor_unica_sem_desconto, 'A'])
                parcelas_lancadas.append(['0', data, valor_unica_com_desconto, 0.0, valor_unica_com_desconto, 'A'])

            parcelas_lancadas.append([f'{parcela}', data, valor_parcelas, 0.0, valor_parcelas, 'A'])

        situacao_imovel[exercicio] = parcelas_lancadas

    else:
        situacao_imovel = {}
    return situacao_imovel


def configurando_pagamentos(pagamentos):
    pagamentos = pagamentos.replace(',"', ',').replace('",', ',').replace(' = "', '#')
    pagamentos = pagamentos.split('"')
    pagamentos_separados = []

    # VALORES FORMATADOS PRA CRUZAR COM LANÇADOS
    lista_informacoes_pagamentos = []

    for registro in pagamentos:
        pagamentos_separados.append(registro.split("#"))

    for linha_pagamento in pagamentos_separados:
        quantidade_pagamentos_parcela = (len(linha_pagamento))
        valor_total_pago = 0.0
        for registro in linha_pagamento:

            if ":" in registro:
                # LOCALIZANDO EXERCÍCIO DO PAGAMENTO
                virgula1 = registro.find(",")
                virgula2 = registro.find(",", virgula1 + 1)
                exercicio = registro[virgula1 + 1:virgula2]

                # LOCALIZANDO PARCELA DO PAGAMENTO
                virgula1 = registro.find(",")
                virgula2 = registro.find(",", virgula1 + 1)
                fechaparenteses = registro.find(")")
                parcela = registro[virgula2 + 1:fechaparenteses]

        for reg in range(1, quantidade_pagamentos_parcela, 3):
            if not linha_pagamento[reg]: linha_pagamento[reg] = 0.0
            valor_total_pago += float(linha_pagamento[reg])
        if "*" in linha_pagamento[-1]:
            situacao = 'S'
        else:
            situacao = 'Q'

        lista_informacoes_pagamentos.append([exercicio, parcela, valor_total_pago, situacao])

    lista_informacoes_pagamentos.pop()
    return lista_informacoes_pagamentos


def cruzando_dados_extrato_pagamento(extrato_completo, pagamentos_formatados):
    for exercicio, parcelas in extrato_completo.items():
        num_parcelas = 0
        for parcela in parcelas:

            for pagamento in pagamentos_formatados:
                # COMPARA EXERCÍCIO E PARCELA PAGA COM VALORES LANÇADOS

                if exercicio == pagamento[0] and parcela[0] == pagamento[1]:
                    extrato_completo[exercicio][num_parcelas][3] = pagamento[2]

                    saldo_devedor = round(extrato_completo[exercicio][num_parcelas][2] - pagamento[2], 3)

                    extrato_completo[exercicio][num_parcelas][4] = round(saldo_devedor, 2)

                    extrato_completo[exercicio][num_parcelas][5] = pagamento[3]

            num_parcelas = num_parcelas + 1

    return extrato_completo


def extrato_com_valores_em_aberto(extrato_completo):
    """
    Do extrato detalhado, retorna um dicionário apenas com os débitos em aberto pra compensação
    :param extrato_completo:
    :return: extrato_em_aberto
    """

    # COPIANDO DICIONARIO ALOCANDO ESPAÇO DE MEMÓRIA DIFERENTE
    extrato_em_aberto = extrato_completo.copy()

    for exercicio, parcelas in extrato_completo.items():
        indices_de_exclusao = []
        num_parcelas = 0
        for parcela in parcelas:

            # GRAVA INDICE SE A PARCELA ESTÁ QUITADA OU EXERCÍCIO PARCELADO
            if parcela[-1] == 'Q' or parcela[0] == 'PARCELADO':
                indices_de_exclusao.append(num_parcelas)
            # else:
            #     extrato_em_aberto[exercicio][num_parcelas].pop(0)
            num_parcelas += 1

        indices_de_exclusao.reverse()

        if indices_de_exclusao:
            # REMOVENDO PARCELAS PAGAS
            for ind in indices_de_exclusao:
                del extrato_em_aberto[exercicio][ind]
                if not extrato_em_aberto[exercicio]:
                    del extrato_em_aberto[exercicio]

    return extrato_em_aberto


def multa_juros(global_acrescimos):
    """
    Método pra buscar na base de dados os parâmetros pra calcular acréscimos
    :param global_acrescimos:
    :return: multa, limite_multa, juros
    """
    # FATIAR GLOBAL PRA FICAR APENAS COM AS INFORMAÇÕES NECESSÁRIAS
    fatia1 = global_acrescimos.find('"')
    fatia2 = global_acrescimos.find('"', fatia1 + 1)
    global_acrescimos = global_acrescimos[fatia1 + 1:fatia2]
    desativa_saldo, multa, limite_multa, juros = global_acrescimos.split('#')
    return multa, limite_multa, juros


def unidades_fiscais(lista_uf):
    lista_uf = lista_uf.replace('  ^SICMPR("U",', '').replace(')', '').replace('"', '').replace(' = ', '#')

    quantidade_igual = 0
    inicio = 2
    uf_ano = {}

    fim_lista = False

    while not fim_lista:
        posicao_igual = lista_uf.find('#', inicio)
        posicao_dois_pontos = lista_uf.find(':', posicao_igual)
        quantidade_igual += 1
        tamanho_digito = len(str(quantidade_igual))
        final = posicao_dois_pontos - tamanho_digito

        try:
            exercicio, valor = lista_uf[inicio:final].split("#")
            exercicio = exercicio[:2]

        except Exception as e:
            pass
            # print("ERRO AO SEPARAR VALOR COM BASE NO CARACTERE '#'")
            # print("OCORRÊNCIA GERADA, PROVAVELMENTE NO ÚLTIMO ITEM DA LISTA (TOTAL DA GLOBAL)")

        if not exercicio in uf_ano:
            uf_ano[exercicio] = float(valor) / 10000

        if posicao_igual == -1:
            fim_lista = True

        inicio = final + tamanho_digito + 1

    return uf_ano


def validar_dados_creditos(credito):
    """
        Verifica se as informações passadas pelo usuário são válidas
    :param lista do crédito [data,valor]:
    :return: True or False
    """

    for registro in credito:
        try:
            registro[0] = datetime.strptime(registro[0], '%d%m%y')
            registro[1] = float(registro[1])

        except Exception as e:
            print(f"Um dos dados está no formato inválido!")
            print(e)
            return False

    return True


def validar_parcelas_compensar(debitos_em_aberto, parcelas_a_compensar):
    """
    CONFERE SE AS PARCELAS SOLICITADAS PARA SEREM COMPENSADAS ESTÃO EM ABERTO OU COM SALDO DEVEDOR
    :param debitos_em_aberto:
    :param parcelas_a_compensar:
    :return: True or False
    """

    validar_compensacao = False

    for exercicio, parcelas in parcelas_a_compensar.items():

        validar_compensacao = False

        if not debitos_em_aberto.get(exercicio):
            print(f"Não há débito em aberto no exercício de {exercicio}")
            break

        for parcela in parcelas:

            validar_compensacao = False
            for indice in debitos_em_aberto.get(exercicio):

                if parcela in indice:
                    validar_compensacao = True
                    break
            if not validar_compensacao: break
        if not validar_compensacao: break
    return validar_compensacao


# def salvar_compensacao(namespace, sequencial, globais):
#     print("namespace",namespace," | Tipo",type(namespace))
#     print("sequencial",sequencial," | Tipo",type(sequencial))
#     print("globais",globais," | Tipo",type(globais))
