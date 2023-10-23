import os
import requests
import json
import uuid
import tkinter as tk

# ========================
#
# = = = = Requests = = = =
#
# ========================

def make_request(raw_dict: dict):
    # URL para onde você deseja enviar a requisição POST
    url = os.getenv('results_api')

    # Dados que você deseja enviar no corpo da requisição
    dados = {
        "dfifa_id": str(uuid.uuid4()),
        "meu_placar": raw_dict['gols_favor'],
        "dele_placar": raw_dict['gols_contra'],
        "moedas": raw_dict['moedas'],
        "competição": raw_dict['competicao'],
        "penaltis": raw_dict['penaltis']
    }

    # Enviar a requisição POST
    response = requests.post(url, json=dados)

    # Verificar a resposta
    if response.status_code == 200:
        print(f'Requisição bem-sucedida! Resposta: {response.text}')
    else:
        print(f'Erro na requisição. Código de status: {response.status_code}' )

# Função para fazer a requisição GET com parâmetros "comeco" e "fim"
def obter_resumo_do_dia(comeco, fim):
    # URL para fazer a requisição GET com os parâmetros
    url = os.getenv('results_api')  # Substitua pela URL correta
    parametros = {'comeco': comeco, 'fim': fim}

    # Enviar a requisição GET com os parâmetros
    response = requests.get(url, json=parametros)

    if response.status_code == 200:
        # Parse da resposta JSON
        resumo_dia = json.loads(response.text)
        print(f'Resumo dia: {resumo_dia}')
        
        # Exibir o resumo na interface gráfica
        resumo_label.config(text="Resultados do dia:\n"
                                  f"Vitórias: {resumo_dia['Resultados do dia']['Vitorias']}\n"
                                  f"Empates: {resumo_dia['Resultados do dia']['Empates']}\n"
                                  f"Derrotas: {resumo_dia['Resultados do dia']['Derrotas']}\n"
                                  f"Total arrecadado: {resumo_dia['Resultados do dia']['Total arrecadado']}\n"
                                  f"Quits: {resumo_dia['Resultados do dia']['Quits']}")
    else:
        resumo_label.config(text="Erro na requisição. Código de status: " + str(response.status_code))


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
    penaltis = entry_penalti_texto.get()

    if penaltis not in ['-', 'd', 'v']:
        resultado_label.config(text=f'Valor para penaltis informado está incorreto!')
        return

    response = {
        "gols_favor": gols_favor,
        "gols_contra": gols_contra,
        "moedas": moedas,
        "competicao": competicao,
        "penaltis": penaltis
    }

    make_requests = make_request(response)
    
    resultado_label.config(text=f"Gols Favor: {gols_favor}, Gols Contra: {gols_contra}, Moedas: {moedas}, Competição: {competicao}, Penaltis: {penaltis}")

    return make_requests

# Cria a janela principal
janela = tk.Tk()
janela.title("Resultado da Partida")

# Defina a largura e altura da janela
largura_janela = 800
altura_janela = 600
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

penalti_texto = tk.Label(janela, text="Penaltis:")
penalti_texto.pack()
entry_penalti_texto = tk.Entry(janela)
entry_penalti_texto.pack()

# Botão para identificar os valores
identificar_button = tk.Button(janela, text="Enviar Resultado", command=identificar_valores)
identificar_button.pack()

# Label para exibir o resultado
resultado_label = tk.Label(janela, text="")
resultado_label.pack()

# Botão para obter o resumo do dia com parâmetros
def obter_resumo_com_parametros():
    comeco = entry_comeco.get()
    fim = entry_fim.get()
    obter_resumo_do_dia(comeco, fim)

# Labels e campos de entrada para os parâmetros "comeco" e "fim"
label_comeco = tk.Label(janela, text="Data de Início:")
label_comeco.pack()
entry_comeco = tk.Entry(janela)
entry_comeco.pack()

label_fim = tk.Label(janela, text="Data de Fim:")
label_fim.pack()
entry_fim = tk.Entry(janela)
entry_fim.pack()

# Botão para obter o resumo com parâmetros
resumo_com_parametros_button = tk.Button(janela, text="Resumo do Dia", command=obter_resumo_com_parametros)
resumo_com_parametros_button.pack()

# Label para exibir o resultado
resumo_label = tk.Label(janela, text="")
resumo_label.pack()

janela.mainloop()