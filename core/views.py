from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import date
from fiscal.models import ObrigacaoFiscal
from fiscal.utils import calcular_proximas_datas
from documentos.models import Documento

@login_required
def home(request):
    user = request.user
    ctx = {}

    # Totais conforme cargo
    if user.cargo in ['ADMIN', 'CONTADOR']:
        ctx['total_documentos'] = Documento.objects.count()
        ctx['total_obrigacoes'] = ObrigacaoFiscal.objects.filter(ativo=True).count()
        obrigacoes_ativas = ObrigacaoFiscal.objects.filter(ativo=True)
    else:
        ctx['total_documentos'] = Documento.objects.filter(cliente=user.empresa).count()
        ctx['total_obrigacoes'] = ObrigacaoFiscal.objects.filter(cliente=user.empresa, ativo=True).count()
        obrigacoes_ativas = ObrigacaoFiscal.objects.filter(cliente=user.empresa, ativo=True)

    # Próximos vencimentos (limitado a 5)
    proximos = []
    hoje = date.today()
    for ob in obrigacoes_ativas:
        datas = calcular_proximas_datas(ob.data_vencimento_base, ob.periodicidade, meses_adiante=2)
        for d in datas:
            if d >= hoje:
                proximos.append({
                    'cliente': ob.cliente.razao_social,
                    'tipo': ob.tipo,
                    'data': d,
                })
    proximos.sort(key=lambda x: x['data'])
    ctx['proximos_vencimentos'] = proximos[:5]

    return render(request, 'home.html', ctx)