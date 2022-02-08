#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""[summary]

    Returns:
        [type]: [description]
"""
import os
import socket
import random
import json
import requests
from flask import Flask, render_template, request, make_response, send_from_directory

option_a = os.getenv('OPTION_A', "Dog 🐺")
option_b = os.getenv('OPTION_B', "Cat 🐶")
hostname = socket.gethostname()

app = Flask(__name__)


@app.route("/", methods=['POST','GET'])
def hello():
    """[summary]

    Returns:
        [type]: [description]
    """
    rest_endpoint="http://" + os.environ["VOTING_API_SERVICE_HOST"] + ":" +\
        os.environ["VOTING_API_SERVICE_PORT"]
    voter_id = request.cookies.get('voter_id')
    if not voter_id:
        voter_id = hex(random.getrandbits(64))[2:-1]

    vote = None
    if request.method == 'POST':
        vote = request.form['vote']
        data = json.dumps({'voter_id': voter_id, 'vote': vote})
        requests.post(url=rest_endpoint + "/vote", data=data)

    resp = make_response(render_template(
        'index.html',
        option_a=option_a,
        option_b=option_b,
        hostname=hostname,
        vote=vote,
    ))
    resp.set_cookie('voter_id', voter_id)
    return resp

@app.route("/result", methods=['GET'])
def result():
    """[summary]

    Returns:
        [type]: [description]
    """
    return make_response(render_template('result/index.html'))


@app.route("/votes", methods=['GET'])
def votes():
    """[summary]

    Returns:
        [type]: [description]
    """
    rest_endpoint="http://" + os.environ["VOTING_API_SERVICE_HOST"] + ":" +\
        os.environ["VOTING_API_SERVICE_PORT"]
    response = requests.get(url=rest_endpoint + "/vote")
    print(response.content)
    return response.content

@app.route('/templates/<path:path>')
def send_js(path):
    """[summary]

    Returns:
        [type]: [description]
    """
    return send_from_directory('templates', path)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
