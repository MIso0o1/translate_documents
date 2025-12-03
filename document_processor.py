import sys
from excel_translate import translate_excel_file
from translate_word import translate_docx
from powerpoint_translate import translate_pptx_file
import io  

def translate_files(file_content, filename, target_lang):

    if filename.endswith(".docx"):
        translated_doc = translate_docx(file_content, target_lang)
        translated_bytes = io.BytesIO()
        translated_doc.save(translated_bytes)
        translated_bytes.seek(0)
    elif filename.endswith(".xlsx"):
        translated_doc = translate_excel_file(file_content, target_lang)
        translated_bytes = io.BytesIO()
        translated_doc.save(translated_bytes)
        translated_bytes.seek(0)
    elif filename.endswith(".pptx"):
        translated_doc = translate_pptx_file(file_content, target_lang)
        translated_bytes = io.BytesIO()
        translated_doc.save(translated_bytes)
        translated_bytes.seek(0)    
    else:
        print(f"Error: Unsupported file format '{filename}'")
        return None  # Return None for unsupported formats

    return translated_bytes

