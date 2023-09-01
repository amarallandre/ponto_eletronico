import mysql.connector
import tkinter as tk
from tkinter import ttk


# Função para carregar registros de ponto do funcionário selecionado
def carregar_registros():
    selected_name = funcionario_combobox.get()

    # Consulta o ID do funcionário com base no nome selecionado
    cursor.execute("SELECT id FROM funcionarios WHERE nome = %s", (selected_name,))
    funcionario_id = cursor.fetchone()[0]

    # Consulta todos os registros de ponto do funcionário
    cursor.execute(
        "SELECT data, horario_entrada, horario_almoco_saida, horario_almoco_retorno, horario_saida FROM registros WHERE id_funcionario = %s",
        (funcionario_id,))
    registros = cursor.fetchall()

    # Limpa a área de exibição de registros
    registros_text.delete(1.0, tk.END)

    # Exibe os registros na área de texto
    for registro in registros:
        registros_text.insert(tk.END, f"Data: {registro[0]}\n")
        registros_text.insert(tk.END, f"Entrada: {registro[1]}\n")
        registros_text.insert(tk.END, f"Saída para Almoço: {registro[2]}\n")
        registros_text.insert(tk.END, f"Retorno do Almoço: {registro[3]}\n")
        registros_text.insert(tk.END, f"Saída: {registro[4]}\n")
        registros_text.insert(tk.END, "-" * 40 + "\n")


# Conexão com o banco de dados
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456",
    database="ponto_eletronico"
)

cursor = db.cursor()

# Criação da janela principal
root = tk.Tk()
root.title("Registros de Ponto")

# Consulta todos os nomes dos funcionários
cursor.execute("SELECT nome FROM funcionarios")
nomes_funcionarios = [row[0] for row in cursor.fetchall()]

# Combobox para selecionar um funcionário
funcionario_combobox = ttk.Combobox(root, values=nomes_funcionarios)
funcionario_combobox.pack()

# Botão para carregar os registros do funcionário selecionado
carregar_button = tk.Button(root, text="Carregar Registros", command=carregar_registros)
carregar_button.pack()

# Área de texto para exibir os registros
registros_text = tk.Text(root, width=40, height=20)
registros_text.pack()

# Iniciar a interface gráfica
root.mainloop()

# Fechar a conexão com o banco de dados
cursor.close()
db.close()