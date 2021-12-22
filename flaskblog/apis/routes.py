from flask import request, Blueprint
from flask import jsonify

rest_api = Blueprint('rest_api', __name__)

@rest_api.route("/api", methods=['GET'])
def sample():
    return jsonify({'name': 'Jimit',
                    'address': 'India'})

@rest_api.route('/post', methods=["POST", 'GET'])
def test_post():
    input_json = request.get_json(force=True)
    dict_to_return = {'text1': input_json['text']}
    return jsonify(dict_to_return)
