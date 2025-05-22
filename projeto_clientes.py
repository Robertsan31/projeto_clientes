import sqlite3
import tkinter as tk
from tkinter import messagebox
from fpdf import FPDF
import re

# Conectar ao banco de dados
conn = sqlite3.connect("cadastro.db")
cursor = conn.cursor()

# Criar tabelas
cursor.execute("""
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    cpf TEXT UNIQUE NOT NULL,
    email TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    preco REAL NOT NULL,
    quantidade INTEGER NOT NULL
)
""")

conn.commit()

# Validações
def validar_cpf(cpf):
    return re.match(r'^\d{11}$', cpf) is not None

def validar_preco(preco):
    return preco > 0

def validar_quantidade(qtd):
    return qtd > 0

# Funções do sistema
def cadastrar_cliente():
    nome = nome_entry.get()
    cpf = cpf_entry.get()
    email = email_entry.get()

    if not validar_cpf(cpf):
        messagebox.showerror("Erro", "CPF inválido! Deve conter 11 números.")
        return
    
    try:
        cursor.execute("INSERT INTO clientes (nome, cpf, email) VALUES (?, ?, ?)", (nome, cpf, email))
        conn.commit()
        messagebox.showinfo("Sucesso", "Cliente cadastrado!")
        limpar_campos()
    except sqlite3.IntegrityError:
        messagebox.showerror("Erro", "CPF já cadastrado!")

def cadastrar_produto():
    nome = produto_nome_entry.get()
    try:
        preco = float(preco_entry.get())
        quantidade = int(quantidade_entry.get())

        if not validar_preco(preco) or not validar_quantidade(quantidade):
            raise ValueError

        cursor.execute("INSERT INTO produtos (nome, preco, quantidade) VALUES (?, ?, ?)", (nome, preco, quantidade))
        conn.commit()
        messagebox.showinfo("Sucesso", "Produto cadastrado!")
        limpar_campos()
    except ValueError:
        messagebox.showerror("Erro", "Preço deve ser positivo e quantidade deve ser um número inteiro.")

def buscar_cliente():
    termo = busca_cliente_entry.get()
    cursor.execute("SELECT * FROM clientes WHERE nome LIKE ? OR cpf LIKE ?", (f"%{termo}%", f"%{termo}%"))
    resultado = cursor.fetchall()

    if resultado:
        mensagem = "\n".join([f"Nome: {c[1]}, CPF: {c[2]}, Email: {c[3]}" for c in resultado])
        messagebox.showinfo("Resultados da Pesquisa", mensagem)
    else:
        messagebox.showinfo("Resultados", "Nenhum cliente encontrado.")

def buscar_produto():
    termo = busca_produto_entry.get()
    cursor.execute("SELECT * FROM produtos WHERE nome LIKE ?", (f"%{termo}%",))
    resultado = cursor.fetchall()

    if resultado:
        mensagem = "\n".join([f"Nome: {p[1]}, Preço: {p[2]}, Quantidade: {p[3]}" for p in resultado])
        messagebox.showinfo("Resultados da Pesquisa", mensagem)
    else:
        messagebox.showinfo("Resultados", "Nenhum produto encontrado.")

def gerar_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "Relatório de Clientes e Produtos", ln=True, align="C")

    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Clientes:", ln=True)

    cursor.execute("SELECT * FROM clientes")
    clientes = cursor.fetchall()
    for c in clientes:
        pdf.cell(0, 10, f"Nome: {c[1]}, CPF: {c[2]}, Email: {c[3]}", ln=True)

    pdf.cell(0, 10, "", ln=True)  
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Produtos:", ln=True)

    cursor.execute("SELECT * FROM produtos")
    produtos = cursor.fetchall()
    for p in produtos:
        pdf.cell(0, 10, f"Nome: {p[1]}, Preço: {p[2]}, Quantidade: {p[3]}", ln=True)

    pdf.output("relatorio.pdf")
    messagebox.showinfo("Sucesso", "Relatório PDF gerado!")

def limpar_campos():
    nome_entry.delete(0, tk.END)
    cpf_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    produto_nome_entry.delete(0, tk.END)
    preco_entry.delete(0, tk.END)
    quantidade_entry.delete(0, tk.END)
    busca_cliente_entry.delete(0, tk.END)
    busca_produto_entry.delete(0, tk.END)

# Criar interface gráfica
root = tk.Tk()
root.title("Sistema Completo")
root.geometry("450x650")

# Seção Cliente
tk.Label(root, text="Nome do Cliente:").pack()
nome_entry = tk.Entry(root)
nome_entry.pack()

tk.Label(root, text="CPF:").pack()
cpf_entry = tk.Entry(root)
cpf_entry.pack()

tk.Label(root, text="E-mail:").pack()
email_entry = tk.Entry(root)
email_entry.pack()

tk.Button(root, text="Cadastrar Cliente", command=cadastrar_cliente).pack()

# Seção Busca Cliente
tk.Label(root, text="Buscar Cliente por Nome ou CPF:").pack()
busca_cliente_entry = tk.Entry(root)
busca_cliente_entry.pack()
tk.Button(root, text="Buscar Cliente", command=buscar_cliente).pack()

# Seção Produto
tk.Label(root, text="Nome do Produto:").pack()
produto_nome_entry = tk.Entry(root)
produto_nome_entry.pack()

tk.Label(root, text="Preço:").pack()
preco_entry = tk.Entry(root)
preco_entry.pack()

tk.Label(root, text="Quantidade:").pack()
quantidade_entry = tk.Entry(root)
quantidade_entry.pack()

tk.Button(root, text="Cadastrar Produto", command=cadastrar_produto).pack()

# Seção Busca Produto
tk.Label(root, text="Buscar Produto por Nome:").pack()
busca_produto_entry = tk.Entry(root)
busca_produto_entry.pack()
tk.Button(root, text="Buscar Produto", command=buscar_produto).pack()

# Botão para Relatórios
tk.Button(root, text="Gerar Relatório PDF", command=gerar_pdf).pack()

# Iniciar interface gráfica
root.mainloop()

# Fechar conexão ao sair
conn.close()
