import sqlite3
import bcrypt
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# --- 1. Configuração do Banco de Dados e Hash ---

DATABASE_NAME = 'usuarios.db'

def connect_db():
    """Cria uma conexão com o banco de dados SQLite."""
    return sqlite3.connect(DATABASE_NAME)

def initialize_db():
    """Cria a tabela 'usuarios' se ela não existir."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def hash_password(password):
    """Gera o hash da senha usando bcrypt."""
    salt = bcrypt.gensalt()
    hashed_bytes = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_bytes.decode('utf-8')

# --- 2. Funções CRUD (Integradas à GUI) ---

def cadastrar_usuario(nome, email, senha):
    """Cadastra um novo usuário com senha criptografada."""
    if not nome or not email or not senha:
        messagebox.showerror("Erro de Cadastro", "Todos os campos (Nome, Email, Senha) são obrigatórios.")
        return False

    hashed_pwd = hash_password(senha)
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)",
            (nome, email, hashed_pwd)
        )
        conn.commit()
        messagebox.showinfo("Sucesso", f"Usuário '{nome}' cadastrado com sucesso!")
        return True
    except sqlite3.IntegrityError:
        messagebox.showerror("Erro de Cadastro", f"O email '{email}' já está em uso.")
        return False
    except Exception as e:
        messagebox.showerror("Erro de Cadastro", f"Erro inesperado: {e}")
        return False
    finally:
        conn.close()

def listar_usuarios():
    """Retorna todos os usuários (id, nome, email)."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, email , senha FROM usuarios")
    usuarios = cursor.fetchall()
    conn.close()
    return usuarios

def editar_usuario(user_id, novo_nome, novo_email, nova_senha=None):
    """Edita nome, email e, opcionalmente, a senha de um usuário."""
    conn = connect_db()
    cursor = conn.cursor()
    
    try:
        if nova_senha:
            hashed_pwd = hash_password(nova_senha)
            cursor.execute(
                "UPDATE usuarios SET nome = ?, email = ?, senha = ? WHERE id = ?",
                (novo_nome, novo_email, hashed_pwd, user_id)
            )
        else:
            cursor.execute(
                "UPDATE usuarios SET nome = ?, email = ? WHERE id = ?",
                (novo_nome, novo_email, user_id)
            )
            
        if cursor.rowcount == 0:
            messagebox.showwarning("Alerta", f"Nenhum usuário encontrado com ID {user_id}.")
            return False
        
        conn.commit()
        messagebox.showinfo("Sucesso", f"Usuário ID {user_id} editado com sucesso.")
        return True
    except sqlite3.IntegrityError:
        messagebox.showerror("Erro de Edição", f"O novo email '{novo_email}' já está em uso.")
        return False
    except Exception as e:
        messagebox.showerror("Erro de Edição", f"Erro ao editar: {e}")
        return False
    finally:
        conn.close()

def excluir_usuario(user_id):
    """Exclui um usuário pelo ID."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id = ?", (user_id,))
    
    if cursor.rowcount > 0:
        conn.commit()
        messagebox.showinfo("Sucesso", f"Usuário ID {user_id} excluído com sucesso.")
        return True
    else:
        messagebox.showwarning("Alerta", f"Nenhum usuário encontrado com ID {user_id}.")
        return False
   # finally:
        conn.close()

# --- 3. Classe da Aplicação Tkinter ---

class UserManagementApp:
    def __init__(self, root):
        self.root = root
        root.title("Sistema CRUD de Usuários")
        root.geometry("800x500") # Tamanho da janela principal
        
        # Inicializa o banco de dados
        initialize_db()
        
        # --- Configuração dos Frames ---
        self.frame_cadastro = ttk.LabelFrame(root, text="Cadastro de Novo Usuário")
        self.frame_cadastro.pack(padx=10, pady=10, fill="x")
        
        self.frame_lista = ttk.LabelFrame(root, text="Lista de Usuários (ID, Nome, Email, senha)")
        self.frame_lista.pack(padx=10, pady=10, fill="both", expand=True)

        # --- Elementos do Cadastro ---
        self.create_cadastro_widgets()
        
        # --- Elementos da Lista (Treeview) ---
        self.create_list_widgets()
        
        # Carrega os dados iniciais
        self.refresh_list()

    def create_cadastro_widgets(self):
        """Cria os campos de entrada e o botão de cadastro."""
        
        # Nome
        ttk.Label(self.frame_cadastro, text="Nome:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_nome = ttk.Entry(self.frame_cadastro, width=30)
        self.entry_nome.grid(row=0, column=1, padx=5, pady=5)
        
        # Email
        ttk.Label(self.frame_cadastro, text="Email:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_email = ttk.Entry(self.frame_cadastro, width=30)
        self.entry_email.grid(row=1, column=1, padx=5, pady=5)
        
        # Senha
        ttk.Label(self.frame_cadastro, text="Senha:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.entry_senha = ttk.Entry(self.frame_cadastro, show="*", width=30) # show="*" oculta a senha
        self.entry_senha.grid(row=2, column=1, padx=5, pady=5)
        
        # Botão de Cadastro
        ttk.Button(self.frame_cadastro, text="Cadastrar", command=self.handle_cadastro).grid(row=3, column=0, columnspan=2, pady=10)

    def create_list_widgets(self):
        """Cria o Treeview para exibir a lista e os botões de ação."""
        
        # Configuração do Treeview (Tabela)
        self.tree = ttk.Treeview(self.frame_lista, columns=("ID", "Nome", "Email", "Senha"), show="headings")
        self.tree.heading("ID", text="ID", anchor="center")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Senha", text="Senha")
        
        self.tree.column("ID", width=50, stretch=tk.NO)
        self.tree.column("Nome", width=200)
        self.tree.column("Email", width=300)
        self.tree.column("Senha", width=200)
        
        self.tree.pack(side="top", fill="both", expand=True)

        # Barra de Rolagem
        scrollbar = ttk.Scrollbar(self.frame_lista, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        
        # Frame para Botões de Ação
        frame_botoes = ttk.Frame(self.frame_lista)
        frame_botoes.pack(pady=10)

        ttk.Button(frame_botoes, text="Atualizar Lista", command=self.refresh_list).pack(side="left", padx=5)
        ttk.Button(frame_botoes, text="Editar Selecionado", command=self.open_edit_window).pack(side="left", padx=5)
        ttk.Button(frame_botoes, text="Excluir Selecionado", command=self.handle_exclusao).pack(side="left", padx=5)

    def refresh_list(self):
        """Limpa e preenche o Treeview com os dados atuais do banco."""
        # Limpa todos os itens existentes
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Insere os novos dados
        usuarios = listar_usuarios()
        for user in usuarios:
            self.tree.insert("", "end", values=user)
            
    # --- 4. Handlers de Ação ---

    def handle_cadastro(self):
        """Ação do botão 'Cadastrar'."""
        nome = self.entry_nome.get()
        email = self.entry_email.get()
        senha = self.entry_senha.get()
        
        if cadastrar_usuario(nome, email, senha):
            # Limpa os campos após o sucesso
            self.entry_nome.delete(0, tk.END)
            self.entry_email.delete(0, tk.END)
            self.entry_senha.delete(0, tk.END)
            self.refresh_list()

    def handle_exclusao(self):
        """Ação do botão 'Excluir Selecionado'."""
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showwarning("Seleção", "Selecione um usuário na lista para excluir.")
            return

        user_values = self.tree.item(selected_item, 'values')
        user_id = user_values[0]
        user_name = user_values[1]
        
        if messagebox.askyesno("Confirmação", f"Tem certeza que deseja excluir o usuário '{user_name}' (ID: {user_id})?"):
            if excluir_usuario(user_id):
                self.refresh_list()

    # --- 5. Janela de Edição (TopLevel) ---

    def open_edit_window(self):
        """Abre uma nova janela para edição do usuário selecionado."""
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showwarning("Seleção", "Selecione um usuário na lista para editar.")
            return
            
        user_values = self.tree.item(selected_item, 'values')
        user_id, current_name, current_email = user_values[0], user_values[1], user_values[2]
        
        # Cria a nova janela (TopLevel)
        edit_window = tk.Toplevel(self.root)
        edit_window.title(f"Editar Usuário ID: {user_id}")
        edit_window.geometry("350x250")
        
        # Labels e Entradas de Edição
        
        ttk.Label(edit_window, text="ID:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        ttk.Label(edit_window, text=user_id).grid(row=0, column=1, padx=10, pady=5, sticky="w")
        
        ttk.Label(edit_window, text="Novo Nome:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        entry_edit_nome = ttk.Entry(edit_window, width=30)
        entry_edit_nome.insert(0, current_name)
        entry_edit_nome.grid(row=1, column=1, padx=10, pady=5)
        
        ttk.Label(edit_window, text="Novo Email:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        entry_edit_email = ttk.Entry(edit_window, width=30)
        entry_edit_email.insert(0, current_email)
        entry_edit_email.grid(row=2, column=1, padx=10, pady=5)
        
        ttk.Label(edit_window, text="Nova Senha:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        entry_edit_senha = ttk.Entry(edit_window, show="*", width=30)
        entry_edit_senha.grid(row=3, column=1, padx=10, pady=5)
        
        def save_edits():
            """Função de salvar dentro da janela de edição."""
            novo_nome = entry_edit_nome.get().strip()
            novo_email = entry_edit_email.get().strip()
            nova_senha = entry_edit_senha.get().strip() # Pode ser vazio
            
            # Use os valores atuais se os campos estiverem vazios
            final_nome = novo_nome if novo_nome else current_name
            final_email = novo_email if novo_email else current_email
            
            if not final_nome or not final_email:
                 messagebox.showerror("Erro", "Nome e Email não podem ficar vazios.")
                 return

            if editar_usuario(user_id, final_nome, final_email, nova_senha if nova_senha else None):
                edit_window.destroy() # Fecha a janela se a edição for bem-sucedida
                self.refresh_list() # Atualiza a lista principal

        ttk.Button(edit_window, text="Salvar Alterações", command=save_edits).grid(row=4, column=0, columnspan=2, pady=15)


if __name__ == "__main__":
    root = tk.Tk()
    app = UserManagementApp(root)
    root.mainloop()