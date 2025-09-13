LISTA_MUNICIPIOS = {
        'GAV': {
            'PM S G AVELINO TRIBU001BANCO DO BRASIL':'.001',
            'PMSGA               104CAIXA':'.104'
        },
        'PAR': {
            'PAR BB':'.001',
            'PAR CAIXA':'.104'
        },
}

for sigla in LISTA_MUNICIPIOS:
    print("dict: ",LISTA_MUNICIPIOS[sigla])

    print("MUNICÍPIO = ", sigla)
    
    for header, extensao in LISTA_MUNICIPIOS[sigla].items():
        print("HEADER: ", header)
        print("EXTENSÃO: ",extensao )