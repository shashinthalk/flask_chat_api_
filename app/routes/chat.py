import os
import json
import random
from flask import Blueprint, request, jsonify
from sentence_transformers import SentenceTransformer, util

chat_bp = Blueprint('chat', __name__)

# Load model and data once when blueprint is loaded
model = SentenceTransformer('all-MiniLM-L6-v2')

current_dir = os.path.dirname(__file__)
data_file_path = os.path.join(current_dir, 'qa_data.json')

with open(data_file_path) as f:
    qa_pairs = json.load(f)

fallback_entry = next(item for item in qa_pairs if item['question'] == 'fallback')
fallback_answers = fallback_entry['answers']

qa_pairs = [q for q in qa_pairs if q['question'] != 'fallback']
questions = [q['question'] for q in qa_pairs]
question_embeddings = model.encode(questions)

SIMILARITY_THRESHOLD = 0.4

@chat_bp.route('/chat', methods=['POST'])
def chat():
    user_input = request.json['message']
    input_embedding = model.encode(user_input)
    scores = util.cos_sim(input_embedding, question_embeddings)[0]

    best_score = scores.max().item()
    best_index = scores.argmax().item()

    if best_score >= SIMILARITY_THRESHOLD:
        matched_answers = qa_pairs[best_index]['answers']
        reply = random.choice(matched_answers)
    else:
        reply = random.choice(fallback_answers)

    return jsonify({'reply': reply})
