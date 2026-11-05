from datetime import date
from dateutil.relativedelta import relativedelta

def calcular_proximas_datas(data_base, periodicidade, meses_adiante=3):
    hoje = date.today()
    datas = []
    data_atual = data_base

    # Ajusta para a primeira data que é >= hoje (ou a própria base, se futura)
    while data_atual < hoje:
        if periodicidade == 'MENSAL':
            data_atual += relativedelta(months=1)
        elif periodicidade == 'TRIMESTRAL':
            data_atual += relativedelta(months=3)
        elif periodicidade == 'ANUAL':
            data_atual += relativedelta(years=1)

    # A data_atual agora é o primeiro vencimento válido; vamos adicioná-la
    datas.append(data_atual)

    # Gera os próximos vencimentos (meses_adiante - 1, pois o primeiro já foi)
    for _ in range(meses_adiante * 12):  # limite de segurança alto
        if periodicidade == 'MENSAL':
            data_atual += relativedelta(months=1)
        elif periodicidade == 'TRIMESTRAL':
            data_atual += relativedelta(months=3)
        elif periodicidade == 'ANUAL':
            data_atual += relativedelta(years=1)
        else:
            break
        datas.append(data_atual)
        if len(datas) >= meses_adiante:
            break

    return datas