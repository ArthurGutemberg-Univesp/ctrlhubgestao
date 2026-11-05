from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ObrigacaoFiscal, LembreteFiscal
from .utils import calcular_proximas_datas
from core.models import Cliente

@login_required
def lista_obrigacoes(request):
    user = request.user
    if user.cargo in ['ADMIN', 'CONTADOR']:
        obrigacoes = ObrigacaoFiscal.objects.filter(ativo=True)
        cliente_id = request.GET.get('cliente')
        if cliente_id:
            obrigacoes = obrigacoes.filter(cliente_id=cliente_id)
        clientes = Cliente.objects.filter(ativo=True)
    else:
        obrigacoes = ObrigacaoFiscal.objects.filter(cliente=user.empresa, ativo=True)
        clientes = None

    return render(request, 'fiscal/lista_obrigacoes.html', {
        'obrigacoes': obrigacoes,
        'clientes': clientes,
    })

@login_required
def calendario_fiscal(request):
    """
    Gera eventos para o FullCalendar: para cada obrigação ativa,
    calcula as próximas 6 datas e retorna JSON.
    """
    import json
    from django.http import JsonResponse
    from datetime import date

    user = request.user
    if user.cargo in ['ADMIN', 'CONTADOR']:
        obrigacoes = ObrigacaoFiscal.objects.filter(ativo=True)
    else:
        obrigacoes = ObrigacaoFiscal.objects.filter(cliente=user.empresa, ativo=True)

    eventos = []
    cores = {'MENSAL': '#007bff', 'TRIMESTRAL': '#28a745', 'ANUAL': '#ffc107'}

    for ob in obrigacoes:
        datas = calcular_proximas_datas(ob.data_vencimento_base, ob.periodicidade, meses_adiante=6)
        for venc in datas:
            eventos.append({
                'title': f"{ob.cliente.razao_social} - {ob.tipo}",
                'start': venc.isoformat(),
                'color': cores.get(ob.periodicidade, '#6c757d'),
            })

    return JsonResponse(eventos, safe=False)


@login_required
def pagina_calendario(request):
    return render(request, 'fiscal/calendario.html')