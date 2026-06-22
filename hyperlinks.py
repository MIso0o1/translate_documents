import os
import zipfile
import asyncio
import httpx
from xml.etree import ElementTree as ET
from translate_text import translate_text_with_deepl_async

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

async def translate_and_create_new_docx_async(docx_file_path, target_lang):
    anchor_texts = extract_hyperlink_anchor_text(docx_file_path)
    translated_anchor_texts = []

    async with httpx.AsyncClient() as client:
        tasks = [translate_text_with_deepl_async(text, target_lang, client) for text in anchor_texts]
        translated_anchor_texts = await asyncio.gather(*tasks)

    output_filename = os.path.splitext(docx_file_path)[0] + "_translated.docx"
    with zipfile.ZipFile(docx_file_path, 'r') as zip_ref:
        with zipfile.ZipFile(output_filename, 'w') as new_zip_ref:
            for item in zip_ref.infolist():
                content = zip_ref.read(item.filename)
                if item.filename == 'word/document.xml':
                    xml_content = content.decode('utf-8')
                    for i, anchor_text in enumerate(anchor_texts):
                        if translated_anchor_texts[i]:
                            xml_content = xml_content.replace(anchor_text, translated_anchor_texts[i])
                    new_zip_ref.writestr(item, xml_content.encode('utf-8'))
                else:
                    new_zip_ref.writestr(item, content)
    return output_filename

def translate_and_create_new_docx(docx_file_path, target_lang):
    return asyncio.run(translate_and_create_new_docx_async(docx_file_path, target_lang))
