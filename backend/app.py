from flask import Flask, request, jsonify
from flask_cors import CORS
from rag_processor import KnowledgeProcessor
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)
processor = KnowledgeProcessor()

UPLOAD_FOLDER = 'data/uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify(success=False, message="No file part"), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify(success=False, message="No selected file"), 400

    if file and allowed_file(file.filename):
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        try:
            processor.process_document(filepath)
            return jsonify(success=True, message="File uploaded successfully")
        except Exception as e:
            return jsonify(success=False, message=str(e)), 500

    return jsonify(success=False, message="Invalid file type"), 400


@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.json
    question = data.get('question', '')

    if not question:
        return jsonify(answer="Please provide a question"), 400

    try:
        context = processor.retrieve_context(question)
        answer = processor.generate_answer(question, context)
        return jsonify(answer=answer)
    except Exception as e:
        return jsonify(answer=f"Error: {str(e)}"), 500

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(host='0.0.0.0', port=5000)