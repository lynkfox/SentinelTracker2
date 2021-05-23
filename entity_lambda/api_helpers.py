import json

def create_base_response():
    return {
        "isBase64Encoded": True,
        "statusCode": "200",
        "headers": { 
            "x-clacks-overhead": "GNU-TerryPratchet",
            'Content-Type': 'application/json'}
        } 