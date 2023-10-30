import json
import boto3
from boto3.dynamodb.conditions import Attr
from datetime import datetime

client = boto3.client('dynamodb')
fifa_table = 'Daily_FIFA'

def lambda_handler(event, context):
    print(f'Evento: {event}')
    
    response = scan_attributes()
    
    new_response = []
    
    for resp in response:
        item = deep_clean_field(resp)
        new_response.append(item)
    
    print(f'New Response: {new_response}')
    
    updating = update_data(new_response)
    
    return {
        'statusCode': 200,
        'message': "Update Concluido"
    }
    
def scan_attributes():
    expressao_filtro = 'attribute_not_exists(penaltis)'
    
    resultado = client.scan(
        TableName=fifa_table,
        FilterExpression=expressao_filtro
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

def update_ids(dfifa_id, competicao):
    response = client.update_item(
        TableName=fifa_table,
        Key={
            'dfifa_id': {'S': str(dfifa_id)},
            'competicao': {'S': competicao}
        },
        UpdateExpression='SET penaltis = :penaltis',
        ExpressionAttributeValues={
            ':penaltis': {'S': '-'}
        }
    )

    return response

def change_data_style(timestamp):
    data = datetime.fromtimestamp(timestamp)
    new_data = data.strftime('%d/%m/%Y')
    return new_data

def update_data(raw_list: list):
    for item in raw_list:
        dfifa_id = item['dfifa_id']
        # day_and_time = int(item['day&time'])
        competicao = item['competicao']
        
        # day = change_data_style(day_and_time)
        
        response = update_ids(dfifa_id, competicao)
    
    return