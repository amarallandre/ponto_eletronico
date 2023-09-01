import mysql.connector
import tkinter as tk
from datetime import datetime, timedelta

# Função para registrar os horários
def registrar_ponto():
    nome = nome_entry.get()

    # Obter o ID do funcionário pelo nome
    cursor.execute("SELECT id FROM funcionarios WHERE nome = %s", (nome,))
    result = cursor.fetchone()

    if result:
        funcionario_id = result[0]
        now = datetime.now()

        data = now.date()
        horario_atual = now.strftime("%H:%M:%S")

        # Verifica se já existe um registro para o funcionário no dia atual
        cursor.execute("SELECT * FROM registros WHERE id_funcionario = %s AND data = %s", (funcionario_id, data))
        existing_record = cursor.fetchone()

        if existing_record:
            horario_almoco_saida = existing_record[4]
            horario_almoco_retorno = existing_record[5]
            horario_saida = existing_record[6]

            if horario_almoco_saida is None:
                cursor.execute("UPDATE registros SET horario_almoco_saida = %s WHERE id_funcionario = %s AND data = %s",
                               (now.strftime("%Y-%m-%d %H:%M:%S"), funcionario_id, data))
            elif horario_almoco_retorno is None:
                cursor.execute(
                    "UPDATE registros SET horario_almoco_retorno = %s WHERE id_funcionario = %s AND data = %s",
                    (now.strftime("%Y-%m-%d %H:%M:%S"), funcionario_id, data))
            elif horario_saida is None:
                cursor.execute("UPDATE registros SET horario_saida = %s WHERE id_funcionario = %s AND data = %s",
                               (now.strftime("%Y-%m-%d %H:%M:%S"), funcionario_id, data))
            else:
                # Caso todos os horários já estejam registrados, crie um novo registro para o próximo dia
                data = data + timedelta(days=1)  # Avança para o próximo dia
                sql = "INSERT INTO registros (id_funcionario, data, horario_entrada, horario_almoco_saida, horario_almoco_retorno, horario_saida) VALUES (%s, %s, %s, %s, %s, %s)"
                val = (funcionario_id, data, now.strftime("%Y-%m-%d %H:%M:%S"), None, None, None)
                cursor.execute(sql, val)
        else:
            # Cria um novo registro para o dia atual
            sql = "INSERT INTO registros (id_funcionario, data, horario_entrada, horario_almoco_saida, horario_almoco_retorno, horario_saida) VALUES (%s, %s, %s, %s, %s, %s)"
            val = (funcionario_id, data, now.strftime("%Y-%m-%d %H:%M:%S"), None, None, None)
            cursor.execute(sql, val)

        db.commit()  # Confirma a transação no banco de dados
        cursor.close()  # Fecha o cursor
        resultado_label.config(text="Ponto registrado com sucesso!")
    else:
        resultado_label.config(text="Funcionário não encontrado!")

# Função para abrir a janela de criação de funcionário
def abrir_janela_criar_funcionario():
    janela_criar_funcionario = tk.Toplevel(root)
    janela_criar_funcionario.title("Criar Funcionário")

    novo_nome_label = tk.Label(janela_criar_funcionario, text="Nome:")
    novo_nome_label.pack()

    novo_nome_entry = tk.Entry(janela_criar_funcionario)
    novo_nome_entry.pack()

    novo_criar_button = tk.Button(janela_criar_funcionario, text="Criar Funcionário",
                                  command=lambda: criar_funcionario(janela_criar_funcionario, novo_nome_entry.get()))
    novo_criar_button.pack()

# Função para criar um novo funcionário
def criar_funcionario(janela, nome):
    sql = "INSERT INTO funcionarios (nome) VALUES (%s)"
    val = (nome,)

    cursor.execute(sql, val)
    db.commit()

    novo_resultado_label = tk.Label(janela, text="Funcionário criado com sucesso!")
    novo_resultado_label.pack()

# Conectando ao banco de dados
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456",
    database="ponto_eletronico"
)

cursor = db.cursor(buffered=True)

# Criar uma janela principal
root = tk.Tk()
root.title("Sistema de Ponto Eletrônico")

# Adicionar widgets para registrar o ponto
nome_label = tk.Label(root, text="Nome:")
nome_label.pack()

nome_entry = tk.Entry(root)
nome_entry.pack()

registrar_button = tk.Button(root, text="Registrar Ponto", command=registrar_ponto)
registrar_button.pack()

resultado_label = tk.Label(root, text="")
resultado_label.pack()

# Adicionar botão para abrir janela de criação de funcionário
abrir_janela_button = tk.Button(root, text="Abrir Janela de Criação de Funcionário",
                                command=abrir_janela_criar_funcionario)
abrir_janela_button.pack()

# Iniciar o loop da interface
root.mainloop()

# Fechar a conexão com o banco de dados
cursor.close()
db.close()