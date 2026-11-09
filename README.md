# 📁 Gestão Documental e Fiscal – CTRL HUB

Sistema web desenvolvido para a disciplina **Projeto Integrador** do curso de **Engenharia da Computação** da **UNIVESP**.  
A aplicação centraliza documentos contábeis, controla obrigações fiscais e emite alertas de vencimento, atendendo à empresa fictícia **CTRL HUB**.

---

## 👥 Integrantes

| Nome | RA |
|---|---|
| Arthur Gutemberg Feitoza de Moraes | 24211162 |
| Inayá Janaina Cardoso de Omena | 24227189 |
| Luiz Guilherme Oliveira Pirossi | 2104559 |
| Marcos Vinicios Sarmento Paes | 23204741 |
| Márcia Chiquete Melo | 24210505 |
| Mayara Sarmento Paes | 2226804 |
| Thiago Barcelos de Oliveira | 23205107 |
| Victória Olga Menegasse Sampaio | 24226317 |

**Tutor(a):** Ana Elisa Teixeira da Silva

---

## 🎯 Objetivo

Mitigar falhas na organização e recuperação de documentos fiscais causadas pelo uso de ferramentas informais (WhatsApp, e-mail).  
O sistema oferece:

*   Repositório centralizado de documentos com controle de versão.
*   Calendário fiscal interativo com lembretes automáticos de prazos.
*   Diferentes níveis de acesso (administrador, contador, cliente).
*   Interface web responsiva e de fácil utilização.

---

## ⚙️ Funcionalidades

- ✅ Autenticação customizada (Admin, Contador, Cliente)
- ✅ Upload, download e versionamento de documentos
- ✅ Filtros por categoria, cliente e busca textual
- ✅ Cadastro de obrigações fiscais com periodicidade
- ✅ Calendário interativo (FullCalendar.js)
- ✅ Geração de lembretes e envio de e-mails de aviso
- ✅ Dashboard com indicadores e próximos vencimentos
- ✅ Controle de acesso baseado no perfil do usuário
- ✅ Comando para popular dados de demonstração

---

## 🛠️ Tecnologias

- **Back-end:** Python 3.10+, Django 4.2 LTS
- **Front-end:** HTML5, CSS3, Bootstrap 5, FullCalendar.js
- **Banco de dados:** SQLite3 (desenvolvimento)
- **Ambiente virtual:** venv
- **Controle de versão:** Git, GitHub

---

## 🚀 Como executar o projeto localmente

### 📋 Pré-requisitos

*   Python 3.10 ou superior
*   Git instalado

### 🛠️ Passos para Instalação

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/seu-usuario/gestao-documentos-fiscais.git](https://github.com/seu-usuario/gestao-documentos-fiscais.git)
   cd gestao-documentos-fiscais
2. **Crie e ative o ambiente virtual:**
    ```bash
    python -m venv venv
    ```

    Windows: 
    ```bash
    venv\Scripts\activate
    ```
    Linux/Mac:
    ```bash
    source venv/bin/activate
    ```

    
3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
4. **Prepare o Banco de Dados:**
    ```bash
    python manage.py migrate
5. **Popule o sistema (Dados de demonstração):**
    ```bash
    python manage.py criar_demo
    ```
    Ou crie um admin manualmente: 
    ```bash
    python manage.py createsuperuser
6. **Inicie o servidor:**
    ```bash
    python manage.py runserver
🌐 Acesso ao Sistema

Sistema: http://127.0.0.1:8000/

Admin: http://127.0.0.1:8000/admin/

## ⌨️ Comandos úteis

- `python manage.py runserver` – inicia o servidor local
- `python manage.py migrate` – aplica migrações pendentes
- `python manage.py createsuperuser` – cria um superusuário
- `python manage.py criar_demo` – popula dados de demonstração
- `python manage.py gerar_lembretes` – envia e-mails de aviso
- `python manage.py limpar_dados` – remove todos os dados do sistema
- `python manage.py limpar_dados --manter-admin` – remove todos os dados exceto superusuários