from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
# from time import sleep


URL = 'https://www.tinus.com.br/csp/sys/exp/UtilExpGlobalView.csp?%24NAMESPACE='
# URL = 'https://www2.tinus.com.br/csp/sys/exp/UtilExpGlobalView.csp?$ID2=SITCD&$NAMESPACE='

class ChromeAuto:

    def __init__(self):

        # self.caminho_driver = 'chromedriver'
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
            print('Página já aberta')

    def fazer_login(self):
        try:
            enviar_login = self.chrome.find_element(By.NAME, 'CacheUserName')
            enviar_login.send_keys('aldyr')
            enviar_senha = self.chrome.find_element(By.NAME, 'CachePassword')
            enviar_senha.send_keys('al110665')
        except Exception as e:
            print('Usuário já logado')

    def exibir_valores (self, mascara_pesquisa):
        # PROCURAR PAGAMENTO
        global_relatorio = self.chrome.find_element(By.ID, "$ID2")
        global_relatorio.clear()
        global_relatorio.send_keys(mascara_pesquisa)

        quantidade_linhas = self.chrome.find_element(By.ID, "NodeCount")
        quantidade_linhas.clear()
        quantidade_linhas.send_keys("1000")

        # EXIBIR GLOBAL PESQUISADA
        botao_exibir = self.chrome.find_element(By.ID, "BTN_Display")
        botao_exibir.click()
        return self.chrome.find_element(By.CLASS_NAME, "DetailTable").text

    def manutencao_de_global(self, mascara, linha, excluir):
        valores = self.exibir_valores(mascara)

        detalhes = self.chrome.find_element(By.CLASS_NAME, "DetailTable")
        if "Total: 0 [Fim da global]" in detalhes.text:
            print("Nenhum valor encontrado")
            return


        lista_registros = []
        if linha == 'todos':
            total_de_registros = int(self.chrome.find_element(By.ID, "TotalText").text[7:])
            for id in range(1, total_de_registros + 1): lista_registros.append(id)
        else:
            registros = linha.split(";")
            lista_registros = [int(val) for val in registros]

        lista_registros.sort(reverse=True)

        for registro in lista_registros:
            print("Gravando registro", registro)
            # HABILITAR EDICAO
            habilitar_edicao = self.chrome.find_element(By.ID, "chkEdit")
            if not habilitar_edicao.is_selected():
                habilitar_edicao.click()
            try:
                editar_global = self.chrome.find_element(By.CSS_SELECTOR, f"body > table > tbody > tr:nth-child(2) > td >"
                                                                      " form > table.DetailTable > tbody >"
                                                                      f" tr:nth-child({str(registro)}) > td:nth-child(4) > a")
                editar_global.click()
                no_global = self.chrome.find_element(By.ID, "txtGlobal")
                valor_original = self.chrome.find_element(By.ID, "txtGlobal").get_property("value")

                # ADICIONANDO 'ant' AO REGISTRO ORIGINAL
                bkp = valor_original.replace("(", "ant(")

                no_global.clear()
                no_global.send_keys(bkp)
                # sleep(1)
                salvar = self.chrome.find_element(By.ID, "BTN_Insert")

                excluir_no_original = self.chrome.find_element(By.ID, "chkDelete")
                if excluir:
                    if not excluir_no_original.is_selected():
                        excluir_no_original.click()
                else:
                    if excluir_no_original.is_selected():
                        excluir_no_original.click()
                salvar.click()
                self.exibir_valores(mascara)

            except Exception as e:
                print(f"Número do registro {registro} em '{mascara}' não encontrado.")
                print("Erro = ", e)


def listar_regitros(namespace, mascara):

    chrome = ChromeAuto()
    chrome.acessa(URL+namespace)
    chrome.fazer_login()
    chrome.clica_entrar()
    registros = chrome.exibir_valores(mascara)
    chrome.sair()
    return registros

def executar_salvar_global (namespace, mascara, linha, excluir):
    chrome = ChromeAuto()
    chrome.acessa(URL + namespace)
    chrome.fazer_login()
    chrome.clica_entrar()
    chrome.manutencao_de_global(mascara, linha, excluir)
    chrome.sair()