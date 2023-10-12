import docx
from translate_text import translate_text_with_deepl

def apply_formatting(run, formatting):
    if formatting:
        run.bold = True

def translate_paragraph(paragraph, target_lang):
    for run in paragraph.runs:
        original_text = run.text
        if original_text:
            translated_text = translate_text_with_deepl(original_text, target_lang)
            run.clear()
            run.text = translated_text
            apply_formatting(run, run.bold)

def translate_tables_in_docx(doc, target_lang):
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    translate_paragraph(paragraph, target_lang)

def clean_toc_entry(entry):
    entry = entry.split('\t', 1)[-1].strip()
    entry = entry.split('\\o', 1)[0].strip()
    return entry

def translate_toc_entries(toc_entries, target_lang):
    translated_toc_entries = []
    for toc_entry in toc_entries:
        if toc_entry:
            translated_toc_entry = translate_text_with_deepl(toc_entry, target_lang)
            translated_toc_entries.append(translated_toc_entry)
    return translated_toc_entries

def translate_docx(docx_file_path, target_lang):
    doc = docx.Document(docx_file_path)
    toc_entries = []

    for paragraph in doc.paragraphs:
        if paragraph.style.name.startswith("toc"):
            toc_entries.append(clean_toc_entry(paragraph.text))

    translated_toc_entries = translate_toc_entries(toc_entries, target_lang)

    for paragraph in doc.paragraphs:
        if paragraph.style.name.startswith("toc"):
            if translated_toc_entries:
                # Replace the TOC entry with the translated version
                paragraph.clear()
                run = paragraph.add_run()
                run.text = translated_toc_entries.pop(0)  # Use pop to get the next translated entry
        else:
            translate_paragraph(paragraph, target_lang)

    translate_tables_in_docx(doc, target_lang)

    return doc


# Define the Word document file path
#word_document_path = "c:\\miso\\testy\\DS_Template_EN_TRM.MDGF.032.00_Tagetik for Approver 1.docx"

# Define the target language for translation
#target_lang = "DE"  # Change this to your desired target language code

# Translate the document, including the TOC, and get the translated DOCX document
#translated_doc = translate_docx(word_document_path, target_lang)

# Save the updated Word document with the translated TOC
#translated_doc.save("c:\\miso\\testy\\a_with_toc.docx")
