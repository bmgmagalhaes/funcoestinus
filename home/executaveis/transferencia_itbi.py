from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium import webdriver


class ChromeAuto:

    def __init__(self):
        self.caminho_driver = ChromeDriverManager().install()
        self.opcoes = webdriver.ChromeOptions()
        self.opcoes.add_argument(r'user-data-dir=C:\Users\Usuario\AppData\Local\Google\Chrome\User Data\Default')
        self.opcoes.add_experimental_option('excludeSwitches', ['enable-logging'])
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
            print('Erro na função clica_entrar')

    def fazer_login(self):
        try:
            enviar_login = self.chrome.find_element(By.NAME, 'CacheUserName')
            enviar_login.send_keys('aldyr')
            enviar_senha = self.chrome.find_element(By.NAME, 'CachePassword')
            enviar_senha.send_keys('al110665')
        except Exception as e:
            print('Erro em fazer_login')

    def transferir_pagamento_mdinin(self, sequencial_de, sequencial_para):

        # PROCURAR PAGAMENTO
        global_relatorio = self.chrome.find_element(By.ID, "$ID2")
        global_relatorio.clear()
        global_relatorio.send_keys(f"MDININ(1{sequencial_de}")

        # EXIBIR GLOBAL PESQUISADA
        botao_exibir = self.chrome.find_element(By.ID, "BTN_Display")
        botao_exibir.click()

        detalhe_pagamentos = self.chrome.find_element(By.CLASS_NAME, "DetailTable")
        print(detalhe_pagamentos.text)
        registro_pagamento = input("Informe o número do registro do pagamento pra transferir: ")

        # HABILITAR EDICAO
        habilitar_edicao = self.chrome.find_element(By.ID, "chkEdit")
        if not habilitar_edicao.is_selected():
            habilitar_edicao.click()

        editar_global = self.chrome.find_element(By.CSS_SELECTOR, f"body > table > tbody > tr:nth-child(2) > td >"
                                                                  " form > table.DetailTable > tbody >"
                                                                  f" tr:nth-child({registro_pagamento}) > td:nth-child(4) > a")
        editar_global.click()

        no_global = self.chrome.find_element(By.ID, "txtGlobal")
        valor_original = self.chrome.find_element(By.ID, "txtGlobal").get_property("value")

        bkp = valor_original[0:7] + "ant" + valor_original[7:]
        transfere_para = valor_original[0:9] + sequencial_para + valor_original[17:]

        no_global.clear()
        no_global.send_keys(bkp)
        salvar = self.chrome.find_element(By.ID,"BTN_Insert")
        salvar.click()
        no_global.clear()
        no_global.send_keys(transfere_para)
        excluir_no_original = self.chrome.find_element(By.ID, "chkDelete")
        if not excluir_no_original.is_selected():
            excluir_no_original.click()
        salvar.click()

    def transferir_itbi(self, sequencial_de, itbi_de, sequencial_para, texto_global, final):
        # PROCURAR ITBI
        global_relatorio = self.chrome.find_element(By.ID, "$ID2")
        global_relatorio.clear()
        global_relatorio.send_keys(f"{texto_global}{sequencial_de},{itbi_de}{final}")

        # EXIBIR GLOBAL PESQUISADA
        botao_exibir = self.chrome.find_element(By.ID, "BTN_Display")
        botao_exibir.click()

        # HABILITAR EDICAO
        habilitar_edicao = self.chrome.find_element(By.ID, "chkEdit")
        if not habilitar_edicao.is_selected():
            habilitar_edicao.click()

        editar_global = self.chrome.find_element(By.CSS_SELECTOR, "body > table > tbody > tr:nth-child(2) > td > form >"
                                                                  " table.DetailTable > tbody > tr.EvenRow >"
                                                                  " td:nth-child(4) > a")
        editar_global.click()

        no_global = self.chrome.find_element(By.ID, "txtGlobal")
        valor_original = self.chrome.find_element(By.ID, "txtGlobal").get_property("value")

        bkp = valor_original[0:6] + "ant" + valor_original[6:]
        transfere_cadastro_itbi = valor_original[0:7] + sequencial_para + valor_original[15:]

        no_global.clear()
        no_global.send_keys(bkp)

        salvar = self.chrome.find_element(By.ID,"BTN_Insert")
        salvar.click()
        no_global.clear()
        no_global.send_keys(transfere_cadastro_itbi)
        excluir_no_original = self.chrome.find_element(By.ID, "chkDelete")

        if not excluir_no_original.is_selected():
            excluir_no_original.click()

        salvar.click()


def transferir_itbi(sequencial_de, itbi_de, sequencial_para, namespace):
    chrome = ChromeAuto()

    # AMBIENTE DE TESTE
    # url = 'https://www2.tinus.com.br/csp/sys/exp/UtilExpGlobalView.csp?$ID2=SITCD&$NAMESPACE=' + namespace
    # AMBIENTE DE PRODUÇÃO
    url = 'https://www.tinus.com.br/csp/sys/exp/UtilExpGlobalView.csp?$ID2=SITCD&$NAMESPACE=' + namespace
    chrome.acessa(url)
    chrome.fazer_login()
    chrome.clica_entrar()
    # chrome.transferir_pagamento_mdinin(sequencial_de, sequencial_para)
    chrome.transferir_itbi(sequencial_de, itbi_de, sequencial_para, "SITCD(", ')')
    chrome.transferir_itbi(sequencial_de, itbi_de, sequencial_para, "SITDB(", ')')
    chrome.transferir_itbi(sequencial_de, itbi_de, sequencial_para, "SITDB(", ',')

    chrome.sair()