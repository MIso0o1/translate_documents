import os
import zipfile
from xml.etree import ElementTree as ET
from translate_text import translate_text_with_deepl  # Assuming the translate_text module is available

def extract_hyperlink_anchor_text(docx_file_path):
    anchor_texts = []
    with zipfile.ZipFile(docx_file_path, 'r') as zip_ref:
        xml_content = zip_ref.read('word/document.xml')
        root = ET.fromstring(xml_content)
        for hyperlink in root.findall('.//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}hyperlink'):
            anchor_text = hyperlink.find('.//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t')
            if anchor_text is not None and anchor_text.text is not None:
                anchor_texts.append(anchor_text.text)
    return anchor_texts

def translate_and_create_new_docx(docx_file_path, target_lang):
    anchor_texts = extract_hyperlink_anchor_text(docx_file_path)
    translated_anchor_texts = []
    for text in anchor_texts:
        translated_text = translate_text_with_deepl(text, target_lang)
        translated_anchor_texts.append(translated_text)

    output_filename = os.path.splitext(docx_file_path)[0] + "_translated.docx"
    with zipfile.ZipFile(docx_file_path, 'r') as zip_ref:
        with zipfile.ZipFile(output_filename, 'w') as new_zip_ref:
            for item in zip_ref.infolist():
                content = zip_ref.read(item.filename)
                if item.filename == 'word/document.xml':
                    xml_content = content.decode('utf-8')
                    for i, anchor_text in enumerate(anchor_texts):
                        xml_content = xml_content.replace(anchor_text, translated_anchor_texts[i])
                    new_zip_ref.writestr(item, xml_content.encode('utf-8'))
                else:
                    new_zip_ref.writestr(item, content)
    return output_filename

# Example usage:
#docx_file_path = "c:\\miso\\testy\\DS_Template_EN_TRM.MDGF.032.00_Tagetik for Approver.docx"  # Replace with your file path
#target_lang = "de"  # Replace with your target language code
#translated_docx_path = translate_and_create_new_docx(docx_file_path, target_lang)
#print(f"Translated document created at: {translated_docx_path}")
