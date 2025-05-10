import os
import json
import random
from sentence_transformers import SentenceTransformer, util
from app.services.mongo_client import load_data_from_db

model = SentenceTransformer('all-MiniLM-L6-v2')
SIMILARITY_THRESHOLD = 0.4


def find_most_similar(user_input):

    qa_pairs = json.loads(load_data_from_db())

    fallback_entry = next(item for item in qa_pairs if item['question'] == 'fallback')
    fallback_answers = fallback_entry['answers']

    qa_pairs = [q for q in qa_pairs if q['question'] != 'fallback']
    questions = [q['question'] for q in qa_pairs]
    question_embeddings = model.encode(questions)

    input_embedding = model.encode(user_input)
    scores = util.cos_sim(input_embedding, question_embeddings)[0]

    best_score = scores.max().item()
    best_index = scores.argmax().item()

    if best_score >= SIMILARITY_THRESHOLD:
        matched_answers = qa_pairs[best_index]['answers']
        reply = random.choice(matched_answers)
    else:
        reply = random.choice(fallback_answers)

    return reply


