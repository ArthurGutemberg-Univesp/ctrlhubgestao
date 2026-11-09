from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from documentos.models import Documento
from fiscal.models import ObrigacaoFiscal
from fiscal.utils import calcular_proximas_datas
from datetime import date

@login_required
def home(request):
    user = request.user
    hoje = date.today()
    
    # 1. Filtro base por perfil
    if user.cargo in ['ADMIN', 'CONTADOR']:
        docs = Documento.objects.all()
        obrigacoes = ObrigacaoFiscal.objects.filter(ativo=True)
    else:
        docs = Documento.objects.filter(cliente=user.empresa)
        obrigacoes = ObrigacaoFiscal.objects.filter(cliente=user.empresa, ativo=True)
        
    # 2. Dados do Gráfico de Documentos
    qtd_fiscais = docs.filter(categoria='FISCAL').count()
    qtd_contratos = docs.filter(categoria='CONTRATO').count()
    qtd_folhas = docs.filter(categoria='FOLHA').count()
    qtd_outros = docs.filter(categoria='OUTROS').count()
    
    # 3. Lógica dos próximos vencimentos
    proximos_vencimentos = []
    for ob in obrigacoes:
        datas = calcular_proximas_datas(ob.data_vencimento_base, ob.periodicidade, meses_adiante=2)
        for d in datas:
            diff = (d - hoje).days
            if diff >= 0:
                proximos_vencimentos.append({
                    'cliente': ob.cliente.razao_social,
                    'tipo': ob.tipo,
                    'data': d,
                    'dias_para_vencer': diff # <-- Isso alimenta os badges coloridos do HTML
                })
                
    # Ordena os vencimentos da data mais próxima para a mais distante
    proximos_vencimentos = sorted(proximos_vencimentos, key=lambda x: x['data'])

    contexto = {
        'total_documentos': docs.count(),
        'total_obrigacoes': obrigacoes.count(),
        'proximos_vencimentos': proximos_vencimentos,
        'grafico_labels': ['Fiscais', 'Contratos', 'Folha', 'Outros'],
        'grafico_dados': [qtd_fiscais, qtd_contratos, qtd_folhas, qtd_outros],
    }
    
    return render(request, 'home.html', contexto)