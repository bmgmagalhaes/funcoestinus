from .dados_acesso import login_cache, senha_cache, url_ambiente_de_producao, url_ambiente_de_teste, CHROME_DRIVER_PATH
from datetime import datetime
# from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium import webdriver

# AMBIENTE DE TESTES
url = url_ambiente_de_teste+'TESTEBAN'

# AMBIENTE DE PRODUÇÃO
url = url_ambiente_de_producao+'BANANEIRAS'


class ChromeAuto:

    def __init__(self):

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
            print('Erro na função clica_entrar')
            print('Página não carregada ou usuário já logado')

    def fazer_login(self):
        try:
            enviar_login = self.chrome.find_element(By.NAME, 'CacheUserName')
            enviar_login.send_keys(login_cache)
            enviar_senha = self.chrome.find_element(By.NAME, 'CachePassword')
            enviar_senha.send_keys(senha_cache)

        except Exception as e:
            print('Erro em fazer_login')
            print('Página não carregada ou usuário já logado')

    def backup_relatorio(self, data):

        # SALVANDO GLOBAL COM Ant
        global_relatorio = self.chrome.find_element(By.ID,"$ID2")
        global_relatorio.clear()

        global_relatorio.send_keys(f"SIATRR({data})")


        # Exibir global pesquisada
        botao_exibir = self.chrome.find_element(By.ID,"BTN_Display")
        botao_exibir.click()


        # Habilitar edição
        habilitar_edicao = self.chrome.find_element(By.ID,"chkEdit")


        if not habilitar_edicao.is_selected():
            habilitar_edicao.click()


        editar_global = self.chrome.find_element(By.CSS_SELECTOR, "body > table > tbody > tr:nth-child(2) > td > form >"
                                                                  " table.DetailTable > tbody > tr.EvenRow >"
                                                                  " td:nth-child(4) > a")

        editar_global.click()

        no_global = self.chrome.find_element(By.ID,"txtGlobal")
        no_global.clear()
        no_global.send_keys(f"^SIATRRant({data})")

        valores_dia = self.chrome.find_element(By.ID,"GValue")

        salvar = self.chrome.find_element(By.ID,"BTN_Insert")
        salvar.click()
        return valores_dia.text

    def editar_relatorio(self, valores, irrf, data):

        relatorio_editado = valores.split("#")

        relatorio_editado[0] = str(int(relatorio_editado[0]) + irrf)

        relatorio_editado[531] = str(int(relatorio_editado[531]) + irrf)
        relatorio_editado = "#".join(relatorio_editado)

        # ABRINDO GLOBAL
        global_relatorio = self.chrome.find_element(By.ID, "$ID2")
        global_relatorio.clear()
        global_relatorio.send_keys(f"SIATRR({data})")

        # Exibir global pesquisada
        botao_exibir = self.chrome.find_element(By.ID, "BTN_Display")
        botao_exibir.click()
        # Habilitar edição
        habilitar_edicao = self.chrome.find_element(By.ID, "chkEdit")

        if not habilitar_edicao.is_selected():
            habilitar_edicao.click()

        editar_global = self.chrome.find_element(By.CSS_SELECTOR, "body > table > tbody > tr:nth-child(2) > td > form >"
                                                 " table.DetailTable > tbody > tr.EvenRow >"
                                                 " td:nth-child(4) > a")
        editar_global.click()

        valores_dia = self.chrome.find_element(By.ID, "GValue")
        valores_dia.clear()

        valores_dia.send_keys(relatorio_editado)

        salvar = self.chrome.find_element(By.ID, "BTN_Insert")
        salvar.click()



def adicionar_irrf(data_completa, adicionar_irrf):

    data_completa = datetime.strftime(data_completa, '%y%m%d')

    chrome = ChromeAuto()

    chrome.acessa(url)
    chrome.fazer_login()
    chrome.clica_entrar()
    valores_dia = chrome.backup_relatorio(data_completa)

    chrome.acessa(url)
    valores_mes = chrome.backup_relatorio(data_completa[0:4] + "00")
    
    chrome.acessa(url)      
    valores_ano = chrome.backup_relatorio(data_completa[0:2] + "0000")

    chrome.acessa(url)
    chrome.editar_relatorio(valores_dia, adicionar_irrf, data_completa)
    
    chrome.acessa(url)
    chrome.editar_relatorio(valores_mes, adicionar_irrf, data_completa[0:4] + "00")

    chrome.acessa(url)
    chrome.editar_relatorio(valores_ano, adicionar_irrf, data_completa[0:2] + "0000")
    chrome.sair()
