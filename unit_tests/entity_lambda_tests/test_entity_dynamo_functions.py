from re import L
import boto3
from moto import mock_dynamodb2
import pytest
from entity_dynamo_functions import EntityCommands

@mock_dynamodb2
class TestEntityDynamoFunctionsWithDynamoActive():
    
    def setup(self):
        self.table_name = "test_table"
        self.client = boto3.client('dynamodb')
        self.test_entity_name = "baronblade"
        
        self.client.create_table(
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
            TableName=self.table_name,
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
        
        self.client.put_item(
            TableName=self.table_name,
            Item={
                'pk': {
                    'S': f"ENTITY#{self.test_entity_name}"
                },
                'sk': {
                    'S': f'#META#{self.test_entity_name}'
                },
                'display_name': {
                    'S': 'Baron Blade'
                },
                'entity_source': {
                    'S': f'ENTITY#{self.test_entity_name}'
                },
                'total_wins': {
                    'N': '15'
                },
                'total_losses': {
                    'N': '23'
                }
            }
        )
        
        self.entity = EntityCommands(self.table_name, self.test_entity_name)
    
    def teardown(self):
        del self.entity
        self.client.delete_table(TableName=self.table_name)
        del self.client
        
    def test_get_all_entity_returns_full_dictionary_of_all_entities_data(self):
        expected_result = {
            'Name': 'Baron Blade',
            'Entity': "baronblade",
            "TotalWins": 15,
            "TotalLosses": 23
        }
        
        self.entity.get_all_entity_data()
        
        assert self.entity.entity_data == expected_result
        
    def test_get_meta_data_converts_meta_sk_entry_to_dictionary(self):
        result_from_dynamo_0 = {
            'display_name': 'Baron Blade',
            'entity_source': 'ENTITY#baronblade',
            'pk': 'ENTITY#baronblade',
            'sk': '#META#baronblade',
            'total_losses':23,
            'total_wins': 15
            }
        
        expected_result = {
            'display_name': "Baron Blade",
            'entity_source': f'ENTITY#{self.test_entity_name}',
            'total_wins': 15,
            'total_losses': 23,
            'total_games': 38
            }
        
        self.entity.get_meta_data(result_from_dynamo_0)
        
        assert self.entity.entity_data == expected_result
        
    def test_calculate_total_games_correctly_tallies_total_game_amount(self):
        wins = 15
        loses = 23
        
        self.entity.calculate_total_games(wins, loses)
        
        assert self.entity.entity_data['total_games'] == 38
        