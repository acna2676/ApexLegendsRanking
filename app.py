import json
import os
import sys
from pprint import pprint

import jinja2  # import Environment, FileSystemLoader, select_autoescape
import requests
from chalice import Chalice, Response
from flask import Flask, render_template, request

# from chalicelib import staticfiles  # noqa
from chalicelib import API_KEY

app = Chalice(app_name='ApexLegendsRanking')
# app = Flask(__name__)


TRN_URL = 'https://public-api.tracker.gg/v2/apex/standard'
# with open("credentials.json") as f:
#     credentials = json.load(f)
# API_KEY = credentials['access_token']  # 自分のAPIキーを入力

# ユーザープロフィールを取得


def get_streamer_rank():
    streamer_ids = ["CR_RAS_LOG", "NIRUi7", "tttcheekyttt_SBI"]  # , "りんしゃんつかい"]  # ,
    # "ULT_ちひ太郎",	"ABC_EluAndrade	",
    # "丁1_かえで",	"Xogkewlkvy",
    # "Hajimen_2434",	"umiushi_2434",	"mugi_ienaga"]
    rank_list = {}
    for player_id in streamer_ids:
        response = GetProfile('origin', player_id)
        CheckResponseStats(response)

        user_stats = json.loads(response.text)
        stats = user_stats['data']['segments'][0]['stats']
        for key, value in stats.items():
            if key == "rankScore":
                rank_list[player_id] = int(value['displayValue'].replace(",", ""))
    rank_list_sorted = sorted(rank_list.items(), key=lambda x: x[1], reverse=True)
    return rank_list_sorted


def GetProfile(platform, playerId):
    sendUrl = TRN_URL + '/profile'
    sendUrl += '/' + platform
    sendUrl += '/' + playerId
    sendUrl += '?TRN-Api-Key=' + API_KEY
    print('sendUrl :', sendUrl)

    # http getリクエスト送信
    response = requests.get(sendUrl)

    return response

# レスポンスをチェック


def CheckResponseStats(response):

    # 200以外の場合は失敗
    if response.status_code != 200:
        print(response.status_code, 'error')
        sys.exit()


def DispStats(json):
    # statsに主な戦績データが入ってるぽい
    stats = json['data']['segments'][0]['stats']
    # pprint(stats)

    for key, value in stats.items():
        print(key, value['displayValue'])


@ app.route('/', methods=["GET", "POST"], content_types=["*/*"])
def index():

    rank_list_sorted = get_streamer_rank()
    print(rank_list_sorted)

    # if request.method == "POST":
    if app.current_request.method == "POST":
        print(app.current_request.raw_body)
        key_pair_list = app.current_request.raw_body.decode()
        player_id_pair = key_pair_list.split("&")[0]
        platform_pair = key_pair_list.split("&")[1]
        player_id = player_id_pair.split("=")[1]
        platform = platform_pair.split("=")[1]
        # player_id = app.current_request.form['playerId']
        # platform = app.current_request.form['platform']
    else:
        platform = 'origin'
        player_id = "CR_RAS_LOG"
    response = GetProfile(platform, player_id)
    CheckResponseStats(response)

    user_stats = json.loads(response.text)
    stats = user_stats['data']['segments'][0]['stats']
    stats_list = {}
    for key, value in stats.items():
        stats_list[key] = value['displayValue']

    #     return render_template('index.html', title='ALR', stats_list=stats_list, rank_list_sorted=dict(rank_list_sorted))
    context = {'stats_list': stats_list, 'rank_list_sorted': dict(rank_list_sorted)}
    template = render("chalicelib/templates/index.html", context)
    return Response(template, status_code=200, headers={"Content-Type": "text/html", "Access-Control-Allow-Origin": "*"})


def render(tpl_path, context):
    path, filename = os.path.split(tpl_path)
    return jinja2.Environment(loader=jinja2.FileSystemLoader(path or "./")).get_template(filename).render(context)


# @app.route('/')
# def index():
#     context = {'stats_list': {"a": "a"}, 'rank_list_sorted': {"a": "a"}}
#     template = render("chalicelib/templates/index.html", context)
#     return Response(template, status_code=200, headers={"Content-Type": "text/html", "Access-Control-Allow-Origin": "*"})
    # return render_template('index.html', title='ALR', stats_list={"a": "a"}, rank_list_sorted={"a": "a"})


@app.route('/chalicelib/static/css/style.css')
def cssindex():
    with open('chalicelib/static/css/style.css') as f:
        data = f.read()
    return Response(body=data, status_code=200, headers={"Content-Type": "text/css", "Access-Control-Allow-Origin": "*"})


@app.route('/favicon.ico')
@app.route('/chalicelib/favicon.ico')
def cfaviconindex():
    with open('chalicelib/static/favicon.ico', 'rb') as fp:
        data = fp.read()
    return Response(body=data, status_code=200, headers={"Content-Type": "image/png", "Access-Control-Allow-Origin": "*"})


if __name__ == "__main__":
    app.run(debug=True, port=8888, threaded=True)

# 実行方法
# python app.py
