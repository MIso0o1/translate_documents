import docx
from translate_text import translate_text_with_deepl

def apply_formatting(run, formatting):
    if formatting:
        run.bold = True

def translate_paragraph(paragraph, target_lang):
    original_runs = paragraph.runs
    paragraph.clear()

    for run in original_runs:
        original_text = run.text

        if original_text:
            # Translate the run text
            translated_text = translate_text_with_deepl(original_text, target_lang)

            # Create a new run with the translated text and the same formatting
            new_run = paragraph.add_run()
            new_run.text = translated_text
            new_run.bold = run.bold
            new_run.italic = run.italic
            new_run.underline = run.underline
            new_run.font.size = run.font.size
            new_run.font.name = run.font.name
            new_run.font.color.rgb = run.font.color.rgb  # Preserve font color

def translate_tables_in_docx(doc, target_lang):
    # Iterate through all tables in the document
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                # Translate the text in the cell
                translated_text = translate_text_with_deepl(cell.text, target_lang)

                # Clear the existing content in the cell
                for paragraph in cell.paragraphs:
                    for run in paragraph.runs:
                        run.clear()

                # Add the translated text with preserved formatting
                paragraph = cell.paragraphs[0]
                run = paragraph.add_run()
                run.text = translated_text
                apply_formatting(run, cell.paragraphs[0].runs[0].bold)

def translate_docx(docx_file_path, target_lang):
    # Open the Word document
    doc = docx.Document(docx_file_path)

    # Translate paragraphs in the document
    for paragraph in doc.paragraphs:
        translate_paragraph(paragraph, target_lang)

    # Translate tables in the document
    translate_tables_in_docx(doc, target_lang)

    return doc


# Define the Word document file path
word_document_path = "c:\\miso\\testy\\DS_Template_EN_TRM.MDGF.032.00_Tagetik for Approver.docx"

# Define the target language for translation
target_lang = "DE"  # Change this to your desired target language code

# Translate the whole document and get the translated DOCX document
translated_doc = translate_docx(word_document_path, target_lang)

# Save the translated DOCX document if needed
translated_doc.save("c:\\miso\\testy\\a.docx")
