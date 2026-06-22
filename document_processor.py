import sys
import io
import asyncio
from excel_translate import translate_excel_file_async
from translate_word import translate_docx_async
from powerpoint_translate import translate_pptx_file_async

async def translate_files_async(file_content, filename, target_lang):
    if filename.endswith(".docx"):
        translated_doc = await translate_docx_async(file_content, target_lang)
        translated_bytes = io.BytesIO()
        translated_doc.save(translated_bytes)
        translated_bytes.seek(0)
    elif filename.endswith(".xlsx"):
        translated_doc = await translate_excel_file_async(file_content, target_lang)
        translated_bytes = io.BytesIO()
        translated_doc.save(translated_bytes)
        translated_bytes.seek(0)
    elif filename.endswith(".pptx"):
        translated_doc = await translate_pptx_file_async(file_content, target_lang)
        translated_bytes = io.BytesIO()
        translated_doc.save(translated_bytes)
        translated_bytes.seek(0)    
    else:
        print(f"Error: Unsupported file format \'{filename}\'")
        return None  # Return None for unsupported formats

    return translated_bytes
