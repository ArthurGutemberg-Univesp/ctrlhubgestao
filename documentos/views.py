from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.db.models import Q
from .models import Documento, VersaoDocumento
from .forms import DocumentoUploadForm
from core.models import Cliente

@login_required
def lista_documentos(request):
    user = request.user
    if user.cargo == 'ADMIN' or user.cargo == 'CONTADOR':
        docs = Documento.objects.all()
    else:  # CLIENTE
        docs = Documento.objects.filter(cliente=user.empresa)

    # Filtros via GET
    categoria = request.GET.get('categoria')
    cliente_id = request.GET.get('cliente')
    search = request.GET.get('search')

    if categoria:
        docs = docs.filter(categoria=categoria)
    if cliente_id and (user.cargo in ['ADMIN', 'CONTADOR']):
        docs = docs.filter(cliente_id=cliente_id)
    if search:
        docs = docs.filter(Q(titulo__icontains=search) | Q(descricao__icontains=search))

    return render(request, 'documentos/lista.html', {
        'documentos': docs,
        'categorias': Documento.CATEGORIA_CHOICES,
        'clientes': Cliente.objects.filter(ativo=True) if user.cargo in ['ADMIN', 'CONTADOR'] else None,
    })

@login_required
def upload_documento(request):
    if request.method == 'POST':
        form = DocumentoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.responsavel = request.user
            doc.save()
            messages.success(request, 'Documento enviado com sucesso.')
            return redirect('lista_documentos')
    else:
        # Se for cliente, fixa o cliente no formulário
        if request.user.cargo == 'CLIENTE' and request.user.empresa:
            form = DocumentoUploadForm(cliente_fixo=request.user.empresa)
        else:
            form = DocumentoUploadForm()

    return render(request, 'documentos/upload.html', {'form': form})

@login_required
def detalhe_documento(request, pk):
    doc = get_object_or_404(Documento, pk=pk)
    # Verifica permissão
    if request.user.cargo == 'CLIENTE' and doc.cliente != request.user.empresa:
        messages.error(request, 'Acesso negado.')
        return redirect('lista_documentos')

    versoes = doc.versoes.all()
    return render(request, 'documentos/detalhe.html', {'documento': doc, 'versoes': versoes})

@login_required
def nova_versao(request, pk):
    doc = get_object_or_404(Documento, pk=pk)
    if request.user.cargo == 'CLIENTE' and doc.cliente != request.user.empresa:
        messages.error(request, 'Acesso negado.')
        return redirect('lista_documentos')

    if request.method == 'POST':
        arquivo = request.FILES.get('arquivo')
        comentario = request.POST.get('comentario', '')
        if arquivo:
            nova_versao = doc.versao_atual + 1
            VersaoDocumento.objects.create(
                documento=doc,
                arquivo=arquivo,
                numero_versao=nova_versao,
                usuario=request.user,
                comentario=comentario
            )
            # Atualiza o arquivo atual e incrementa versão
            doc.arquivo_atual = arquivo
            doc.versao_atual = nova_versao
            doc.save()
            messages.success(request, f'Versão {nova_versao} adicionada.')
        return redirect('detalhe_documento', pk=doc.pk)
    return render(request, 'documentos/nova_versao.html', {'documento': doc})

@login_required
def relatorio_documentos(request):
    user = request.user
    if user.cargo in ['ADMIN', 'CONTADOR']:
        docs = Documento.objects.all()
    else:
        docs = Documento.objects.filter(cliente=user.empresa)

    # Filtro por período
    inicio = request.GET.get('inicio')
    fim = request.GET.get('fim')
    if inicio and fim:
        try:
            inicio_date = datetime.strptime(inicio, '%Y-%m-%d')
            fim_date = datetime.strptime(fim, '%Y-%m-%d')
            docs = docs.filter(data_criacao__date__gte=inicio_date, data_criacao__date__lte=fim_date)
        except ValueError:
            pass

    return render(request, 'documentos/relatorio.html', {'documentos': docs})