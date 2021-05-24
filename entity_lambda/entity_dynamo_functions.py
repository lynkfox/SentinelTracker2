import boto3
import json
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

class EntityCommands():
    def __init__(self, table_name:str, entity:str) -> None:
        '''
        Contains the necessary information for a single entity and retrieving data for it
        '''
        self.ddb = boto3.resource('dynamodb')
        self.entity_table = self.ddb.Table(table_name)
        self.entity_name = entity
    
    def get_all_entity_data(self) -> dict:
        '''
        Retrieves all the info of an entity and collapses it into a single dictionary
        
        Returns:
            (Dictionary): All the entities dynamo items collapsed.
        '''
        
        entity_items = self.entity_table.query(
            KeyConditionExpression=Key('pk').eq(f'ENTITY#{self.entity_name}')
        )['Items']
        
        entity_data = self.get_meta_data(entity_items[0])
        
    def get_meta_data(self, meta_data:dict) -> dict:
        
        return {
            'display_name': meta_data.get('display_name'),
            'entity_source': meta_data.get('entity_source'),
            'total_wins': int(meta_data.get('total_wins')),
            'total_losses': int(meta_data.get('total_losses'))
        }
        
        
        
        
        