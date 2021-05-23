import json

def create_base_response():
    return {
        "isBase64Encoded": True,
        "statusCode": "200",
        "headers": { 
            "X-Clacks-Overhead": "GNU Terry Pratchett",
            "Content-Type": "application/json"
            }
        } 