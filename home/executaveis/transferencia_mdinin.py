from .dados_acesso import login_cache, senha_cache
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


# from time import sleep


class ChromeAuto:

    def __init__(self):

        self.caminho_driver = ChromeDriverManager().install()
        self.opcoes = webdriver.ChromeOptions()
        self.opcoes.add_argument(
            r'user-data-dir=C:\Users\Usuario\AppData\Local\Google\Chrome\User Data\Default')
        self.opcoes.add_experimental_option(
            'excludeSwitches', ['enable-logging'])
        self.chrome = webdriver.Chrome(
            self.caminho_driver,
            options=self.opcoes

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
            enviar_login.send_keys('aldyr')
            enviar_senha = self.chrome.find_element(By.NAME, 'CachePassword')
            enviar_senha.send_keys('al110665')
        except Exception as e:
            print('Usuário já logado')

    def exibir_pagamentos(self, sequencial_de):
        # PROCURAR PAGAMENTO
        global_relatorio = self.chrome.find_element(By.ID, "$ID2")
        global_relatorio.clear()
        global_relatorio.send_keys(f"MDININ(1{sequencial_de}")

        # EXIBIR GLOBAL PESQUISADA
        botao_exibir = self.chrome.find_element(By.ID, "BTN_Display")
        botao_exibir.click()
        return self.chrome.find_element(By.CLASS_NAME, "DetailTable").text

    def transferir_pagamento_mdinin(self, sequencial_de, sequencial_para, registro_para_transferir):
        self.exibir_pagamentos(sequencial_de)
        lista_pagamentos = []

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
            valor_original = self.chrome.find_element(
                By.ID, "txtGlobal").get_property("value")

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
            salvar = self.chrome.find_element(By.ID, "BTN_Insert")
            salvar.click()
            no_global.clear()
            no_global.send_keys(transfere_para)
            excluir_no_original = self.chrome.find_element(By.ID, "chkDelete")
            if not excluir_no_original.is_selected():
                excluir_no_original.click()
            salvar.click()

            self.exibir_pagamentos(sequencial_de)


def transferir_pagamento(namespace, sequencial_de, sequencial_para, pagamentos_para_transferir):
    chrome = ChromeAuto()

    if len(sequencial_para) != 8 and len(sequencial_para) != 7:
        print("Sequencial 'Para' ínvalido")
    if len(sequencial_de) != 8 and len(sequencial_de) != 7:
        print("Sequencial 'De' ínvalido")

    url = 'https://www.tinus.com.br/csp/sys/exp/UtilExpGlobalView.csp?%24NAMESPACE=' + namespace
    # url = 'https://www2.tinus.com.br/csp/sys/exp/UtilExpGlobalView.csp?$ID2=SITCD&$NAMESPACE=' + namespace

    chrome.acessa(url)
    chrome.fazer_login()
    chrome.clica_entrar()
    chrome.transferir_pagamento_mdinin(
        sequencial_de, sequencial_para, pagamentos_para_transferir)

    chrome.sair()


def listar_pagamentos(namespace, sequencial_de):
    chrome = ChromeAuto()

    if len(sequencial_de) != 8 and len(sequencial_de) != 7:
        print("Sequencial 'De' ínvalido")

    url = 'https://www.tinus.com.br/csp/sys/exp/UtilExpGlobalView.csp?%24NAMESPACE=' + namespace
    # url = 'https://www2.tinus.com.br/csp/sys/exp/UtilExpGlobalView.csp?$ID2=SITCD&$NAMESPACE=' + namespace

    chrome.acessa(url)
    chrome.fazer_login()
    chrome.clica_entrar()
    pagamentos = chrome.exibir_pagamentos(sequencial_de)
    chrome.sair()
    return pagamentos


