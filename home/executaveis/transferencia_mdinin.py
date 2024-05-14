from .dados_acesso import login_cache, senha_cache, url_ambiente_de_producao, url_ambiente_de_teste, CHROME_DRIVER_PATH
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
# from webdriver_manager.chrome import ChromeDriverManager

class ChromeAuto:

    def __init__(self):

        # self.caminho_driver = ChromeDriverManager().install()
        # self.opcoes = webdriver.ChromeOptions()
        # self.opcoes.add_argument(r'user-data-dir=C:\Users\Usuario\AppData\Local\Google\Chrome\User Data\Default')
        # self.opcoes.add_experimental_option('excludeSwitches', ['enable-logging'])
        # self.chrome = webdriver.Chrome(
        #     self.caminho_driver,
        #     options=self.opcoes

        # )

        chrome_options = webdriver.ChromeOptions()
        chrome_service = Service(
            executable_path=str(CHROME_DRIVER_PATH),
        )

        self.chrome = webdriver.Chrome(
            service=chrome_service,
            options=chrome_options
        )

    def acessa(self, site):
        self.chrome.get(site)

    def sair(self):
        self.chrome.quit()

    def clica_entrar(self):
        try:
            botao_entrar = self.chrome.find_element(By.NAME, 'CacheLogin')
            botao_entrar.click()

        except Exception as e:
            print('Página já aberta')

    def fazer_login(self):
        try:
            enviar_login = self.chrome.find_element(By.NAME, 'CacheUserName')
            enviar_login.send_keys(login_cache)
            enviar_senha = self.chrome.find_element(By.NAME, 'CachePassword')
            enviar_senha.send_keys(senha_cache)
        except Exception as e:
            print('Usuário já logado')

    def exibir_pagamentos(self, sequencial_de):
        # PROCURAR PAGAMENTO
        global_relatorio = self.chrome.find_element(By.ID, "$ID2")
        global_relatorio.clear()
        global_relatorio.send_keys(f"MDININ(1{sequencial_de}")

        quantidade_linhas = self.chrome.find_element(By.ID, "NodeCount")
        quantidade_linhas.clear()
        quantidade_linhas.send_keys("1000")

        # EXIBIR GLOBAL PESQUISADA
        botao_exibir = self.chrome.find_element(By.ID, "BTN_Display")
        botao_exibir.click()
        return self.chrome.find_element(By.CLASS_NAME, "DetailTable").text

    def transferir_pagamento_mdinin(self, sequencial_de, sequencial_para, registro_para_transferir):
        self.exibir_pagamentos(sequencial_de)
        lista_pagamentos = []
        lista_md = []

        if registro_para_transferir == 'todos':
            total_de_pagamentos = int(
                self.chrome.find_element(By.ID, "TotalText").text[7:])
            for id in range(1, total_de_pagamentos + 1):
                lista_pagamentos.append(id)
        else:
            registros = registro_para_transferir.split(";")
            lista_pagamentos = [int(val) for val in registros]

        lista_pagamentos.sort(reverse=True)
        
        for registro in lista_pagamentos:
            
            # HABILITAR EDICAO
            habilitar_edicao = self.chrome.find_element(By.ID, "chkEdit")
            if not habilitar_edicao.is_selected():
                habilitar_edicao.click()
            editar_global = self.chrome.find_element(By.CSS_SELECTOR, f"body > table > tbody > tr:nth-child(2) > td >"
                                                                      " form > table.DetailTable > tbody >"
                                                                      f" tr:nth-child({str(registro)}) > td:nth-child(4) > a")
            editar_global.click()
            no_global = self.chrome.find_element(By.ID, "txtGlobal")
            valor_original = no_global.get_property("value")

            #CONVERTE MDININ EM MD E GUARDA EM UMA LISTA PRA RETORNO DO PRÓXIMO PROCEDIMENTO
            posicao_data = valor_original.find(',') + 4
            data = valor_original[posicao_data:posicao_data+6]
            posicao_nreg = posicao_data + 6
            nreg = str(int(valor_original[posicao_nreg:posicao_nreg+7]))
            md = 'MD'+data+'('+nreg+')'
            lista_md.append(md)
            
            bkp = valor_original[0:7] + "ant" + valor_original[7:]
            transfere_para = valor_original[0:9] + sequencial_para
            if len(sequencial_para) == 8:
                transfere_para += valor_original[17:]
            elif len(sequencial_para) == 7:
                transfere_para += valor_original[16:]
            else:
                print("Quantidade de dígitos do Sequencial PARA inválido")

            no_global.clear()
            no_global.send_keys(bkp)

            # TODO Descomentar SALVAR pra consolidar funcionamento
            salvar = self.chrome.find_element(By.ID, "BTN_Insert")
            salvar.click()
            no_global.clear()
            no_global.send_keys(transfere_para)
            excluir_no_original = self.chrome.find_element(By.ID, "chkDelete")
            if not excluir_no_original.is_selected():
                excluir_no_original.click()
            
            # TODO Descomentar SALVAR pra consolidar funcionamento
            salvar.click()

            self.exibir_pagamentos(sequencial_de)
            
        return lista_md



    def bkp_md(self, lista_md):

        self.exibir_pagamentos(sequencial_de)
        md_completo = {}

        for md in lista_md:

            # CARREGAR MD
            global_relatorio = self.chrome.find_element(By.ID, "$ID2")
            global_relatorio.clear()
            global_relatorio.send_keys(md)

            # EXIBIR GLOBAL PESQUISADA
            botao_exibir = self.chrome.find_element(By.ID, "BTN_Display")
            botao_exibir.click()

            # HABILITAR EDICAO
            habilitar_edicao = self.chrome.find_element(By.ID, "chkEdit")
            if not habilitar_edicao.is_selected():
                habilitar_edicao.click()
            editar_global = self.chrome.find_element(By.CSS_SELECTOR, f"body > table > tbody > tr:nth-child(2) >"
                                                      "td > form > table.DetailTable > tbody > tr.EvenRow > td:nth-child(4) > a")
            
            editar_global.click()
            
            
            no_global = self.chrome.find_element(By.ID, "txtGlobal")
            
            detalhe_valor_md_atual = self.chrome.find_element(By.ID, "GValue").text
            
            # ADICIONANDO 'ant' AO REGISTRO ORIGINAL
            bkp = md.replace("(", "ant(")
            no_global.clear()
            no_global.send_keys(bkp)
            salvar = self.chrome.find_element(By.ID, "BTN_Insert")

            # TODO Descomentar SALVAR pra consolidar funcionamento
            # Salvar backup
            salvar.click()

            md_completo[md] = [detalhe_valor_md_atual,'MD','PC']

        return md_completo            


    def transferir_pagamento_md(self, sequencial_de, sequencial_para, registro_para_transferir):
        self.exibir_pagamentos(sequencial_de)
        lista_pagamentos = []
        lista_md = []

        if registro_para_transferir == 'todos':
            total_de_pagamentos = int(
                self.chrome.find_element(By.ID, "TotalText").text[7:])
            for id in range(1, total_de_pagamentos + 1):
                lista_pagamentos.append(id)
        else:
            registros = registro_para_transferir.split(";")
            lista_pagamentos = [int(val) for val in registros]

        lista_pagamentos.sort(reverse=True)
        
        for registro in lista_pagamentos:
            
            # HABILITAR EDICAO
            habilitar_edicao = self.chrome.find_element(By.ID, "chkEdit")
            if not habilitar_edicao.is_selected():
                habilitar_edicao.click()
            editar_global = self.chrome.find_element(By.CSS_SELECTOR, f"body > table > tbody > tr:nth-child(2) > td >"
                                                                      " form > table.DetailTable > tbody >"
                                                                      f" tr:nth-child({str(registro)}) > td:nth-child(4) > a")
            editar_global.click()
            no_global = self.chrome.find_element(By.ID, "txtGlobal")
            valor_original = no_global.get_property("value")

            #CONVERTE MDININ EM MD E GUARDA EM UMA LISTA PRA RETORNO DO PRÓXIMO PROCEDIMENTO
            posicao_data = valor_original.find(',') + 4
            data = valor_original[posicao_data:posicao_data+6]
            posicao_nreg = posicao_data + 6
            nreg = str(int(valor_original[posicao_nreg:posicao_nreg+7]))
            md = 'MD'+data+'('+nreg+')'
            lista_md.append(md)
            
            bkp = valor_original[0:7] + "ant" + valor_original[7:]
            transfere_para = valor_original[0:9] + sequencial_para
            if len(sequencial_para) == 8:
                transfere_para += valor_original[17:]
            elif len(sequencial_para) == 7:
                transfere_para += valor_original[16:]
            else:
                print("Quantidade de dígitos do Sequencial PARA inválido")

            no_global.clear()
            no_global.send_keys(bkp)

            # TODO Descomentar SALVAR pra consolidar funcionamento
            salvar = self.chrome.find_element(By.ID, "BTN_Insert")
            salvar.click()
            no_global.clear()
            no_global.send_keys(transfere_para)
            excluir_no_original = self.chrome.find_element(By.ID, "chkDelete")
            if not excluir_no_original.is_selected():
                excluir_no_original.click()
            
            # TODO Descomentar SALVAR pra consolidar funcionamento
            salvar.click()

            self.exibir_pagamentos(sequencial_de)
            
        return lista_md

def transferir_pagamento(namespace, contribuinte_de, contribuinte_para, pagamentos_para_transferir):
    chrome = ChromeAuto()

    if len(contribuinte_para) != 8 and len(contribuinte_para) != 7:
        print("Contribuinte 'Para' ínvalido")
    if len(contribuinte_de) != 8 and len(contribuinte_de) != 7:
        print("Contribuinte 'De' ínvalido")

    if 'TESTE' in namespace:
        # AMBIENTE DE TESTES
        url = url_ambiente_de_teste + namespace
    else:
        # AMBIENTE DE PRODUÇÃO
        url = url_ambiente_de_producao + namespace

    chrome.acessa(url)
    chrome.fazer_login()
    chrome.clica_entrar()
    lista_md = chrome.transferir_pagamento_mdinin(
        contribuinte_de, contribuinte_para, pagamentos_para_transferir)
    
    # chrome.acessa(url)
    # md_completo = chrome.bkp_md(lista_md)

    

    chrome.sair()
    return md_completo


def listar_pagamentos(namespace, sequencial_de):
    chrome = ChromeAuto()

    if len(sequencial_de) != 8 and len(sequencial_de) != 7:
        print("Sequencial 'De' ínvalido")

    if 'TESTE' in namespace:
        # AMBIENTE DE TESTES
        url = url_ambiente_de_teste+namespace
    else:
        # AMBIENTE DE PRODUÇÃO
        url = url_ambiente_de_producao+namespace

    chrome.acessa(url)
    chrome.fazer_login()
    chrome.clica_entrar()
    pagamentos = chrome.exibir_pagamentos(sequencial_de)
    chrome.sair()
    return pagamentos



def transferir_md(md_completo, modelo_para, parcela_para, contribuinte_para, namespace):



    print("Onde estou? TRANSFERENCIA_MDININ.PY DEF TRANSFERIR_MD")
    print(__name__)

    print(f'contribuinte_para: {contribuinte_para}')
    print(f'namespace: {namespace}')
    print(f'md_completo: {md_completo}')
    print(f'modelo_para: {modelo_para}')
    print(f'parcela_para: {parcela_para}')

    chrome = ChromeAuto()

    # if len(contribuinte_para) != 8 and len(contribuinte_para) != 7:
    #     print("Contribuinte 'Para' ínvalido")
    # if len(contribuinte_de) != 8 and len(contribuinte_de) != 7:
    #     print("Contribuinte 'De' ínvalido")

    # if 'TESTE' in namespace:
    #     # AMBIENTE DE TESTES
    #     url = url_ambiente_de_teste + namespace
    # else:
    #     # AMBIENTE DE PRODUÇÃO
    #     url = url_ambiente_de_producao + namespace

    chrome.acessa(url)
    chrome.fazer_login()
    chrome.clica_entrar()
    # lista_md = chrome.transferir_pagamento_mdinin(
    #     contribuinte_de, contribuinte_para, pagamentos_para_transferir)
    
    chrome.acessa(url)
    # md_completo = chrome.bkp_md(lista_md)

    

    chrome.sair()
    return md_completo