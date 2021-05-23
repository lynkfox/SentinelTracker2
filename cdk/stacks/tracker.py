from aws_cdk import (
    core as cdk,
    aws_lambda as aws_lambda,
    aws_dynamodb as dynamodb,
    aws_apigateway as api,
    aws_iam as iam
    
)
import os
from pathlib import Path

base_directory = Path(__file__).parents[2]


class Tracker(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        ################################
        # DynamoDBs                    #
        ################################
        
        tracker_db = dynamodb.Table(
            self, "TrackerDynamo",
            table_name="SentinelsCardGameTracker",
            partition_key={ 'name': 'pk', 'type': dynamodb.AttributeType.STRING},
            sort_key={ 'name': 'sk', 'type': dynamodb.AttributeType.STRING}
        )
        
        ################################
        # Lambdas                      #
        ################################
        
        ###########
        # Env Var #
        ###########
        
        lambda_environment_variables = {
            'TRACKER_DYNAMO': tracker_db.table_name
        }
        
        entity_lambda = aws_lambda.Function(
            self, "EntityLambda",
            function_name="Entity_Lambda",
            runtime=aws_lambda.Runtime.PYTHON_3_8,
            handler='entity_handler.entity_lambda_handler',
            code=aws_lambda.Code.asset(os.path.join(base_directory, "lambdas/entity_lambda")),
            environment=lambda_environment_variables
        )
        
        ################################
        # APIs                         #
        ################################
        
        tracker_api = api.LambdaRestApi(
            self, 'TrackerEndpoint',
            handler=entity_lambda,
            proxy=True,
            
        )
        
        tracker_resource = tracker_api.root.add_resource("entity")
        tracker_resource.add_method("GET", api_key_required=True)
        
        api_usage_plan = tracker_api.add_usage_plan(
            "TrackerUsagePlan",
            name="TrackerUsagePlan",
            throttle={
                "rate_limit": 10,
                "burst_limit": 3
            }
        )
        
        api_key = tracker_api.add_api_key("TrackerKey")
        api_usage_plan.add_api_key(api_key)
        
        
        