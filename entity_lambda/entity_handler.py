import json
import os
from api_helpers import *
from entity_dynamo_functions import EntityCommands
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def entity_lambda_handler(event: dict, context: dict) -> dict:
    '''
    Lambda Handler for the Entity API end points

    Path format

    /entity_type/entity_name/game_type/outcome
    /entity_type/entity_name/vs/second_entity_name/game_type/outcome

    '''
    response = create_base_response()

    # Verify Env Variables All Exist
    try:
        ENTITY_TABLE = os.environ['TRACKER_DYNAMO']
    except KeyError as e:
        logger.critical(
            f'[entity_lambda_handler] - Missing environment variable {e.args[0]}')

        if e.args[0] == "TRACKER_DYNAMO":
            error_code = "ENV0001"

        response['body'] = json.dumps({
            "message": "Service is Temporary Unavailable. Please try again or notify an administrator.",
            "error": error_code
        })

        response['statusCode'] = '503'
        return response

    logger.info(f"[entity_lambda_handler] - Handler called with {event['path']}.")
    path = event['path'].split('/')[1:]

    if len(path) < 2:
        response['body'] = json.dumps({
            "message": "Not Enough Values in request. entity/[name] minium needed",
            "path": event['path']
        })
    else:
        # TODO: Add check for path[1] == entity/hero/villain/environment/gametype/box
        logger.info(f"[entity_lambda_handler] - Initalizing Search for {path[1]}.")
        entity = EntityCommands(ENTITY_TABLE, path[1])
        response['body'] = json.dumps(entity.entity_data)

    return response
