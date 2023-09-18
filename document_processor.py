import sys
from excel_translate import translate_excel_file
from translate_word import translate_docx
from pdf_convert_version2 import convert_pdf_to_translated_pdf
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
    elif filename.endswith(".pdf"):
        translated_doc = convert_pdf_to_translated_pdf(file_content, target_lang)
        translated_bytes = io.BytesIO()
        translated_doc.save(translated_bytes)
        translated_bytes.seek(0)    
    else:
        print(f"Error: Unsupported file format '{filename}'")
        return None  # Return None for unsupported formats

    return translated_bytes

# Define the content of the file and its filename
#file_content = "c:\\miso\\testy\\DS_Template_EN_TRM.MDGF.032.00_Tagetik for Approver.xlsx"
#filename = "DS_Template_EN_TRM.MDGF.032.00_Tagetik for Approver.xlsx"  # Change this to your desired file name
#target_lang = "DE"

# Call the translate_files function to process the file based on its format
#translated_content = translate_files(file_content, filename, target_lang)
