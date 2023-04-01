from django import template
register = template.Library()

@register.filter(name='lista_indice')
def indice(indexavel, i):
    return indexavel[i]

@register.filter(name='situacao')
def situacao(status):
    if status == 'A':
        return 'Em Aberto'
    elif status == 'S':
        return 'Saldo Devedor'

@register.filter(name='data')
def data(vencimento):
    return vencimento[0:2]+"/"+vencimento[2:4]+"/"+vencimento[4:]


@register.filter(name='soma_total_credito')
def soma_total_credito(credito):
    total = 0.0
    for indice in credito:
        total += indice[1]
    soma = 'R$' + str(total)
    return soma
