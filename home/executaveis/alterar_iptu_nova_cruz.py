from .dados_acesso import login_cache, senha_cache
from datetime import date
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium import webdriver

# AMBIENTE DE TESTES
# url = 'https://www2.tinus.com.br/csp/sys/exp/UtilExpGlobalView.csp?%24NAMESPACE=TESTENCR'

# AMBIENTE DE PRODUÇÃO
url = 'https://www.tinus.com.br/csp/sys/exp/UtilExpGlobalView.csp?$ID2=SIATMS&$NAMESPACE=NOVACRUZ'
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
            botao_entrar = self.chrome.find_element(By.NAME,'CacheLogin')
            botao_entrar.click()

        except Exception as e:
            print('Erro na função clica_entrar')
            print('Página não carregada ou usuário já logado')

    def fazer_login(self):
        try:
            enviar_login = self.chrome.find_element(By.NAME,'CacheUserName')
            enviar_login.send_keys(login_cache)
            
            enviar_senha = self.chrome.find_element(By.NAME,'CachePassword')
            enviar_senha.send_keys(senha_cache)
        except Exception as e:
            print('Erro em fazer_login')
            print('Página não carregada ou usuário já logado')

    def backup_lancamento(self, sequencial, exercicios, exercicio_atual):

        # Lista pra guardar os valores originais lançados
        lancamento_original = {}
 
        nome_da_global = ''

        for ano in exercicios:

            # SALVANDO GLOBAL COM Ant
            global_relatorio = self.chrome.find_element(By.ID,"$ID2")
            global_relatorio.clear()

            if ano == exercicio_atual:
                nome_da_global = '^SCICD'
            else:
                nome_da_global = '^SCIDA'


            global_relatorio.send_keys(f"{nome_da_global}({sequencial},{ano})")

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
            no_global.send_keys(f"{nome_da_global}ant({sequencial},{ano})")

            valor_lancado = self.chrome.find_element(By.ID,"GValue").text

            salvar = self.chrome.find_element(By.ID,"BTN_Insert")
            salvar.click()

            lancamento_original[ano] = valor_lancado

        return lancamento_original

    def buscar_uf(self, exercicio_atual):

        global_relatorio = self.chrome.find_element(By.ID, "$ID2")
        global_relatorio.clear()
        global_relatorio.send_keys(f'^SICMPR("U",{exercicio_atual}01')

        botao_exibir = self.chrome.find_element(By.ID, "BTN_Display")
        botao_exibir.click()

        # Habilitar edição
        habilitar_edicao = self.chrome.find_element(By.ID,"chkEdit")

        if not habilitar_edicao.is_selected():
            habilitar_edicao.click()
        
        editar_global = self.chrome.find_element(By.CSS_SELECTOR, "body > table > tbody > tr:nth-child(2) > td > form >"
                                                                    " table.DetailTable > tbody > tr.EvenRow >"
                                                                    " td:nth-child(4) > a")
        editar_global.click()

        return self.chrome.find_element(By.ID,"GValue").text   

    def recalcular_lancamentos(self, lancamentos_originais, uf, valor, exercicio_atual):
        """Função pra alterar os valores de IPTU pra o valor informado"""
        lancamentos_alterados = {}

        for ano, lancamento in lancamentos_originais.items():
            
            if ano == exercicio_atual:

                lancamento_atual = lancamento.split("#")
                qtd_parcelas = int(lancamento_atual[-8])
                a_vista_sem_desconto = float(lancamento_atual[0])
                a_vista_com_desconto = float(lancamento_atual[3])
                parcela = float(lancamento_atual[-7])
                desconto = round(a_vista_com_desconto*100/a_vista_sem_desconto,1)

                novo_a_vista_sem_desconto = round(valor/uf,4)
                novo_a_vista_com_desconto = round(novo_a_vista_sem_desconto/100*desconto,4)
                novo_parcela = round(novo_a_vista_sem_desconto/qtd_parcelas,4)

                lancamento_atual[0] = str(novo_a_vista_sem_desconto)
                lancamento_atual[3] = str(novo_a_vista_com_desconto)
                lancamento_atual[9], lancamento_atual[12] = str(novo_parcela), str(novo_parcela)

                lancamento_alterado = '#'.join(lancamento_atual)
                lancamentos_alterados[ano] = lancamento_alterado
            
            else:

                lancamento_atual = lancamento.split("#")
                qtd_parcelas = int(lancamento_atual[-5][-1])
                if qtd_parcelas == 0: qtd_parcelas = 1
                
                novo_valor = round((valor/uf)/qtd_parcelas,4)

                for piece in range(2,(qtd_parcelas*5+1),6):
                    lancamento_atual[piece] = str(novo_valor)

                lancamento_alterado = '#'.join(lancamento_atual)
                lancamentos_alterados[ano] = lancamento_alterado

        return lancamentos_alterados

    def editar_lancamento(self, sequencial, novos_valores, exercicio_atual):
        nome_da_global = ''

        for ano, lancamento in novos_valores.items():

            # ABRINDO GLOBAL
            global_relatorio = self.chrome.find_element(By.ID,"$ID2")
            global_relatorio.clear()

            if ano == exercicio_atual:
                nome_da_global = '^SCICD'
            else:
                nome_da_global = '^SCIDA'

            global_relatorio.send_keys(f"{nome_da_global}({sequencial},{ano})")
                
            # Exibir global pesquisada
            botao_exibir = self.chrome.find_element(By.ID,"BTN_Display")
            botao_exibir.click()

            # Habilitar edição
            habilitar_edicao = self.chrome.find_element(By.ID,"chkEdit")

            if not habilitar_edicao.is_selected():
                habilitar_edicao.click()

            editar_global = self.chrome.find_element(By.CSS_SELECTOR,"body > table > tbody > tr:nth-child(2) > td > form >"
                                                                    " table.DetailTable > tbody > tr.EvenRow >"
                                                                    " td:nth-child(4) > a")
            editar_global.click()

            valores_dia = self.chrome.find_element(By.ID,"GValue")
            valores_dia.clear()
            valores_dia.send_keys(lancamento)
            
            salvar = self.chrome.find_element(By.ID,"BTN_Insert")
            salvar.click()

def alterar_iptu(sequencial, exercicios, valor):

    # Obtendo o exercício atual atualizado (ano com dois dígitos)
    exercicio_atual = str(date.today().year)[2:]
    
    chrome = ChromeAuto()

    chrome.acessa(url)
    chrome.fazer_login()
    chrome.clica_entrar()

    # Salvando as globais originais com 'ant'
    lancamentos_originais = chrome.backup_lancamento(sequencial, exercicios, exercicio_atual)

    # Obtendo o valor da UF do exercício atual
    uf = float(chrome.buscar_uf(exercicio_atual))/10000
    
    # Recalculandos os valores de IPTU (parcelas e cota única)
    novos_valores = chrome.recalcular_lancamentos(lancamentos_originais, uf, valor, exercicio_atual)

    # Salvando os novos valores calculados
    chrome.editar_lancamento(sequencial, novos_valores, exercicio_atual)
    
    chrome.sair()