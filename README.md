# SentinelTracker2

A Restful API backed by AWS Lambdas and Dynamo DB for storing, tracking, and retrieving Sentinels Card Game Tracking Information

# Lambdas

## entity_lambda

This lambda is responsible for returning various Entity data - from Meta Data to Staticics Data

called from the api: entity/name/additional/arguments/to/narrow/search

eg. entity/baronblade/vs/legacy
eg. entity/baronblade/wins
eg. entity/baronblade/wins/insulaprimalis
## user_lambda

This lambda will be responsible for updating and retriving user specific data

called from the api: user/username

eg. user/username/create
eg. user/username/games
eg. 

## record_lambda

This lambda will be responsible for adding new games to the database. This API will be the only one that expects a JSON in the body of the message that will need to be provided for input

called from the api: statistics/

# utilities

## google_sheets_translator.py

This file will connect to the former Google Sheets location of the Statistics, download and output the data in a json format for consumption by the AWS CLI dynamodb to load all existing data into the dyanmo