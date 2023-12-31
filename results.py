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

def postar_resultado(raw_dict: dict):
    # URL para onde você deseja enviar a requisição POST
    url = os.getenv('results_api')

    # Dados que você deseja enviar no corpo da requisição
    dados = {
        "dfifa_id": str(uuid.uuid4()),
        "meu_placar": raw_dict['gols_favor'],
        "dele_placar": raw_dict['gols_contra'],
        "moedas": raw_dict['moedas'],
        "competição": raw_dict['competicao'],
        "penaltis": raw_dict['penaltis'],
        "semana": raw_dict['semana']
    }

    # Enviar a requisição POST
    response = requests.post(url, json=dados)

    # Verificar a resposta
    if response.status_code == 200:
        print(f'Requisição bem-sucedida! Resposta: {response.text}')
    else:
        print(f'Erro na requisição. Código de status: {response.status_code}' )

# Função para fazer a requisição GET com parâmetros "comeco" e "fim"
def obter_resumo_do_dia(data):
    # URL para fazer a requisição GET com os parâmetros
    url = os.getenv('results_api')  # Substitua pela URL correta
    parametros = {'data': data}

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
                                  f"Quits: {resumo_dia['Resultados do dia']['Quits']}\n"
                                  f"Gols Marcados: {resumo_dia['Resultados do dia']['Gols Marcados']}\n"
                                  f"Gols Sofridos: {resumo_dia['Resultados do dia']['Gols Sofridos']}\n"
                                  f"Saldo: {resumo_dia['Resultados do dia']['Saldo']}\n")
    else:
        resumo_label.config(text="Erro na requisição. Código de status: " + str(response.status_code))

def obter_resumo_por_competicao(competicao):
    # Substitua 'URL_DA_API' pela URL correta para obter o resumo por competição.
    url_competicao = os.getenv('competitions_api')
    
    # Parâmetros para a requisição (se necessário)
    parametros = {'competicao': competicao}
    
    response = requests.get(url_competicao, json=parametros)
    
    if response.status_code == 200:
        # Parse da resposta JSON
        resumo_competicao = json.loads(response.text)['message']
        resumo_competicao_label.config(text="Resultados por competição:\n"
                                          f"Vitórias: {resumo_competicao['Vitorias']}\n"
                                          f"Empates: {resumo_competicao['Empates']}\n"
                                          f"Derrotas: {resumo_competicao['Derrotas']}\n"
                                          f"Total arrecadado: {resumo_competicao['Total arrecadado']}\n"
                                          f"Quits: {resumo_competicao['Quits']}\n"
                                          f"Gols marcados: {resumo_competicao['Gols Marcados']}\n"
                                          f"Gols sofridos: {resumo_competicao['Gols Sofridos']}\n"
                                          f"Saldo: {resumo_competicao['Saldo']}\n")
    else:
        resumo_competicao_label.config(text=f"Erro na requisição. Código de status: {response.status_code}")

def obter_resumo_por_semana(semana):
    # Substitua 'URL_DA_API' pela URL correta para obter o resumo por semana.
    url_competicao = os.getenv('week_api')
    
    # Parâmetros para a requisição (se necessário)
    parametros = {'semana': int(semana)}
    
    response = requests.get(url_competicao, json=parametros)
    
    if response.status_code == 200:
        # Parse da resposta JSON
        resumo_semana = json.loads(response.text)['message']
        resumo_semana_label.config(text="Resultados por competição:\n"
                                          f"Vitórias: {resumo_semana['Vitorias']}\n"
                                          f"Empates: {resumo_semana['Empates']}\n"
                                          f"Derrotas: {resumo_semana['Derrotas']}\n"
                                          f"Total arrecadado: {resumo_semana['Total arrecadado']}\n"
                                          f"Quits: {resumo_semana['Quits']}\n"
                                          f"Gols marcados: {resumo_semana['Gols Marcados']}\n"
                                          f"Gols sofridos: {resumo_semana['Gols Sofridos']}\n"
                                          f"Saldo: {resumo_semana['Saldo']}\n")
    else:
        resumo_semana_label.config(text=f"Erro na requisição. Código de status: {response.status_code}")

# =======================
# 
# = = = = TKinter = = = =
# 
# =======================

# =========================
# 
# = = Formatação Janela = =
# 
# =========================

# Cria a janela principal
janela = tk.Tk()
janela.title("Daily FIFA")

# Defina a largura e altura da janela
largura_janela = 800
altura_janela = 800
janela.geometry(f"{largura_janela}x{altura_janela}")

# Cria um frame para a seção "Resultado" e agrupa os elementos nesse frame
frame_resultado = tk.Frame(janela)
frame_resultado.pack(side="left", padx=50, pady=10, anchor="w")

# Cria um frame para agrupar todos os elementos
frame = tk.Frame(janela)
frame.pack(side="right", padx=50, pady=10, anchor="e")

# =======================
# 
# = = = = Funções = = = =
# 
# =======================

# Título para a seção "Resultado"
titulo_resultado = tk.Label(frame_resultado, text="Resultado")
titulo_resultado.pack()

# Labels para cada entrada da seção "Resultado"
meu_placar_label = tk.Label(frame_resultado, text="Meu Placar:")
meu_placar_label.pack()
entry_meu_placar = tk.Entry(frame_resultado)
entry_meu_placar.pack()

placar_dele_label = tk.Label(frame_resultado, text="Placar dele:")
placar_dele_label.pack()
entry_placar_dele = tk.Entry(frame_resultado)
entry_placar_dele.pack()

label_moedas = tk.Label(frame_resultado, text="Moedas:")
label_moedas.pack()
entry_moedas = tk.Entry(frame_resultado)
entry_moedas.pack()

label_competicao = tk.Label(frame_resultado, text="Competição:")
label_competicao.pack()
entry_competicao = tk.Entry(frame_resultado)
entry_competicao.pack()

label_penalti = tk.Label(frame_resultado, text="Penaltis:")
label_penalti.pack()
entry_penalti = tk.Entry(frame_resultado)
entry_penalti.pack()

label_week = tk.Label(frame_resultado, text="Semana:")
label_week.pack()
entry_week = tk.Entry(frame_resultado)
entry_week.pack()

def identificar_valores():
    gols_favor = entry_meu_placar.get()
    gols_contra = entry_placar_dele.get()
    moedas = entry_moedas.get()
    competicao = entry_competicao.get()
    penaltis = entry_penalti.get()
    semana = entry_week.get()

    if competicao not in ['Rivals', 'WL', 'KWL']:
        resultado_label.config(text=f'Competicao informada está incorreta!')
        return

    if int(gols_favor) < 0 or int(gols_contra) < 0:
        resultado_label.config(text=f'Não existe placar negativo!')
        return

    if penaltis not in ['-', 'd', 'v']:
        resultado_label.config(text=f'Valor para penaltis informado está incorreto!')
        return

    response = {
        "gols_favor": gols_favor,
        "gols_contra": gols_contra,
        "moedas": moedas,
        "competicao": competicao,
        "penaltis": penaltis,
        "semana": semana
    }

    postar_resultados = postar_resultado(response)

    resultado_label.config(
        text=f"Gols Favor: {gols_favor}, Gols Contra: {gols_contra}, Moedas: {moedas},\n Competição: {competicao}, Penaltis: {penaltis}, Semana {semana}")

    return postar_resultados

# Botão para enviar o resultado
enviar_resultado = tk.Button(frame_resultado, text="Enviar resultado", command=identificar_valores)
enviar_resultado.pack()

resultado_label = tk.Label(frame_resultado, text="")
resultado_label.pack()

# ==========================
# 
# = = = Resumo por Dia = = = 
# 
# ==========================

# Título para a seção "Resumo"
titulo_resumo = tk.Label(frame, text="Resumo")
titulo_resumo.pack()

# Labels e campos de entrada para a seção "Resumo"
label_data = tk.Label(frame, text="Data:")
label_data.pack()
entry_data = tk.Entry(frame)
entry_data.pack()

# Botão para obter o resumo do dia com parâmetros
def obter_resumo_com_parametros():
    data = entry_data.get()
    obter_resumo_do_dia(str(data))

# Botão para obter o resumo com parâmetros
resumo_com_parametros_button = tk.Button(frame, text="Resumo do Dia", command=obter_resumo_com_parametros)
resumo_com_parametros_button.pack()

# Label para exibir o resultado
resumo_label = tk.Label(frame, text="")
resumo_label.pack()

# =========================
# 
# = Resumo por Competição = 
# 
# =========================

# Nova label para verificar resumo por competição
label_competicao2 = tk.Label(frame, text="Competição:")
label_competicao2.pack()
entry_competicao2 = tk.Entry(frame)
entry_competicao2.pack()

# Label para exibir o resumo por competição
resumo_competicao_label = tk.Label(frame, text="")
resumo_competicao_label.pack()

# Botão para obter o resumo por competição
def obter_resumo_com_competicao():
    competicao2 = entry_competicao2.get()
    obter_resumo_por_competicao(competicao2)

# Botão para obter o resumo por competição
resumo_competicao_button = tk.Button(frame, text="Resumo por Competição", command=obter_resumo_com_competicao)
resumo_competicao_button.pack()

# =========================
# 
# = = Resumo por Semana = =
# 
# =========================

# Nova label para verificar resumo por semana
label_semana = tk.Label(frame, text="Semana:")
label_semana.pack()
entry_semana = tk.Entry(frame)
entry_semana.pack()

# Botão para obter o resumo por semana
def obter_resumo_com_semana():
    semana = entry_semana.get()
    obter_resumo_por_semana(semana)

# Botão para obter o resumo por semana
resumo_semana_button = tk.Button(frame, text="Resumo por Semana", command=obter_resumo_com_semana)
resumo_semana_button.pack()

# Label para exibir o resumo por semana
resumo_semana_label = tk.Label(frame, text="")
resumo_semana_label.pack()

janela.mainloop()