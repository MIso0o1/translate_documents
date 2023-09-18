import os
import io
import base64
from flask import Flask, request, jsonify
from document_processor import translate_files  # Import your translation function

app = Flask(__name__)

@app.route('/translate', methods=['POST'])
def translate():
    try:
        # Check if a file was included in the request
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400

        uploaded_file = request.files['file']

        # Check if the file has a filename
        if uploaded_file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        target_lang = request.form['language']

        if not target_lang:
            return jsonify({'error': 'Target language not provided'}), 400

        # Read the content of the uploaded file as BytesIO-like object
        file_content = io.BytesIO(uploaded_file.read())

        # Call the translation function
        translated_content = translate_files(file_content, uploaded_file.filename, target_lang)

        # Encode the translated content as base64
        base64_content = base64.b64encode(translated_content.read()).decode('utf-8')

        # Return the base64-encoded content in the response
        return jsonify({'translated_content': base64_content})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
