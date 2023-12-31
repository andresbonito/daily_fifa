import json
import boto3
from datetime import datetime


client = boto3.client('dynamodb')
fifa_table = 'Daily_FIFA'

now_saopaulo = int(datetime.now().timestamp())

def lambda_handler(event, context):
    print(f'Evento: {event}')
    
    id = event['dfifa_id']
    meu_placar = event['meu_placar']
    dele_placar = event['dele_placar']
    competicao = event['competição']
    moedas = event['moedas']
    penaltis = str(event['penaltis'])
    
    if competicao not in ['Rivals', 'WL', 'KWL']:
        return {
            'statusCode': 400,
            'message': 'Esta competicão não existe.'
        }
        
    if meu_placar < 0 or dele_placar < 0:
        return {
            'statusCode': 400,
            'message': 'Não existe placar negativo.'
        }
    
    raw_dict = {
        'dfifa_id': {'S': id},
        'competicao': {'S': competicao},
        'gols_favor': {'N': f'{meu_placar}'},
        'gols_contra': {'N': f'{dele_placar}'},
        'moedas': {'N': f'{moedas}'},
        'day&time': {'S': f"{now_saopaulo}"},
        'penaltis': {'S': penaltis}
    }
    
    response = creating_item_ddb(raw_dict)
    
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return {
            'Operação': "Concluida!",
            'Item': raw_dict
        }
    else:
        return {
            'Operação': "Falha!"
        }
    
def creating_item_ddb(raw_dict: dict):
    response = client.put_item(
        TableName=fifa_table,
        Item=raw_dict,
        ConditionExpression="attribute_not_exists(dfifa_id)"
        )
        
    return response