import boto3
import json
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key
from decimal import *
import logging


class EntityCommands():
    def __init__(self, table_name: str, entity: str) -> None:
        '''
        Contains the necessary information for a single entity and retrieving data for it
        '''
        self.ddb = boto3.resource('dynamodb')
        self.entity_table = self.ddb.Table(table_name)
        self.entity_name = entity
        self.entity_data = {}
        self.get_all_entity_data()

    def get_all_entity_data(self) -> None:
        '''
        Retrieves all the info of an entity and collapses it into a single dictionary.
        '''

        entity_items = self.entity_table.query(
            KeyConditionExpression=Key('pk').eq(f'ENTITY#{self.entity_name}')
        )['Items']

        # Extract the Various Items belonging to this Entity
        self.get_meta_data(entity_items[0])

        self.calculate_total_games(self.entity_data.get('total_wins'), self.entity_data.get('total_losses'))

    def get_meta_data(self, meta_data: dict) -> None:
        '''
        Takes the MetaData of a given entity and translates it to the entity_data.

        Parameters:
            meta_data(Dictionary): The [0] index of the dynamodby Items response.
        '''
        logging.info('[entity_lambda.EntityCommands] - Retrieving Metadata')
        for key in meta_data:
            if key == 'pk' or key == 'sk':
                continue
            elif isinstance(meta_data[key], Decimal):
                self.entity_data.update({key: int(meta_data[key])})
            else:
                self.entity_data.update({key: meta_data[key]})

    def calculate_total_games(self, *args) -> None:
        '''
        Quick Sum the Args
        '''
        logging.info('[entity_lambda.EntityCommands] - Calculating Total Games')
        self.entity_data['total_games'] = sum(list(args))
