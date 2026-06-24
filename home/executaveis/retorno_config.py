"""
Usado para renomear os arquivos de retorno, a partir do header, e definir a extensão correta para cada arquivo, de acordo com o executável do município
APENAS PARA A FUNÇÃO WEB
"""

lista_municipios_renomear_off_line = {
    # 'pau':'Paulista',
    'scc':'Santa Cruz do Capibaribe',
    'are':'Arez',
    'ban':'Bananeiras',
    'bel':'Belo Jardim',
    # 'bod':'Bodo',
    'ext':'Extremoz',
    'equ':'Equador',
    'gal':'Galinhos',
    'gav':'Georgino Avelino',    
    'goi':'Goiana',
    'cre':'Campo Redondo',
    'can':'Canguaretama',
    'cai':'Caico',
    'crv':'Caicara do Rio do Vento',
    'goh':'Goianinha',
    'gon':'Sao Goncalo',
    'jds':'Jardim do Serido',
    'ipa':'Ipanguacu',
    'laj':'Lajes',
    'lda':'Lagoa Danta',
    'ldv':'Lagoa de Velhos',
    'luc':'Lucena',
    'mam':'Mamanguape',
    'ncr':'Nova Cruz',
    'nis':'Nisia Floresta',
    'oub':'Ouro Branco',
    'pef':'Passa e Fica',
    'pah':'Parelhas',
    'par':'Parnamirim',
    'pat':'Patu',
    'pav':'Pedro Avelino',
    'pve':'Pedro Velho',
    'pur':'Pureza',
    'rdf':'Rio do Fogo',
    'sbn':'Sao Bento do Norte',
    'smg':'Sao Miguel do Gostoso',
    'snn':'Serra Negra do Norte',
    'sou':'Sousa',
    'sta':'Serra Talhada',
    'sdm':'Serra do Mel',
    'tdb':'Timbauba dos Batistas',
    'uir':'Uirauna',
}

lista_municipios_retorno = {
        'Uirauna': {
            'PREF MUN DE UIRAUNA 001BANCO DO BRASIL':'.001',
            'MUN UIRAUNA         104CAIXA ECON. FEDERAL':'.104'
        },
        'Arez': {
            'ARES ARRECADAÇÃO 001BANCO DO BRASIL':'.001'
        },
        'Belo Jardim': {
            'TRIBUTOS BELO JARDIM001BANCO DO BRASIL':'.001',
            'PREF MUN BELO JARDIM341BANCO ITAU S.A.':'.341',
            'PMBELOJARDIM        104CAIXA ECON. FEDERAL':'.104',
            'PM BELO JARDIM      033BANCO SANTANDER':'.033',
            'PM DE BELO JARDIM - 237BANCO BRADESCO':'.237'
        },
        'Galinhos': {
            'PREF MUN DE GALINHOS001BANCO DO BRASIL':'.001',
            'PMGALINHOS          104CAIXA ECON. FEDERAL':'.104'
        },
        'Georgino Avelino': {
            'PM S G AVELINO TRIBU001BANCO DO BRASIL':'.001',
            'PMSGA               104CAIXA':'.104'
        },
        'Goiana': {
            'PREF MUN DE GOIANA  104CAIXA ECON. FEDERAL':'.104',
            'PREFEITURA MUN GOIAN001BANCO DO BRASIL':'.001',
            'PREF. MUN. DE GOIANA004BANCO DO NORDESTE DO':'.004'
        },
        'Ipanguacu': {
            'PMIPANGUACU         104CAIXA':'.104',
            'ARRECADAÇÃO MUN IPAN001BANCO DO BRASIL':'.001'
        },
        'Lagoa de Velhos': {
            'PM LAGOA VELHOS TRIB001BANCO DO BRASIL':'.001'
        },
        'Mamanguape': {
            'PMM - Tributos Munic001BANCO DO BRASIL':'.001'
        },
        'Ouro Branco': {
            'PREF MUN DE OURO BRA001BANCO DO BRASIL':'.001'
        },
        'Equador': {
            'EQUADOR - ARRECADACA001BANCO DO BRASIL':'.001'
        },
        'Parelhas': {
            'PM DE PARELHAS      104CAIXA ECON. FEDERAL':'.204',
            'PARELHAS - ARRECA001BANCO DO BRASIL':'.904'
        },
        # 'Paulista':{
        #     'IPTU PAULISTA-PE    001BANCO DO BRASIL':'.001',
        #     'PM DE PAULISTA      104CAIXA ECON. FEDERAL':'.104',
        #     'PM PAULISTA         033BANCO SANTANDER':'.033',
        #     'PREF.MUN.DE PAULISTA237BANCO BRADESCO':'.237',
        #     'PREF MUN PAULISTA  P341BANCO ITAU S.A.':'.341',
        #     'PREF. MUN. DE PAULIS004BANCO DO NORDESTE':'.004'
        # },
        'Passa e Fica':{
            'PASSA E FICA PREFEITURA       C ECON FEDERAL':'.904',
            'PM PASSA E FICA RN  104CAIXA ECON. FEDERAL':'.104',
        },
        'Pedro Avelino':{
            'MUN PEDRO AVELINO   104CAIXA ECON. FEDERAL':'.104',
            'ARRECADACAO PM P AVE001BANCO DO BRASIL':'.001',
        },
        'Pedro Velho':{
            'MUN. PEDRO VELHO    104CAIXA ECON. FEDERAL':'.104',
            'PEDRO VELHO ARRECADA001BANCO DO BRASIL ':'.001',
        },
        'Rio do Fogo':{
            'PREF MUN RIO DO FOGO001BANCO DO BRASIL':'.001',
            'PMRIODOFOGO         104CAIXA ECON. FEDERAL':'.104',
        },
        'Sao Miguel do Gostoso': {
            'PREFEITURA MUNICIPAL DE SAO MI237BRADESCO':'.237',  
            'P M SAO MIGUEL DO GO001BANCO DO BRASIL  S/A':'.001',
            'PM S M DO GOSTOSO RN104CAIXA ECON. FEDERAL': '.104',
            'MUNICIPIO DE SAO MIGUEL DO GOS001BANCO DO BRASIL': '.002',
        },
        'Pureza': {
            'ARRECADACAO PUREZA  001BANCO DO BRASIL':'.001',
            'PMPUREZA            104CAIXA ECON. FEDERAL': '.104',
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
            # '570168000000MUNICIPIO DE SERRA NEGRA DO NO001BANCO DO BRASIL':'.004',
            'SERRA NEGRA NORTE TR001BANCO DO BRASIL  S/A':'.005',
        },
        'Serra Talhada': {
            'PREFEITURA MUN S. TA001BANCO DO BRASIL':'.001',
            '577561 MUNICIPIO DE SERRA TALHADA    BANCO DO BRASIL':'.002',
            'PREFEITURA DE SERRA TALHADA   237BRADESCO':'.237',
            'PM SERRA TALHADA    104CAIXA ECON. FEDERAL':'.104',
            'PM DE SERRA TALHADA 033BANCO SANTANDER':'.033',
        },
        'Sao Bento do Norte': {
            'SAO BENTO DO NORTE PREFEITURA C ECON FEDERAL':'.104',
        },

        'Patu': {
            'MUNICIPIO DE PATU TR001BANCO DO BRASIL':'.001'
        },
        # 'Messias Targino':{
        #     'MUN MESSIAS TARGINO 104CAIXA ECON. FEDERAL':'.104',
        #     'MESSIAS TARGINO TRIB001BANCO DO BRASIL':'.001',
        # },
        'Timbauba dos Batistas':{
            'MUNICIPIO DE TIMBAUBA DOS BATI001BANCO DO BRASIL':'.002',
            'PM TIMBAUBA DOS BATI104CAIXA ECON. FEDERAL':'.104'
        },
        'Lajes':{
            'PM LAJES            104CAIXA ECON. FEDERAL':'.104',
            'PREFEITURA MUNIC DE 001BANCO DO BRASIL  S/A':'.001'
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
        'Sousa':{
            
            'PREF. MUN. SOUSA IPT001BANCO DO BRASIL':'.001',
            'PREF DE SOUSA       004BANCO DO NORDESTE':'.004',
            'ARREC PM SOUSA      104CAIXA ECON. FEDERAL':'.104'
        },
        'Extremoz':{
            'PM EXTREMOZ - TRIBUT001BANCO DO BRASIL':'.001',
            'PM EXTREMOZ         104CAIXA ECON. FEDERAL':'.104',
        },
        'Campo Redondo':{
            'PM CAMPO REDONDO RN 104CAIXA ECON. FEDERAL':'.104',
        },
        'Caicara do Rio do Vento':{
            'PREF CAIC RIO DO VEN001BANCO DO BRASIL  S/A':'.001',
        },
        'Canguaretama':{
            'P.M. DE CANGUARETAMA237BANCO BRADESCO S/A':'.237',
            'P M CANGUARETAMA TRI001BANCO DO BRASIL  S/A':'.904',
            '70556 MUNICIPIO DE CANGUARETAMA     BANCO DO BRASIL':'.905',
            '272299 MUNICIPIO DE CANGUARETAMA     BANCO DO BRASIL':'.914',
        },
        'Nisia Floresta':{
            'PMDENISIAFLORESTA   104CAIXA ECON. FEDERAL':'.104',
            'PREF MUN NISIA FLORE001BANCO DO BRASI':'.001',
            'IPTU NISIA FLORESTA 756SICOOB POTIGUAR':'.756',
        },
        'Jardim do Serido':{
            '3512214  2807793':'.001', 
            'MUN JARDIM DO SERIDO001BANCO DO BRASIL  S/A':'.901',
            '3512214  3178850':'.902',
        },
        'Parnamirim':{
            '2008769113600000000FUNDO MUNICIPAL DE SAUDE DE PAC ECON FEDERAL':'.204',
            '779460100000000MUNICIPIO DE PARNAMIRIM       C ECON FEDERAL':'.304',
            'ARRECADACAO PM PARNA001BANCO DO BRASIL':'.001',
            'PM PARNAMIRIM       104CAIXA ECON. FEDERAL':'.104',
            '2008798913700000000MUNICIPIO DE PARNAMIRIM       C ECON FEDERAL':'.404',
        },
        'Nova Cruz':{
            'PM DE NOVA CRUZ - RN237BANCO BRADESCO S/A':'.237',
            'PMNC ARRECADACAO    001BANCO DO BRASIL':'.001',
            'PM DE NOVA CRUZ/RN  104CAIXA ECON. FEDERAL':'.904',
            'PREF MUNICIPAL DE NOVA CRUZ   C ECON FEDERAL':'.104',
        },

        
                
        
    }
def selecionar_municipio(municipio):
    """
    Identifica o muncípio e retorna dicionário com a relação HEADER x Extensão_Arquivo 
    """
    retornos = lista_municipios_retorno.get(municipio)
    return retornos
    