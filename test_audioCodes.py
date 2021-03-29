from flask import Flask, jsonify, request, make_response
import pytest

app = Flask(__name__)
bots_list = [{
    'provider': 'AudioCodes',
    'name': 'Eden',
    'display_name': 'bot1',
    'credentials': 'none'
},
    {
        'provider': 'EdenBeAm',
        'name': 'Omri',
        'display_name': 'bot2',
        'credentials': 'none'
    }]


@app.route('/', methods=['GET'])
def authorization():  # The user must enter the correct username and password
    if request.authorization and request.authorization.username == 'audiocodes' and request.authorization.password == '1234':
        return '<h1>hello AudioCodes</h1>'
    return make_response('you have to login to the server', 401, {
        'WWW-Authenticate': 'Basic realm="loging required"'})


def test_base_route():#check the bot list and the http status code
    app = Flask(__name__)
    client = app.test_client()
    url = '/'
    response = client.get(url)
    assert response.get_data() == bots_list
    assert response.status_code == 200


@app.route('/botlist', methods=['GET'])  # /botlist will show us all the bots info
def return_All_Bots():
    return jsonify({'This is the bot lists': bots_list})  #


@app.route('/botlist/<string:name>',
           methods=['GET'])  # /botlist/'some name' will show us specific bot info, for example "/botlist/eden"
def return_Requested_Bot(name):
    bot = [bot_object for bot_object in bots_list if bot_object['name'] == name]
    return jsonify({'Requested Bot': bot[0]})


@app.route('/botlist/post/<string:name>', methods=['POST'])
def add_Bot():#add a new bot
    new_bot = {'name': request.json['name']}
    bots_list.append(new_bot)
    return jsonify({'new': bots_list})


@app.route('/botlist/<string:name>', methods=['PUT'])
def edit_Bot(name):#edit a bot
    edit_bot = [bot_object for bot_object in bots_list if bot_object['name'] == name]
    edit_bot[0]['name'] = request.json['name']
    return jsonify({'bots': edit_bot[0]})


@app.route('/botlist/<string:name>', methods=['DELETE'])
def remove_Bot(name):#remove a bot
    bot = [bot_object for bot_object in bots_list if bot_object['name'] == name]
    bots_list.remove(bot[0])
    return jsonify({'remove': bots_list})


if __name__ == '__main__':
    app.run(debug=True, port=8080)  # run app on port 8080 in debug mode
