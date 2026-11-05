from django import forms
from .models import Documento
from core.models import Cliente

class DocumentoUploadForm(forms.ModelForm):
    class Meta:
        model = Documento
        fields = ['titulo', 'descricao', 'categoria', 'arquivo_atual', 'cliente']
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 3}),
            # Removido o HiddenInput daqui – será definido na view conforme o cargo
        }

    def __init__(self, *args, **kwargs):
        # Aceita um kwarg opcional para desabilitar o campo cliente (para clientes)
        self.cliente_fixo = kwargs.pop('cliente_fixo', None)
        super().__init__(*args, **kwargs)
        self.fields['titulo'].widget.attrs.update({'class': 'form-control'})
        self.fields['descricao'].widget.attrs.update({'class': 'form-control'})
        self.fields['categoria'].widget.attrs.update({'class': 'form-select'})
        self.fields['arquivo_atual'].widget.attrs.update({'class': 'form-control'})

        # Se cliente_fixo for fornecido, esconde o campo e define o valor fixo
        if self.cliente_fixo:
            self.fields['cliente'].widget = forms.HiddenInput()
            self.fields['cliente'].initial = self.cliente_fixo
            self.fields['cliente'].disabled = True  # não exibe erro de required
        else:
            # Para contador/admin, mostra dropdown com todos os clientes ativos
            self.fields['cliente'].queryset = Cliente.objects.filter(ativo=True)
            self.fields['cliente'].widget.attrs.update({'class': 'form-select'})