import requests
import random
import string
import tkinter as tk

def gerar_id_aleatorio(tamanho):
    caracteres = string.ascii_letters + string.digits  # letras maiúsculas, minúsculas e números
    id_aleatorio = ''.join(random.choice(caracteres) for _ in range(tamanho))
    return id_aleatorio


# ========================
# 
# = = = = Requests = = = =
# 
# ========================

def make_request(raw_dict: dict):
    # URL para onde você deseja enviar a requisição POST
    url = 'MEU_ENDPOINT_API'

    # Dados que você deseja enviar no corpo da requisição
    dados = {
        "dfifa_id": gerar_id_aleatorio(10),
        "meu_placar": raw_dict['gols_favor'],
        "dele_placar": raw_dict['gols_contra'],
        "moedas": raw_dict['moedas'],
        "competição": raw_dict['competicao']
    }

    # Enviar a requisição POST
    response = requests.post(url, data=dados)
    print(response.text)

    # Verificar a resposta
    if response.status_code == 200:
        print(f'Requisição bem-sucedida! Resposta: {response.text}')
    else:
        print(f'Erro na requisição. Código de status: {response.status_code}' )


# =======================
# 
# = = = = TKinter = = = =
# 
# =======================

def identificar_valores():
    gols_favor = entry_valor1.get()
    gols_contra = entry_valor2.get()
    moedas = entry_valor3.get()
    competicao = entry_texto.get()

    response = {
        "gols_favor": gols_favor,
        "gols_contra": gols_contra,
        "moedas": moedas,
        "competicao": competicao
    }

    make_requests = make_request(response)
    
    resultado_label.config(text=f"Gols Favor: {gols_favor}, Gols Contra: {gols_contra}, Moedas: {moedas}, Competição: {competicao}")

    return make_requests

# Cria a janela principal
janela = tk.Tk()
janela.title("Resultado da Partida")

# Defina a largura e altura da janela
largura_janela = 400
altura_janela = 300
janela.geometry(f"{largura_janela}x{altura_janela}")

# Labels para cada entrada
label_valor1 = tk.Label(janela, text="Meu Placar:")
label_valor1.pack()
entry_valor1 = tk.Entry(janela)
entry_valor1.pack()

label_valor2 = tk.Label(janela, text="Placar dele:")
label_valor2.pack()
entry_valor2 = tk.Entry(janela)
entry_valor2.pack()

label_valor3 = tk.Label(janela, text="Moedas:")
label_valor3.pack()
entry_valor3 = tk.Entry(janela)
entry_valor3.pack()

label_texto = tk.Label(janela, text="Competição:")
label_texto.pack()
entry_texto = tk.Entry(janela)
entry_texto.pack()

# Botão para identificar os valores
identificar_button = tk.Button(janela, text="Enviar Resultado", command=identificar_valores)
identificar_button.pack()

# Label para exibir o resultado
resultado_label = tk.Label(janela, text="")
resultado_label.pack()

janela.mainloop()