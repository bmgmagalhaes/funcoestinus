"""
Arquivo para concentrar dados com a relação Município x Retorno x Órgão de todos os municípios
"""

lista_municipios_renomear_off_line = {
    'pau':'Paulista',
    'scc':'Santa Cruz do Capibaribe',
    'are':'Arez',
    'ban':'Bananeiras',
    'bod':'Bodo',
    'ext':'Extremoz',
    'gal':'Galinhos',
    'gav':'Georgino Avelino',    
    'goi':'Goiana',
    'cre':'Campo Redondo',
    'goh':'Goianinha',
    'gon':'Sao Goncalo',
    'laj':'Lajes',
    'lda':'Lagoa Danta',
    'luc':'Lucena',
    'mta':'Messias Targino',
    'nis':'Nisia Floresta',
    'pef':'Passa e Fica',
    'pah':'Parelhas',
    'pat':'Patu',
    'pav':'Pedro Avelino',
    'sbn':'Sao Bento do Norte',
    'smg':'São Miguel do Gostoso',
    'snn':'Serra Negra do Norte',
    'sdm':'Serra do Mel',
    'tdb':'Timbauba dos Batistas',
}

lista_municipios_retorno = {
        'Galinhos': {
            'PREF MUN DE GALINHOS001BANCO DO BRASIL':'.001',
            'PMGALINHOS          104CAIXA ECON. FEDERAL':'.104'
        },
        'Goiana': {
            'PREF MUN DE GOIANA  104CAIXA ECON. FEDERAL':'.104',
            'PREFEITURA MUN GOIAN001BANCO DO BRASIL':'.001'
        },
        'Parelhas': {
            'PM DE PARELHAS      104CAIXA ECON. FEDERAL':'.204',
            'PARELHAS - ARRECA001BANCO DO BRASIL':'.904'
        },
        'Paulista':{
            'IPTU PAULISTA-PE    001BANCO DO BRASIL':'.001',
            'PM DE PAULISTA      104CAIXA ECON. FEDERAL':'.104',
            'PM PAULISTA         033BANCO SANTANDER':'.033',
            'PREF.MUN.DE PAULISTA237BANCO BRADESCO':'.237',
            'PREF MUN PAULISTA  P341BANCO ITAU S.A.':'.341',
            'PREF. MUN. DE PAULIS004BANCO DO NORDESTE':'.004'
        },
        'Passa e Fica':{
            'PASSA E FICA PREFEITURA       C ECON FEDERAL':'.904',
            'PM PASSA E FICA RN  104CAIXA ECON. FEDERAL':'.104',
        },
        'Pedro Avelino':{
            'MUN PEDRO AVELINO   104CAIXA ECON. FEDERAL':'.104',
        },
        'São Miguel do Gostoso': {
            'PREFEITURA MUNICIPAL DE SAO MI237BRADESCO':'.237',
            'P M SAO MIGUEL DO GO001BANCO DO BRASIL  S/A':'.001',
            'PM S M DO GOSTOSO RN104CAIXA ECON. FEDERAL': '.104',
            'PREFEITURA MUNICIPAL DE SAO MI001BANCO DO BRASIL': '.002',
        },
            
        'Sao Goncalo': {
            'MUNICIPIO DE SAO GONCALO DO AMBANCO DO BRASIL':'.901',
            'PMSGAMARANTERN      104CAIXA ECON. FEDERAL':'.104',
            'PMSGA ARRECADACAO   001BANCO DO BRASIL':'.001',
        },
        'Serra Negra do Norte': {
            'MUNICIPIO DE SERRA NEGRA DO NOBANCO DO BRASIL':'.001',
            '272639000000MUNICIPIO DE SERRA NEGRA DO NO001BANCO DO BRASIL':'.002',
            'PM S NEGRA DO NORTE 104CAIXA':'.104',
            '570168000000MUNICIPIO DE SERRA NEGRA DO NO001BANCO DO BRASIL':'.004',
            'SERRA NEGRA NORTE TR001BANCO DO BRASIL  S/A':'.005',
        },
        'Sao Bento do Norte': {
            'SAO BENTO DO NORTE PREFEITURA C ECON FEDERAL':'.104',
        },

        'Patu': {
            'MUNICIPIO DE PATU TR001BANCO DO BRASIL':'.001'
        },
        'Messias Targino':{
            'MUN MESSIAS TARGINO 104CAIXA ECON. FEDERAL':'.104',
            'MESSIAS TARGINO TRIB001BANCO DO BRASIL':'.001',
        },
        'Timbauba dos Batistas':{
            'MUNICIPIO DE TIMBAUBA DOS BATI001BANCO DO BRASIL':'.002'
        },
        'Lajes':{
            'PM LAJES            104CAIXA ECON. FEDERAL':'.104'
        },
        'Lagoa Danta':{
            'PM DE LAGOA DANTA   104CAIXA ECON. FEDERAL':'.104'
        },
        'Bananeiras':{
            'PREF MUN BANANEIRAS 001BANCO DO BRASIL':'.001',
            'PM BANANEIRA PB     104CAIXA ECON. FEDERAL':'.104'
        },
        'Lucena':{
            'PM DE LUCENA/PB     104CAIXA ECON. FEDERAL':'.104',
            'PREF MUNIC LUCENA   001BANCO DO BRASIL':'.001',
        },
        'Goianinha':{
            'PMG-ARREC IMPOSTOS/T001BANCO DO BRASIL':'.001',
            'PM GOIANINHA        104CAIXA ECON. FEDERAL':'.104',
            '307963 MUNICIPIO DE GOIANINHA        BANCO DO BRASIL':'.901',
        },
        'Santa Cruz do Capibaribe':{
            'STA C CAPIBARIBE    001BANCO DO BRASIL':'.001',
            'PM S CRUZ CAPIBARIBE104CAIXA ECON. FEDERAL':'.104',
            'PREF MUN SANTA CRUZ 341BANCO ITAU':'.341',
            'PREF. MUN. DE SANTA 004BANCO DO NORDESTE DO':'.004',
        },
        'Serra do Mel':{
            
            'PREF MUNICIPAL S MEL001BANCO DO BRASIL':'.001',
            '056847000000071867X':'.002',
            'PM SERRA DO MEL     104CAIXA ECON. FEDERAL':'.104',
        },
        'Extremoz':{
            'PM EXTREMOZ - TRIBUT001BANCO DO BRASIL':'.001',
            'PM EXTREMOZ         104CAIXA ECON. FEDERAL':'.104',
        },
        'Campo Redondo':{
            'P M DE CAMPO REDONDO104CAIXA ECON. FEDERAL':'.104',
        },
        
                
        
    }
def selecionar_municipio(municipio):
    """
    Identifica o muncípio e retorna dicionário com a relação HEADER x Extensão_Arquivo 
    """
    retornos = lista_municipios_retorno.get(municipio)
    return retornos
    