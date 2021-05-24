from _pytest.fixtures import yield_fixture
from aws_cdk.aws_lambda import Function
from entity_lambda.entity_handler import entity_lambda_handler
from unit_tests.mock_aws_services.mock_table_handler import create_testing_table, create_expected_response
from moto import mock_dynamodb2
import pytest
import json
import boto3
from entity_lambda import *
import os


@pytest.fixture
def aws_credentials():
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"


@pytest.fixture
def lambda_env_variables():
    os.environ['TRACKER_DYNAMO'] = 'test_table'

    yield

    del os.environ['TRACKER_DYNAMO']


class TestEntityHandlerAPIEvents():

    def setup(self):
        pass

    def teardown(self):
        pass

    def test_lambda_handler_returns_200_status_and_message_if_path_is_not_enough(self, lambda_env_variables, aws_credentials):
        test_event = {
            "path": ""
        }

        expected_body = json.dumps({
            "message": "Not Enough Values in request. entity/[name] minium needed",
            "path": ""
        })

        response = entity_lambda_handler(test_event, {})

        assert response['statusCode'] == '200'
        assert response['body'] == expected_body


class TestEntityHandler():
    def setup(self):
        pass

    def teardown(self):
        pass

    def test_entity_handler_returns_something_wrong_message_when_missing_TRACKER_DYNAMO_env_variables(self):

        expected_body = json.dumps({
            "message": "Service is Temporary Unavailable. Please try again or notify an administrator.",
            "error": "ENV0001"
        })

        response = entity_lambda_handler(None, None)

        assert response['body'] == expected_body
        assert response['statusCode'] == '503'


@mock_dynamodb2
class TestEntityLambda_End_to_End():
    def setup(self):
        self.table_name = "test_table"
        self.client = boto3.client('dynamodb')
        self.test_entity_name = "legacy"

        create_testing_table(self.client, self.table_name,
                             self.test_entity_name)

    def teardown(self):
        self.client.delete_table(TableName=self.table_name)
        del self.client

    def test_lambda_handler_end_to_end(self, lambda_env_variables, aws_credentials):
        test_event = {"path": "/entity/legacy"}
        expected_response = json.dumps(create_expected_response(self.test_entity_name))

        response = entity_lambda_handler(test_event, {})

        assert response['body'] == expected_response
