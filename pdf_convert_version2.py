
import os
import comtypes.client
from pdf2docx import Converter
from translate_word import translate_docx  # Import the translate function

def pdf_to_word(pdf_file, word_file):
    # Convert PDF to Word
    cv = Converter(pdf_file)
    cv.convert(word_file, start=0, end=None)
    cv.close()

def word_to_pdf(word_file, pdf_file):
    # Convert Word to PDF using Microsoft Word (requires Word installation)
    wdFormatPDF = 17  # PDF file format constant

    # Create a COM object for Microsoft Word
    word = comtypes.client.CreateObject("Word.Application")
    doc = word.Documents.Open(word_file)
    doc.SaveAs(pdf_file, FileFormat=wdFormatPDF)
    doc.Close()
    word.Quit()

def convert_pdf_to_translated_pdf(pdf_file_path, target_lang):
    # Create an absolute path for the temporary Word file
    temp_word_file = os.path.join(os.getcwd(), "temp_converted.docx")

    # Convert PDF to Word
    pdf_to_word(pdf_file_path, temp_word_file)

    # Translate the Word document
    translated_docx = translate_docx(temp_word_file, target_lang)

    # Save the translated DOCX to the same temporary Word file path
    translated_docx.save(temp_word_file)

    # Create an absolute path for the temporary PDF file
    temp_pdf_file = os.path.join(os.getcwd(), "temp_translated.pdf")

    # Convert the translated Word document to PDF
    word_to_pdf(temp_word_file, temp_pdf_file)

    # Remove the temporary Word file
    os.remove(temp_word_file)

    # Read the temporary PDF data
    with open(temp_pdf_file, 'rb') as pdf_file:
        translated_pdf_data = pdf_file.read()

    # Remove the temporary PDF file
    os.remove(temp_pdf_file)

    # Save the translated PDF to the specified file path
    #with open(output_pdf_path, 'wb') as output_pdf_file:
        #output_pdf_file.write(translated_pdf_data)

    #return translated_pdf_data

#if __name__ == "__main__":
    # Input PDF file path
    #pdf_input_file = "c:\\miso\\testy\\DS_Template_EN_TRM.MDGF.032.00_Tagetik for Approver.pdf"
    #target_lang = "DE"  # Replace with the target language code
    #output_pdf_file = "c:\\miso\\testy\\translated_pdf.pdf"

    # Convert PDF to Translated PDF and save it
    #translated_pdf = convert_pdf_to_translated_pdf(pdf_input_file, target_lang, output_pdf_file)

    # Now, 'translated_pdf' contains the translated PDF data, and it's also saved to "translated_pdf.pdf" on the file system.
