import os
import io
import base64
import logging  
from flask import Flask, request, jsonify
from document_processor import translate_files 
from flask_restful import Api, Resource, reqparse

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Authentication function to validate API keys
def authenticate(api_key):
    # Replace 'API_KEY' with the actual name of your environment variable
    heroku_api_key = os.environ.get('API_KEY')

    if api_key == heroku_api_key:
        return True
    else:
        return False
    
@app.route('/translate', methods=['POST'])
def translate():
    try:
        logger.info('Received translation request')

        # Check for the API key in the request headers
        api_key = request.headers.get('X-API-Key')

        if not api_key:
            logger.error('No API key provided in the request')
            return jsonify({'error': 'API key missing'}), 401

        # Authenticate the API key
        if not authenticate(api_key):
            logger.error('Invalid API key provided in the request')
            return jsonify({'error': 'Invalid API key'}), 401
        
        # Check if a file was included in the request
        if 'file' not in request.files:
            logger.error('No file provided in the request')
            return jsonify({'error': 'No file provided'}), 400

        uploaded_file = request.files['file']

        # Check if the file has a filename
        if uploaded_file.filename == '':
            logger.error('No selected file in the request')
            return jsonify({'error': 'No selected file'}), 400

        target_lang = request.form['language']

        if not target_lang:
            logger.error('Target language not provided in the request')
            return jsonify({'error': 'Target language not provided'}), 400

        # Read the content of the uploaded file as BytesIO-like object
        file_content = io.BytesIO(uploaded_file.read())

        # Construct the file path using os.path.join()
        file_name = uploaded_file.filename
        file_path = os.path.join('uploads', file_name)  

        # Call the translation function
        translated_content = translate_files(file_content, file_path, target_lang)

        # Encode the translated content as base64
        base64_content = base64.b64encode(translated_content.read()).decode('utf-8')

        # Return the base64-encoded content in the response
        return jsonify({'translated_content': base64_content})

    except FileNotFoundError as e:
        logger.error(f'File not found: {str(e)}')
        return jsonify({'error': f'File not found: {str(e)}'}), 404

    except Exception as e:
        logger.exception('An error occurred during processing')
        return jsonify({'error': 'An error occurred'}), 500

if __name__ == '__main__':
    # Use the PORT environment variable if available (for Heroku)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)



