# Sistema_de_Cadastro_de_Usuarios

## 💻 Equipe de desenvolvedores:
* **Edson Severino**
* **Evencio Neto**
* **José Paulo**

## 💾 Sistema CRUD de Cadastro de Usuários (Python/SQLite/Tkinter)

Este projeto implementa um sistema completo de **Cadastro de Usuários** utilizando a linguagem **Python**, o banco de dados **SQLite** para persistência de dados e a biblioteca **Tkinter** para fornecer uma **Interface Gráfica do Usuário (GUI)** interativa.

A principal característica de segurança deste sistema é a implementação de **criptografia de senha** utilizando o algoritmo **Bcrypt** antes do armazenamento no banco de dados.

---

### ✨ Funcionalidades Principais (CRUD)

O sistema suporta todas as operações essenciais para a gestão de usuários:

| Operação | Descrição | Sigla |
| :--- | :--- | :--- |
| **Cadastrar Usuário** | Insere um novo registro com nome, e-mail e **senha criptografada**. | **C**reate |
| **Listar Usuários** | Exibe todos os usuários cadastrados em uma tabela (Treeview). | **R**ead |
| **Editar Usuário** | Permite alterar o nome, e-mail e, opcionalmente, a senha de um registro existente. | **U**pdate |
| **Excluir Usuário** | Remove um usuário permanentemente do banco de dados por ID. | **D**elete |

---

### 💻 Tecnologias Utilizadas

| Componente | Tecnologia | Propósito |
| :--- | :--- | :--- |
| **Linguagem Principal** | Python 3.x | Lógica do Backend e controle do sistema. |
| **Banco de Dados** | SQLite3 | Armazenamento de dados leve e em arquivo único (`usuarios.db`). |
| **Interface Gráfica** | Tkinter | Criação da GUI para interação visual com o sistema. |
| **Criptografia** | Bcrypt | Geração segura de hash de senhas (incluindo salt). |

---

### ⚙️ Requisitos e Como Rodar

Para executar este sistema em sua máquina, siga os passos abaixo:

#### 1. Requisitos de Sistema

* **Python 3.x** instalado.

#### 2. Instalação de Dependências

O projeto utiliza a biblioteca `bcrypt` para a criptografia. Instale-a via `pip`:

```bash
pip install bcrypt
```
### 3. Execução

1.  Salve o código-fonte em um arquivo chamado `gui_cadastro.py`.
2.  Execute o script no terminal:

```bash
python gui_cadastro.py
```

### 🗄️ Estrutura do Banco de Dados

O banco de dados **SQLite** (`usuarios.db`) contém uma única tabela chamada `usuarios` com a seguinte estrutura: 

| Nome do Campo | Tipo de Dado | Restrições | Detalhes |
| :--- | :--- | :--- | :--- |
| **id** | `INTEGER` | `PRIMARY KEY`, `AUTOINCREMENT` | Identificador único. |
| **nome** | `TEXT` | `NOT NULL` | Nome completo do usuário. |
| **email** | `TEXT` | `UNIQUE`, `NOT NULL` | E-mail do usuário (não pode haver duplicatas). |
| **senha** | `TEXT` | `NOT NULL` | **Hash da senha** gerado pelo Bcrypt (nunca a senha em texto puro). |

**Nota de Segurança:** A coluna **`senha`** armazena o hash criptografado da senha. Em nenhum momento a senha original em texto puro é salva no banco de dados.

...
