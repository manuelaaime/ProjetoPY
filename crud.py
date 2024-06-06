import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import sqlite3

# Conectar ao banco de dados (ou criar um novo)
conn = sqlite3.connect("tepp_db.sqlite3")
cursor = conn.cursor()

# Criar tabela para eventos e matérias
cursor.execute("""
    CREATE TABLE IF NOT EXISTS eventos_materias (
        id INTEGER PRIMARY KEY,
        nome TEXT,
        data DATE,
        descricao TEXT
    )
""")

# Configurar estilo
style = ttk.Style()
style.theme_use('clam')  # Tema Clam, que é mais moderno
style.configure("TButton", font=('Helvetica', 12), padding=10)
style.configure("TEntry", font=('Helvetica', 12), padding=10)
style.configure("TLabel", font=('Helvetica', 12), background='light grey', padding=10)

root = tk.Tk()
root.title("TEPP e Introdução à Lógica")
root.configure(background='light grey')

# Função para adicionar evento
def adicionar_evento():
    nome = entry_nome.get()
    data = entry_data.get()
    descricao = entry_descricao.get()
    cursor.execute("""
        INSERT INTO eventos_materias (nome, data, descricao)
        VALUES (?, ?, ?)
    """, (nome, data, descricao))
    conn.commit()
    messagebox.showinfo("Sucesso", "Evento adicionado com sucesso!")
    limpar_entradas()
    listar_eventos()  # Atualiza a lista de eventos após adicionar um novo

def listar_eventos():
    for widget in frame_lista.winfo_children():
        widget.destroy()
    cursor.execute("SELECT id, nome, data, descricao FROM eventos_materias")
    records = cursor.fetchall()
    for record in records:
        tk.Label(frame_lista, text=f"ID: {record[0]}, Nome: {record[1]}, Data: {record[2]}, Descrição: {record[3]}",
                 font=('Helvetica', 12), background='light grey').pack(anchor='w')

def deletar_evento():
    id_evento = simpledialog.askstring("Deletar Evento", "Digite o ID do evento para deletar:")
    if id_evento:
        cursor.execute("DELETE FROM eventos_materias WHERE id = ?", (id_evento,))
        conn.commit()
        messagebox.showinfo("Sucesso", "Evento deletado com sucesso!")
        listar_eventos()  # Atualiza a lista de eventos após deletar

def alterar_evento():
    id_evento = simpledialog.askstring("Atualizar Evento", "Digite o ID do evento para atualizar:")
    if id_evento:
        nome = simpledialog.askstring("Atualizar Evento", "Novo Nome:")
        data = simpledialog.askstring("Atualizar Evento", "Nova Data:")
        descricao = simpledialog.askstring("Atualizar Evento", "Nova Descrição:")
        cursor.execute("""
            UPDATE eventos_materias
            SET nome = ?, data = ?, descricao = ?
            WHERE id = ?
        """, (nome, data, descricao, id_evento))
        conn.commit()
        messagebox.showinfo("Sucesso", "Evento atualizado com sucesso!")
        listar_eventos()  # Atualiza a lista de eventos após editar

def limpar_entradas():
    entry_nome.delete(0, tk.END)
    entry_data.delete(0, tk.END)
    entry_descricao.delete(0, tk.END)

# Layout usando frames
frame_form = ttk.Frame(root, padding="10 10 10 10")
frame_form.pack(fill=tk.BOTH, expand=True)

frame_buttons = ttk.Frame(root, padding="10 10 10 10")
frame_buttons.pack(fill=tk.BOTH, expand=True)

frame_lista = ttk.Frame(root, padding="10 10 10 10")
frame_lista.pack(fill=tk.BOTH, expand=True)

# Widgets para adicionar evento
label_nome = ttk.Label(frame_form, text="Nome do Evento:")
entry_nome = ttk.Entry(frame_form, width=30)
label_data = ttk.Label(frame_form, text="Data (AAAA-MM-DD):")
entry_data = ttk.Entry(frame_form, width=30)
label_descricao = ttk.Label(frame_form, text="Descrição:")
entry_descricao = ttk.Entry(frame_form, width=30)
btn_adicionar = ttk.Button(frame_buttons, text="Adicionar Evento", command=adicionar_evento)

btn_listar = ttk.Button(frame_buttons, text="Listar Eventos", command=listar_eventos)
btn_deletar = ttk.Button(frame_buttons, text="Deletar Evento", command=deletar_evento)
btn_editar = ttk.Button(frame_buttons, text="Editar Evento", command=alterar_evento)

# Organizando usando grid
label_nome.grid(row=0, column=0, sticky=tk.W)
entry_nome.grid(row=0, column=1, sticky=tk.E)
label_data.grid(row=1, column=0, sticky=tk.W)
entry_data.grid(row=1, column=1, sticky=tk.E)
label_descricao.grid(row=2, column=0, sticky=tk.W)
entry_descricao.grid(row=2, column=1, sticky=tk.E)
btn_adicionar.grid(row=0, column=2, padx=10)

# Organização dos botões de listagem, exclusão e edição
btn_listar.grid(row=0, column=3, padx=10)
btn_deletar.grid(row=0, column=4, padx=10)
btn_editar.grid(row=0, column=5, padx=10)

root.mainloop()

# Fechar conexão ao fechar o aplicativo
conn.close()
