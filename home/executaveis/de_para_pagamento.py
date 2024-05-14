from .dados_acesso import login_cache, senha_cache, url_ambiente_de_producao, url_ambiente_de_teste,CHROME_DRIVER_PATH
# from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium  import webdriver



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
            print('Erro na função clica_entrar')

    def fazer_login(self):
        try:
            enviar_login = self.chrome.find_element(By.NAME, 'CacheUserName')
            enviar_login.send_keys(login_cache)
            enviar_senha = self.chrome.find_element(By.NAME, 'CachePassword')
            enviar_senha.send_keys(senha_cache)
        except Exception as e:
            print('Erro em fazer_login')

    def buscar_uf(self):

        global_relatorio = self.chrome.find_element(By.ID, "$ID2")
        global_relatorio.clear()
        global_relatorio.send_keys(f'^SICMPR("U",')

        contador = self.chrome.find_element(By.ID,"NodeCount")
        contador.clear()
        contador.send_keys(f'1000')
        # EXIBIR GLOBAL PESQUISADA
        botao_exibir = self.chrome.find_element(By.ID, "BTN_Display")
        botao_exibir.click()

        return self.chrome.find_element(By.CLASS_NAME, "DetailTable").text

    def parametros_acrescimos(self):

        global_relatorio = self.chrome.find_element(By.ID, "$ID2")
        global_relatorio.clear()
        global_relatorio.send_keys(f"^SIATTB(5)")

        # EXIBIR GLOBAL PESQUISADA
        botao_exibir = self.chrome.find_element(By.ID, "BTN_Display")
        botao_exibir.click()
        return self.chrome.find_element(By.CLASS_NAME, "DetailTable").text

    def extrato_exercicio_anterior(self, sequencial):

        global_relatorio = self.chrome.find_element(By.ID, "$ID2")
        global_relatorio.clear()
        global_relatorio.send_keys(f"SCIDA({sequencial},)")

        contador = self.chrome.find_element(By.ID, "NodeCount")
        contador.clear()
        contador.send_keys(f'1000')

        # EXIBIR GLOBAL PESQUISADA
        botao_exibir = self.chrome.find_element(By.ID, "BTN_Display")
        botao_exibir.click()
        return self.chrome.find_element(By.CLASS_NAME, "DetailTable").text

    def listar_pagamentos_exercicio_anterior(self, sequencial):

        global_relatorio = self.chrome.find_element(By.ID, "$ID2")
        global_relatorio.clear()
        global_relatorio.send_keys(f"SCIDA({sequencial},,")

        contador = self.chrome.find_element(By.ID, "NodeCount")
        contador.clear()
        contador.send_keys(f'1000')
        # EXIBIR GLOBAL PESQUISADA
        botao_exibir = self.chrome.find_element(By.ID, "BTN_Display")
        botao_exibir.click()
        return self.chrome.find_element(By.CLASS_NAME, "DetailTable").text

    def extrato_exercicio_atual(self, sequencial):

        global_relatorio = self.chrome.find_element(By.ID, "$ID2")
        global_relatorio.clear()
        global_relatorio.send_keys(f"SCICD({sequencial},)")

        # EXIBIR GLOBAL PESQUISADA
        botao_exibir = self.chrome.find_element(By.ID, "BTN_Display")
        botao_exibir.click()
        return self.chrome.find_element(By.CLASS_NAME, "DetailTable").text

    def listar_pagamentos_exercicio_atual(self, sequencial):

        global_relatorio = self.chrome.find_element(By.ID, "$ID2")
        global_relatorio.clear()
        global_relatorio.send_keys(f"SCICD({sequencial},,")

        # EXIBIR GLOBAL PESQUISADA
        botao_exibir = self.chrome.find_element(By.ID, "BTN_Display")
        botao_exibir.click()
        return self.chrome.find_element(By.CLASS_NAME, "DetailTable").text

    def gravar_globais_cache(self, globais):

        for parcela, pagamento_adicional in globais.items():
            # VERIFICAR SE A GLOBAL EXISTE
            global_relatorio = self.chrome.find_element(By.ID, "$ID2")
            global_relatorio.clear()
            global_relatorio.send_keys(f"{parcela}")

            # EXIBIR GLOBAL PESQUISADA
            botao_exibir = self.chrome.find_element(By.ID, "BTN_Display")
            botao_exibir.click()

            pesquisa_global = self.chrome.find_element(By.CLASS_NAME, "DetailTable").text

            if "Total: 0" in pesquisa_global:
                # EDITA A PESQUISA PRA LISTAR GLOBAL DO EXERCICIO, JÁ QUE NÃO HÁ PARCELA PRA EDITAR
                segunda_virgula = parcela.find(',',parcela.find(',')+1)
                global_do_exercicio = parcela[0:segunda_virgula]+")"

                global_relatorio = self.chrome.find_element(By.ID, "$ID2")
                global_relatorio.clear()
                global_relatorio.send_keys(f"{global_do_exercicio}")

                # EXIBIR GLOBAL PESQUISADA
                botao_exibir = self.chrome.find_element(By.ID, "BTN_Display")
                botao_exibir.click()

                # Habilitar edição
                habilitar_edicao = self.chrome.find_element(By.ID, "chkEdit")

                if not habilitar_edicao.is_selected():
                    habilitar_edicao.click()

                editar_global = self.chrome.find_element(By.CSS_SELECTOR,
                                                         "body > table > tbody > tr:nth-child(2) > td > form >"
                                                         " table.DetailTable > tbody > tr.EvenRow >"
                                                         " td:nth-child(4) > a")
                editar_global.click()

                texto_no_global = self.chrome.find_element(By.ID, "txtGlobal")
                texto_no_global.clear()
                texto_no_global.send_keys(parcela.replace("(","ant("))
                valores = self.chrome.find_element(By.ID, "GValue")
                valores.clear()

                salvar = self.chrome.find_element(By.ID, "BTN_Insert")
                salvar.click()

                texto_no_global.clear()
                texto_no_global.send_keys(parcela)

                valores.clear()
                valores.send_keys(pagamento_adicional)
                salvar.click()

            else:
                # Habilitar edição
                habilitar_edicao = self.chrome.find_element(By.ID, "chkEdit")

                if not habilitar_edicao.is_selected():
                    habilitar_edicao.click()

                editar_global = self.chrome.find_element(By.CSS_SELECTOR,
                                                         "body > table > tbody > tr:nth-child(2) > td > form >"
                                                         " table.DetailTable > tbody > tr.EvenRow >"
                                                         " td:nth-child(4) > a")
                editar_global.click()

                valor_pagamento_anterior = self.chrome.find_element(By.ID, "GValue").text
                novo_valor_pagamento = valor_pagamento_anterior+"#"+pagamento_adicional

                texto_no_global = self.chrome.find_element(By.ID, "txtGlobal")

                bkp_no_global = parcela.replace("(","ant(")

                texto_no_global.clear()
                texto_no_global.send_keys(bkp_no_global)

                salvar = self.chrome.find_element(By.ID, "BTN_Insert")
                salvar.click()

                texto_no_global.clear()
                texto_no_global.send_keys(parcela)

                valores = self.chrome.find_element(By.ID, "GValue")
                valores.clear()
                valores.send_keys(novo_valor_pagamento)

                salvar.click()

        return True

def carregar_situacao_atual_do_imovel_para(sequencial_para, namespace):
    chrome = ChromeAuto()

    # SE FOR AMBIENTE DE TESTE
    if 'TESTE' in namespace:
        url = url_ambiente_de_teste + namespace
    else:
        # AMBIENTE DE PRODUÇÃO
        url = url_ambiente_de_producao + namespace  

    chrome.acessa(url)
    chrome.fazer_login()
    chrome.clica_entrar()

    # PEGAR LANÇAMENTOS E PAGAMENTOS DO EXERCÍCIO ANTERIOR
    extrato_ex_anterior = chrome.extrato_exercicio_anterior(sequencial_para)
    pagamentos_ex_anterior = chrome.listar_pagamentos_exercicio_anterior(sequencial_para)

    # PEGAR LANÇAMENTOS E PAGAMENTOS DO EXERCÍCIO ATUAL
    extrato_ex_atual = chrome.extrato_exercicio_atual(sequencial_para)
    pagamentos_ex_atual = chrome.listar_pagamentos_exercicio_atual(sequencial_para)

    # LISTA DE UF E PARÂMETROS PRA CALCULAR ACRÉSCIMOS DO MUNICÍPIO
    uf = chrome.buscar_uf()
    parametros_acrescimos = chrome.parametros_acrescimos()

    chrome.sair()
    return extrato_ex_anterior, pagamentos_ex_anterior, extrato_ex_atual, pagamentos_ex_atual, uf, parametros_acrescimos


def gravar_globais_com_pagamentos(namespace, globais):
    chrome = ChromeAuto()

    #SE FOR AMBIENTE DE TESTE
    if 'TESTE' in namespace:
        url = url_ambiente_de_teste + namespace
    else:
        # AMBIENTE DE PRODUÇÃO
        url = url_ambiente_de_producao + namespace

    chrome.acessa(url)
    chrome.fazer_login()
    chrome.clica_entrar()

    chrome.gravar_globais_cache(globais)

    chrome.sair()
    # return namespace