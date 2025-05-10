from flask import Blueprint, request, jsonify
from app.services.sentence_service import find_most_similar
from app.services.mongo_client import load_data_from_db
fe_communication_bp = Blueprint('fe_communication', __name__)

@fe_communication_bp.route('/get-answer', methods=['POST'])
def message_handler():
    user_input = request.json['message']
    reply = find_most_similar(user_input)
    return jsonify({'reply': reply})


@fe_communication_bp.route('/get-db', methods=['GET'])
def db_handler():
    return load_data_from_db()
