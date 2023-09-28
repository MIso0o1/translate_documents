
from pptx import Presentation
from pptx.util import Pt
from translate_text import translate_text_with_deepl  # Import your translation function


# Function to extract text and formatting from all text boxes in a slide
def extract_text_and_format(slide):
    text_and_format = []
    for shape in slide.shapes:
        if hasattr(shape, "text_frame"):
            for paragraph in shape.text_frame.paragraphs:
                for run in paragraph.runs:
                    text_and_format.append((run.text, run.font))
    return text_and_format

# Function to translate text while preserving formatting and update the slide
def translate_and_update_slide(slide, target_lang):
    text_and_format = extract_text_and_format(slide)
    for shape in slide.shapes:
        if hasattr(shape, "text_frame"):
            for paragraph in shape.text_frame.paragraphs:
                for run in paragraph.runs:
                    original_text, original_font = text_and_format.pop(0)
                    translated_text = translate_text_with_deepl(original_text, target_lang)
                    run.text = translated_text
                    # Preserve original text formatting
                    run.font.name = original_font.name
                    run.font.size = original_font.size


def translate_pptx_file(input_pptx_path, target_language):
    # Load the PowerPoint presentation
    presentation = Presentation(input_pptx_path)

    # Iterate through slides, extract, translate, and update text while preserving formatting
    for slide in presentation.slides:
        translate_and_update_slide(slide, target_language)

    return presentation


# Example usage:
#if __name__ == "__main__":
    #input_pptx_path = 'c:\\miso\\testy\\DS_Template_EN_TRM.MDGF.032.00_Tagetik for Approver.pptx'
    #target_language = 'DE'  # Replace with your target language code
    #output_pptx_path = 'c:\\miso\\testy\\translated_presentation.pptx'  # Output file path

    #translate_pptx_file(input_pptx_path, target_language, output_pptx_path)