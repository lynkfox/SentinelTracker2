import json

def entity_lambda_handler(event:dict, context:dict) -> dict:
    '''
    Lambda Handler for the Entity API end points
    
    Path format
    
    entity_type/entity_name/game_type/outcome
    entity_type/entity_name/vs/second_entity_name/game_type/outcome
    
    '''
    
    path = event['path'].split('/')
    
    response = {
    "isBase64Encoded": True,
    "statusCode": "200",
    "headers": { 
        "x-clacks-overhead": "GNU-TerryPratchet",
        'Content-Type': 'application/json'},
    "body": json.dumps({
        "message": "Entity Handler Online",
        "path": event['path']
    })
    }
    
    return response