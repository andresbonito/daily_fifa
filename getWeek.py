import json
import boto3

dynamodb = boto3.client('dynamodb')
fifa_table = 'Daily_FIFA'

def lambda_handler(event, context):
    print(f'Evento: {event}')
    
    semana = f"{event['semana']}"
    
    response = scan_competition(semana)
    
    new_response = clean_data(response)
    
    response = send_results(new_response)
    
    return {
            'statusCode': 200,
            'message': response
        }


def scan_competition(semana):
    expressao_filtro = "#semana = :semana"
    
    valores = {
        ':semana': {'S': f'semana#{semana}'}
    }
    nomes_atributo = {
        '#semana': 'semana'
    }
    
    resultado = dynamodb.scan(
        TableName=fifa_table,
        FilterExpression=expressao_filtro,
        ExpressionAttributeValues=valores,
        ExpressionAttributeNames=nomes_atributo
    )

    items = resultado['Items']
    
    return items
    
def deep_clean_field(raw_dict: dict):
    response = {}

    for key, value in raw_dict.items():
        if key in ['S', 'N', 'B', 'L', 'NS', 'SS', 'BS', 'BOOL', ]:
            return value
        if key in ['NULL', ]:
            return None
        elif key in ['M', ]:
            return deep_clean_field(value)
        else:
            response.update({key: deep_clean_field(value)})

    return response
    
def clean_data(raw_list: list):
    new_raw_list = []
    
    for raw in raw_list:
        response = deep_clean_field(raw)
        new_raw_list.append(response)
        
    return new_raw_list

def send_results(raw_list: list):
    vitorias = 0
    empates = 0
    derrotas = 0
    total_moedas = 0
    quits = 0
    gols_a_favor = 0
    gols_a_contra = 0
    
    for item in raw_list:
        gols_favor = int(item['gols_favor'])
        gols_contra = int(item['gols_contra'])
        moedas = int(item['moedas'])
        penaltis = item['penaltis']
        
        if gols_favor > gols_contra:
            vitorias += 1
        elif gols_favor < gols_contra:
            derrotas += 1
        elif gols_favor == gols_contra and penaltis == '-':
            empates += 1
            
        if moedas == 0:
            quits += 1
            
        if penaltis == 'd':
            derrotas += 1
        elif penaltis == 'v':
            vitorias += 1
        
        total_moedas += moedas
        gols_a_favor += gols_favor
        gols_a_contra += gols_contra
        saldo = gols_a_favor - gols_a_contra
        
    resp = {
        "Vitorias": vitorias,
        "Empates": empates,
        "Derrotas": derrotas,
        "Total arrecadado": total_moedas,
        "Quits": quits,
        "Gols Marcados": gols_a_favor,
        "Gols Sofridos": gols_a_contra,
        "Saldo": saldo
    }
    
    return resp