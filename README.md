# 📘 Projeto Django

## 🔧 Requisitos

### Ambiente

* **Python**: 3.13.5
* **Django**: 5.2.6
* **MySQL**: 8.0.43
* **MySQL Workbench**: 8.0 CE

### Dependências

* `django`
* `wheel` *(caso ocorra erro de comunicação com o MySQL no Windows)*
* `mysqlclient`
* `bcrypt`

---

## 🚀 Passos para rodar

1. **Clonar o projeto**
   Clone o repositório do GitHub (recomendado clonar dentro de um *project environment*).

   ```bash
   git clone https://github.com/Darlan-Jose/Repositorio-teste.git
   cd Repositorio-teste
   ```

2. **Criar o banco de dados**
   Crie um banco de dados MySQL, preferencialmente com o nome `stc`.

   > ⚠️ Caso utilize outro nome, será necessário alterar a configuração de `DATABASES` no arquivo `settings.py`.

3. **Criar o usuário no MySQL**
   Veja o tutorial completo na seção [Criando um usuário no MySQL Workbench (Windows)](https://github.com/Darlan-Jose/Trabalho-Programacao-Internet/blob/main/README.md#%EF%B8%8F-criando-um-usu%C3%A1rio-no-mysql-workbench-windows)
4. **Rodar as migrações**
   No ambiente virtual do projeto, execute:

   ```bash
   py manage.py migrate
   py manage.py createcachetable
   ```

   Em seguida, execute o DDL no MySQL: https://github.com/Darlan-Jose/Repositorio-teste/blob/main/data/DDL.sql.

5. **Iniciar o servidor**

   ```bash
   py manage.py runserver
   ```

6. **Acessar no navegador**
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

