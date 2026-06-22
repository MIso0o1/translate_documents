import os
import io
import base64
import logging
from fastapi import FastAPI, File, UploadFile, Header, HTTPException, Form
from fastapi.responses import JSONResponse
from document_processor import translate_files_async

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI()

def authenticate(api_key: str) -> bool:
    heroku_api_key = os.environ.get('API_KEY')
    return api_key == heroku_api_key

@app.post('/translate')
async def translate(file: UploadFile = File(...), language: str = Form(...), x_api_key: str = Header(None)):
    logger.info('Received translation request')

    if not x_api_key:
        logger.error('No API key provided in the request')
        raise HTTPException(status_code=401, detail='API key missing')

    if not authenticate(x_api_key):
        logger.error('Invalid API key provided in the request')
        raise HTTPException(status_code=401, detail='Invalid API key')
    
    if not language:
        logger.error('Target language not provided in the request')
        raise HTTPException(status_code=400, detail='Target language not provided')

    try:
        file_content = io.BytesIO(await file.read())
        file_name = file.filename

        translated_content = await translate_files_async(file_content, file_name, language)

        if translated_content is None:
            raise HTTPException(status_code=500, detail='Translation failed or unsupported file format')

        base64_content = base64.b64encode(translated_content.read()).decode('utf-8')

        return JSONResponse(content={'translated_content': base64_content})

    except HTTPException as e:
        raise e
    except Exception as e:
        logger.exception('An error occurred during processing')
        raise HTTPException(status_code=500, detail=f'An error occurred: {str(e)}')

if __name__ == '__main__':
    import uvicorn
    port = int(os.environ.get('PORT', 5000))
    uvicorn.run(app, host='0.0.0.0', port=port)
