from entity_lambda.entity_handler import entity_lambda_handler
import pytest
import json
from entity_lambda import *

class TestEntityHandlerAPIEvents():
    
    def setup(self):
        pass
        
    def teardown(self):
        pass

    def test_lambda_handler_returns_200_status_and_message_if_path_is_not_enough(self):
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