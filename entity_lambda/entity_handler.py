import json
from api_helpers import *


def entity_lambda_handler(event:dict, context:dict) -> dict:
    '''
    Lambda Handler for the Entity API end points
    
    Path format
    
    entity_type/entity_name/game_type/outcome
    entity_type/entity_name/vs/second_entity_name/game_type/outcome
    
    '''
    response = create_base_response()
    
    path = event['path'].split('/')
    
    if len(path) < 2:
        response['body'] = json.dumps({
                                "message": "Not Enough Values in request. entity/[name] minium needed",
                                "path": event['path']
                            })
    
    else:
        pass
        
    
    return response
