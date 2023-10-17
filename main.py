import json
import boto3

client = boto3.client('dynamodb')
fifa_table = 'Daily_FIFA'

def lambda_handler(event, context):
    print(f'Evento: {event}')
    
    id = event['dfifa_id']
    vitorias = event['vitorias']
    empates = event['empates']
    derrotas = event['derrotas']
    
    raw_dict = {
        'dfifa_id': {'S': id},
        '__typename': {'S': f"user#{id}"},
        'vitorias': {'N': f'{vitorias}'},
        'empates': {'N': f'{empates}'},
        'derrotas': {'N': f'{derrotas}'}
    }
    
    response = creating_item_ddb(raw_dict)
    
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return {
            'Operação': "Concluida!",
            'Item': raw_dict
        }
    else:
        return {
            'Operação': "Falha!",
            'Item': raw_dict
        }
    
def creating_item_ddb(raw_dict: dict):
    response = client.put_item(
        TableName=fifa_table,
        Item=raw_dict,
        ConditionExpression="attribute_not_exists(dfifa_id)"
        )
        
    return response