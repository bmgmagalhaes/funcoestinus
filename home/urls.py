from django.urls import path#, include
from . import views

urlpatterns = [
    path('', views.index),
    path('baixar_retorno/', views.baixar_retorno, name='baixar_retorno2'),
    path('baixar_retorno_beta/', views.baixar_retorno_beta, name='baixar_retorno_beta'),

    path('iss_nisia/', views.iss_nisia, name='iss_nisia'),
    path('irrf_bananeiras/', views.irrf_bananeiras, name='irrf_bananeiras'),
    path('juncao_agz/', views.juncao_agz, name='juncao_agz'),
    path('juncao_agz_dia/', views.juncao_agz_de_um_dia, name='juncao_agz_de_um_dia'),
    path('alterar_iptu_nova_cruz/', views.iptu_nova_cruz, name='alterar_iptu_nova_cruz'),
    
    path('transferencia_pagamentos/', views.transferencia_pagamento, name='transferencia_pagamento'),
    path('transferencia_pagamentos_md/', views.transferencia_pagamento_md, name='transferencia_pagamento_md'),

    path('lista_pagamentos/', views.exibir_pagamentos, name='listar_pagamentos'),
    path('lista_global/', views.listar_global, name='listar_global'),
    path('salva_global/', views.salvar_global, name='salvar_global'),
    path('transf_itbi/', views.transferencia_itbi, name='transferencia_itbi'),
    path('<str:municipio>', views.renomear, name='renomear'),

    path('de_para_pagamento/', views.de_para_pagamentos, name='de_para_pagamento'),
    path('escolher_parcelas/', views.escolher_parcelas, name='escolher_parcelas'),
    path('informar_creditos/', views.informar_creditos, name='informar_creditos'),
    path('resumo_compensacao/', views.resumo_compensacao, name='resumo_compensacao'),
    path('gerar_globais_pagamentos/', views.gerar_globais_pagamentos, name='gerar_globais_pagamentos'),
    path('gravar_globais_pagamentos/', views.gravar_globais_pagamentos, name='gravar_globais_pagamentos'),

]


