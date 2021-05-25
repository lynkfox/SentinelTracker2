from re import L
import boto3
from moto import mock_dynamodb2
import pytest
from entity_dynamo_functions import EntityCommands
from unit_tests.mock_aws_services.mock_table_handler import create_testing_table, create_expected_response


@mock_dynamodb2
class TestEntityDynamoFunctionsWithDynamoActive():

    def setup(self):
        self.table_name = "test_table"
        self.client = boto3.client('dynamodb')
        self.test_entity_name = "baron_blade"

        create_testing_table(self.client, self.table_name,
                             self.test_entity_name)

        self.entity = EntityCommands(self.table_name, self.test_entity_name)

    def teardown(self):
        del self.entity
        self.client.delete_table(TableName=self.table_name)
        del self.client

    def test_get_all_entity_returns_full_dictionary_of_all_entities_data(self):
        expected_result = create_expected_response(self.test_entity_name)

        self.entity.get_all_entity_data()

        assert self.entity.entity_data == expected_result

    def test_get_meta_data_converts_meta_sk_entry_to_dictionary(self):
        result_from_dynamo_0 = {
            'display_name': 'Baron Blade',
            'entity_source': 'ENTITY#baron_blade',
            'pk': 'ENTITY#baronblade',
            'sk': '#META#baronblade',
            'total_losses': 23,
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
