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
py -m pip install -r requirements.txt
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

2. [Instale as dependências](https://github.com/Darlan-Jose/Trabalho-Programacao-Internet#depend%C3%AAncias)

3. **Criar o banco de dados**
   Crie um banco de dados MySQL, preferencialmente com o nome `stc`.

   > ⚠️ Caso utilize outro nome, será necessário alterar a configuração de `DATABASES` no arquivo `settings.py`.

4. **Criar o usuário no MySQL**
   Veja o tutorial completo na seção [Criando um usuário no MySQL Workbench (Windows)](https://github.com/Darlan-Jose/Trabalho-Programacao-Internet/blob/main/README.md#%EF%B8%8F-criando-um-usu%C3%A1rio-no-mysql-workbench-windows)
5. **Rodar as migrações**
   No ambiente virtual do projeto, execute:

   ```bash
   py manage.py migrate
   py manage.py createcachetable
   py manage.py popular_banco
   python manage.py popular_banco --reset #Mesmo comando do que acima, mas para resetar e recriar
   ```

6. **Iniciar o servidor**

   ```bash
   py manage.py runserver
   ```
> ⚠️ Para testar as funcionalidades de CRUD, é necessário acessar o menu de admin do django, por isso crie um superusuário antes de executar o comando acima, instruções sobre como criar um [superusuário](https://github.com/Darlan-Jose/Repositorio-teste#-criando-um-superusu%C3%A1rio-admin-no-django)).
7. **Acessar no navegador**
   Abra: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 👥 Usuário/senha de teste

**Admin**

* Nome: `root`
* Senha: `test`

**Dealer**

* Nome: `D001`
* Senha: `dealer123`

---

## 👤 Criando um Superusuário (Admin) no Django:
1. **Crie o superusuário:**
Execute o comando abaixo e siga as instruções do terminal:

`py manage.py createsuperuser`

Você precisará informar:

- **Username** (nome de usuário)
    
- **Email** (opcional)
    
- **Password** (senha)

2. Acesse o painel admin
Abra o navegador e vá para:
`http://127.0.0.1:8000/admin/`
Entre com o **username** e **senha** criados no passo 1.

---

## 🔄 Descrição breve do fluxo

* **Acesso inicial** → `/`
* **Login** → `/login` *(valida, cria sessão, regenera ID)*
* Se **admin** → `/admin/dashboard`
* Se **dealer** → `/dealer/dashboard`

> ⚠️ Qualquer tentativa de acessar páginas restritas sem sessão válida → redireciona para `/login`.

---

## 🛠️ Criando um usuário no MySQL Workbench (Windows)

Este tutorial mostra como criar um usuário no MySQL chamado `django_user`, com permissões completas para manipular bancos de dados.
O exemplo foi feito no **MySQL Workbench**, rodando no **Windows**.

### Pré-requisitos

* MySQL Server instalado
* MySQL Workbench instalado
* Acesso a um usuário administrador do MySQL (ex: `root`)

### Passo a passo

1. **Abrir o MySQL Workbench**

   * Inicie o MySQL Workbench.
   * Conecte-se ao servidor (ex.: *Local instance MySQL* ou *Local instance MySQL80*).

2. **Acessar a tela de gerenciamento de usuários**

   * Menu: **Server → Users and Privileges**

3. **Criar um novo usuário**

   * Aba **Users and Privileges**
   * Clique em **Add Account**
   * Configure:

     * **Login Name**: `django_user`
     * **Authentication Type**: *Standard*
     * **Limit Connectivity to Hosts Matching**: `%` *(qualquer host; se quiser restringir, use `localhost` ou um IP específico)*
     * **Password**: `senha123` *(recomendado; se usar outra senha, altere em `settings.py`)*
     * **Confirm Password**: repetir a senha

4. **Conceder privilégios**

   * Aba **Administrative Roles**
   * Selecione **DBA** *(Database Administrator → acesso total)*
   * Opcional: em **Schema Privileges**, adicione privilégios para um schema específico (ex.: `stc`).

5. **Aplicar alterações**

   * Clique em **Apply**

---
## Como criar um ambiente virtual (Visual Studio Code)
### Requisitos:
1. Instalar a extensão do Python: https://marketplace.visualstudio.com/items?itemName=ms-python.python
2. Instale uma versão do Python 3 (para a qual este tutorial foi escrito). As opções incluem:
* (Todos os sistemas operacionais) Um download em python.org; normalmente, use o botão "Baixar Python 3.9.1" que aparece primeiro na página (ou qualquer que seja a versão mais recente). 
* (Linux) A instalação integrada do Python 3 funciona bem, mas para instalar outros pacotes do Python, você deve executar sudo apt install python3-pip no terminal.
* (MacOS) Uma instalação via Homebrew no macOS usando brew install python3 (a instalação do sistema do Python no macOS não é suportada).

3. No Windows, certifique-se de que a localização do seu interpretador Python esteja incluída na variável de ambiente PATH. Você pode verificar a localização executando path no prompt de comando. Se a pasta do interpretador Python não estiver incluída, abra as Configurações do Windows, procure por "ambiente", selecione Editar variáveis ​​de ambiente para sua conta e edite a variável Path para incluir essa pasta.
### Criando o ambiente virtual:
1. No seu sistema de arquivos, crie uma pasta de projeto para este tutorial, como hello_django.

2. Nessa pasta, use o seguinte comando (conforme apropriado para o seu computador) para criar um ambiente virtual chamado .venv com base no seu interpretador atual:
```bash
# Linux
sudo apt-get install python3-venv    # If needed
python3 -m venv .venv
source .venv/bin/activate

# macOS
python3 -m venv .venv
source .venv/bin/activate

# Windows
py -3 -m venv .venv
.venv\scripts\activate
```

3. Abra a pasta do projeto no VS Code executando code . ou executando o VS Code e usando o comando File > Open Folder.

4. No VS Code, abra o Command Palette (View > Command Palette or (Ctrl+Shift+P)). Em seguida, selecione Python: Select Interpreter.

5. O comando apresenta uma lista de interpretadores disponíveis que o VS Code pode localizar automaticamente (a lista pode variar; se você não encontrar o interpretador desejado, consulte https://code.visualstudio.com/docs/python/environments). Na lista, selecione o ambiente virtual na pasta do seu projeto que começa com `./.venv` ou `.\.venv`.

6. Executar Terminal: Create New Terminal (Ctrl+Shift+`) no Command Palette, que cria um terminal e ativa automaticamente o ambiente virtual executando seu script de ativação.
>Nota: no Windows, se o seu tipo de terminal padrão for o PowerShell, você poderá ver um erro informando que o activate.ps1 não pode ser executado porque a execução de scripts está desabilitada no sistema. O erro fornece um link com informações sobre como permitir scripts Caso contrário, use o Terminal: Select Default Profile para definir o "Command Prompt" ou "Git Bash" como padrão.

7. O ambiente selecionado aparece no lado direito da barra de status do VS Code e percebe o indicador ('.venv': venv) que informa que você está usando um ambiente virtual.

8. Atualize o pip:
```bash
py -m pip install --upgrade pip
```

9. Instale o Django no ambiente virtual:
```bash
py -m pip install django
```

**Agora você tem um ambiente independente pronto para escrever código Django.**

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
           'NAME': 'stc',             # nome do banco criado
           'USER': 'django_user',
           'PASSWORD': 'senha123',    # senha definida no Workbench
           'HOST': 'localhost',
           'PORT': '3306',
       }
   }
   ```

---

👉 Pronto! Seu ambiente Django com MySQL está configurado.

---

