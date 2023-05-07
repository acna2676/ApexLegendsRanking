import json

import boto3
import requests

TRN_URL = 'https://public-api.tracker.gg/v2/apex/standard'
API_KEY = "ebc6b0c6-4ff9-4a75-bd63-838132dc1a72"


def put_db(ranking_list, dynamodb=None):
    if not dynamodb:
        # dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')
        dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('ApexLegendsRanking')
    response = table.put_item(Item={'ranking': 'ranking', 'ranking_list': ranking_list})
    return response


def get_streamer_rank():
    streamer_ids = ["CR_RAS_LOG"]  # , "NIRUi7", "tttcheekyttt_SBI"]  # , "りんしゃんつかい"]  # ,
    rank_list = {}
    for player_id in streamer_ids:
        response = GetProfile('origin', player_id)

        user_stats = json.loads(response.text)
        stats = user_stats['data']['segments'][0]['stats']
        for key, value in stats.items():
            if key == "rankScore":
                rank_list[player_id] = int(value['displayValue'].replace(",", ""))
    rank_list_sorted = sorted(rank_list.items(), key=lambda x: x[1], reverse=True)
    print(type(rank_list_sorted))
    print(rank_list_sorted)
    return rank_list_sorted


def GetProfile(platform, playerId):
    sendUrl = TRN_URL + '/profile'
    sendUrl += '/' + platform
    sendUrl += '/' + playerId
    # sendUrl += '?TRN-Api-Key=' + API_KEY
    print('sendUrl :', sendUrl)

    headers = {'TRN-Api-Key': API_KEY}

    response = requests.get(sendUrl, headers=headers)

    print('status_code :', response.status_code)

    return response


def lambda_main():

    rank_list_sorted = get_streamer_rank()
    put_db(rank_list_sorted)
    # query_db()


def handler(_1, _2):
    lambda_main()
    return


# handler(None, None)

# def query_db(dynamodb=None):
#     if not dynamodb:
#         dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')
#     table = dynamodb.Table('ApexLegendsRanking')
#     response = table.query(
#         KeyConditionExpression=Key('ranking').eq('ranking')
#     )
#     print(type(response['Items'][0]['ranking_list']))
#     print(response['Items'][0]['ranking_list'])
#     return response['Items'][0]['ranking_list']


# def to_dict(ranking_list):
#     ranking_list_formatted = [x for x in map(lambda n:(n[0], int(n[1])), ranking_list)]  # [['CR_RAS_LOG', Decimal('17442')]] -> [('CR_RAS_LOG', 17442)]
#     result = dict(ranking_list_formatted)
#     return result
