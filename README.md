# 📘 Projeto Django
## 🔧 Requisitos
### Ambiente
* **Python**: 3.13.5
* **Django**: 5.2.6
* **MySQL**: 8.0.43
* **MySQL Workbench**: 8.0 CE
### Dependências
Para instalar as dependência execute o comando:
```bash
python -m pip install -r requirements.txt
```
Ou instale as dependências manualmente.

---
## 🚀 Passos para rodar
1. **Clonar o projeto**
Clone o repositório do GitHub (recomendado clonar dentro de um *project environment*).
[Como criar um ambiente virtual (project environment)](https://github.com/Darlan-Jose/Trabalho-Programacao-Internet/blob/main/README.md#como-criar-um-ambiente-virtual-visual-studio-code)  
```bash
git clone https://github.com/Darlan-Jose/Trabalho-Programacao-Internet.git
cd Trabalho-Programacao-Internet
```
2. [Instale as dependências](https://github.com/Darlan-Jose/Trabalho-Programacao-Internet#depend%C3%AAncias
3. **Criar o banco de dados**
Crie um banco de dados MySQL, preferencialmente com o nome `stc`.
> ⚠️ Caso utilize outro nome, será necessário alterar a configuração de `DATABASES` no arquivo `settings.py`.
4. **Criar o usuário no MySQL**
Veja as instruções na seção [Criando um usuário no MySQL Workbench (Windows)](https://github.com/Darlan-Jose/Trabalho-Programacao-Internet/blob/main/README.md#%EF%B8%8F-criando-um-usu%C3%A1rio-no-mysql-workbench-windows)
5. **Rodar as migrações**

No ambiente virtual do projeto, execute:
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createcachetable
python manage.py popular_banco
python manage.py popular_banco --reset #Mesmo comando do que acima, mas para resetar e recriar
```
6. **Iniciar o servidor**
```bash
python manage.py runserver
```

> ⚠️ Para testar as funcionalidades de CRUD, é necessário acessar o menu de admin do django, por isso crie um superusuário antes de executar o comando acima, instruções sobre como criar um [superusuário](Criando um Superusuário (Admin) no Django).

7. **Acessar no navegador**
Abra: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---
## 👥 Usuário/senha de teste
**Admin**
* Nome: `root`
* Senha: `test`  

**Dealer**
-  Nome: `D001`
* Senha: `dealer123`
  
---
## 👤 Criando um Superusuário (Admin) no Django:
1. **Crie o superusuário:**
Execute o comando abaixo e siga as instruções do terminal:
`python manage.py createsuperuser`
2. Acesse o painel admin
Abra o navegador e vá para:
`http://127.0.0.1:8000/admin/`
Entre com o **username** e **senha** criados no passo 1.
  
---
  
## 🔄 Resumo do fluxo da aplicação
- A aplicação começa na rota `/`.
- O usuário faz login em `/login`, onde as credenciais são validadas, a sessão é criada e o ID da sessão é regenerado.
- Se o usuário for **administrador**, será redirecionado para `/admin/dashboard`.
- Se for **dealer**, será direcionado para `/dealer/dashboard`.

> ⚠️ Sempre que alguém tentar acessar uma página protegida sem uma sessão válida, será redirecionado para `/login`.

---
# Integração com a API ViaCEP
## Por que a ViaCEP?
A API da ViaCEP foi escolhida porque facilita o preenchimento do endereço durante a compra. Ao informar o CEP, os demais campos são preenchidos automaticamente, tornando a experiência mais rápida e reduzindo erros de digitação.

Além disso, ela oferece outras vantagens:
- É amplamente utilizada e confiável no Brasil.
- Não exige autenticação para uso.
- É gratuita, sendo uma ótima opção para projetos acadêmicos e educacionais.
## 2. Descrição Técnica
### Finalidade
A API recebe um CEP e retorna os dados completos do endereço correspondente. Isso agiliza o preenchimento do formulário e evita inconsistências causadas por digitação manual.
### Endpoints utilizados
- **Consulta por CEP:** `GET https://viacep.com.br/ws/{cep}/json/`
- **Consulta por endereço:** `GET https://viacep.com.br/ws/{UF}/{cidade}/{logradouro}/json/`
### Entrada e saída
- **Entrada:** CEP informado na URL.
- **Saída:** Resposta em formato JSON contendo os dados do endereço.
- **Exemplo:**

```json
{
"cep": "01001-000",
"logradouro": "Praça da Sé",
"complemento": "lado ímpar",
"bairro": "Sé",
"localidade": "São Paulo",
"uf": "SP",
"ibge": "3550308",
"gia": "1004",
"ddd": "11",
"siafi": "7107"
}

```
### Autenticação
A ViaCEP não exige autenticação para uso não comercial.
### Limitações
- Limite recomendado de até 10 requisições por segundo.
- Alta disponibilidade, mas sem SLA oficial.
- Aceita apenas CEPs válidos com 8 dígitos.
- É recomendado utilizar timeout de até 10 segundos nas requisições.
### Como a integração funciona
**1. Modelo (`models.py`)**
O modelo armazena o endereço completo da compra sempre que essas informações estiverem disponíveis.

```python
cep = models.CharField(max_length=9, verbose_name='CEP', blank=True)
street = models.CharField(max_length=100, verbose_name='Rua', blank=True)
# ... outros campos
```

**2. View (`views.py`)**
Foi criado um endpoint próprio para centralizar a comunicação com a ViaCEP. Isso facilita o tratamento de erros e permite implementar cache futuramente sem alterar o restante da aplicação.
https://github.com/Darlan-Jose/Trabalho-Programacao-Internet/blob/cab410fa7bfa32901ca23c3c1c52ee40ff60146d/authentication/views.py#L585

**3. Template (purchase_form.html):**
O formulário consulta automaticamente o CEP informado e preenche os campos disponíveis. Caso seja necessário, o usuário ainda pode completar ou corrigir as informações manualmente.
https://github.com/Darlan-Jose/Trabalho-Programacao-Internet/blob/cab410fa7bfa32901ca23c3c1c52ee40ff60146d/authentication/templates/authentication/purchase_form.html#L34
### Decisões Técnicas
1. **Endpoint próprio (/api/cep/)**
Centralizar a consulta em um endpoint da própria aplicação permite tratar erros de forma consistente, facilitar futuras otimizações, como cache, e reduzir o acoplamento com a API externa
2. **Timeout de 10 segundos**Foi definido um tempo máximo de espera para evitar que o usuário fique preso caso a API demore a responder.
3. **Feedback visual**
Mensagens de sucesso e erro ajudam o usuário a entender o que está acontecendo durante a busca pelo CEP.
4. **Campos opcionais**
Nem todas as informações do endereço estão disponíveis no momento da compra. Por isso, alguns campos permanecem opcionais.
### Exemplo do fluxo
1. O usuário digita "01001000".
2. O JavaScript detecta 8 dígitos e chama `/api/cep/01001000/`.
3. A View valida o CEP e consulta a API.
4. A ViaCEP retorna o endereço.
5. O backend formata e envia o JSON.
6. O frontend preenche rua, bairro, cidade e estado.
7. O usuário só completa o número e finaliza a compra.

---

## 🛠️ Criando um usuário no MySQL Workbench (Windows)
Este passo a passo mostra como criar um usuário chamado `django_user` com permissões administrativas utilizando o MySQL Workbench.
### Pré-requisitos
Antes de começar, verifique se você possui:
- MySQL Server instalado;
- MySQL Workbench instalado;
- acesso a um usuário administrador, como o `root`. 
### Passo a passo
1. Abra o **MySQL Workbench** e conecte-se ao seu servidor.
2. No menu superior, acesse **Server → Users and Privileges**.
3. Clique em **Add Account** e preencha os seguintes campos:
    - **Login Name:** `django_user`
    - **Authentication Type:** Standard
    - **Limit Connectivity to Hosts Matching:** `%` (ou `localhost`, se preferir restringir o acesso)
    - **Password:** `senha123` (caso utilize outra senha, lembre-se de atualizá-la no `settings.py`)
    - **Confirm Password:** repita a senha.
4. Abra a aba **Administrative Roles** e marque a opção **DBA**, caso queira conceder acesso administrativo completo.
    Se preferir restringir o acesso a apenas um banco de dados, utilize a aba **Schema Privileges**.
5. Clique em **Apply** para salvar as alterações.

  

---

## Como criar um ambiente virtual (Visual Studio Code)

### Requisitos:

Antes de criar o ambiente virtual, faça o seguinte:

1. Instale a extensão oficial do Python para o VS Code.
2. Instale uma versão do Python 3 compatível com o projeto.
    - Windows, Linux e macOS: utilize a versão disponível em python.org.
    - No Linux, caso necessário, instale também o `python3-pip`.
3. No Windows, confirme que o diretório do Python está configurado na variável de ambiente **PATH**.

### Criando o ambiente virtual:
1. Crie uma pasta para o projeto.
2. Dentro dela, execute o comando para criar um ambiente virtual chamado `.venv`:
```bash
# Linux
sudo apt-get install python3-venv # If needed
python3 -m venv .venv
source .venv/bin/activate

# macOS
python3 -m venv .venv
source .venv/bin/activate 

# Windows
py -3 -m venv .venv
.venv\scripts\activate
```
3. Abra essa pasta no VS Code.
4. Pressione **Ctrl + Shift + P** e execute o comando **Python: Select Interpreter**.    
5. Selecione o interpretador localizado na pasta `.venv` do projeto.
6. Abra um novo terminal pelo VS Code. O ambiente virtual normalmente será ativado automaticamente.

> **Observação:** Se estiver usando PowerShell e aparecer um erro relacionado à execução de scripts (`activate.ps1`), altere o terminal padrão para **Command Prompt** ou **Git Bash**, ou habilite a execução de scripts conforme a documentação da Microsoft.

7. Verifique se o ambiente ativo aparece na barra de status do VS Code.
8. Por fim, atualize o `pip` antes de instalar as dependências do projeto.
## 🔗 Configurando no Django
1. **Instalar conector MySQL**
```bash
pip install mysqlclient
```
> No Windows, pode ser necessário também:
```bash
pip install wheel
```
Alternativa:
```bash
pip install pymysql
```
2. **Editar `settings.py`**

Configure o banco de dados:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'stc',
        'USER': os.environ.get("DB_USER"),
        'PASSWORD': os.environ.get("DB_PASSWORD"),
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```
