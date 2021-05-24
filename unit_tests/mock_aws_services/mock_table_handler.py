from moto import mock_dynamodb2
import string


@mock_dynamodb2
def create_testing_table(client, table_name, entity_name):
    client.create_table(
        AttributeDefinitions=[
            {
                'AttributeName': 'pk',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'sk',
                'AttributeType': 'S'
            },
        ],
        TableName=table_name,
        KeySchema=[
            {
                'AttributeName': 'pk',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'sk',
                'KeyType': 'RANGE'
            },
        ])

    client.put_item(
        TableName=table_name,
        Item={
            'pk': {
                'S': f"ENTITY#{entity_name}"
            },
            'sk': {
                'S': f'#META#{entity_name}'
            },
            'display_name': {
                'S': string.capwords(entity_name.replace('_', ' '))
            },
            'entity_source': {
                'S': f'ENTITY#{entity_name}'
            },
            'total_wins': {
                'N': '15'
            },
            'total_losses': {
                'N': '23'
            }
        }
    )


def create_expected_response(entity_name):
    full_name = string.capwords(entity_name.replace('_', ' '))
    return {
        'display_name': full_name,
        'entity_source': f'ENTITY#{entity_name}',
        'total_wins': 15,
        'total_losses': 23,
        'total_games': 38
    }
