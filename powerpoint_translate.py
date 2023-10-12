from pptx import Presentation
from pptx.util import Pt
from translate_text import translate_text_with_deepl  # Import your translation function
from pptx.shapes.group import GroupShape

# Function to extract text and formatting from all text boxes in a slide
def extract_text_and_format(slide):
    text_and_format = []
    for shape in slide.shapes:
        if shape.shape_type == GroupShape:  # Check if the shape is a grouped shape
            for s in shape.shapes:
                if hasattr(s, "text_frame"):
                    for paragraph in s.text_frame.paragraphs:
                        for run in paragraph.runs:
                            text_and_format.append(run)
        elif hasattr(shape, "text_frame"):
            for paragraph in shape.text_frame.paragraphs:
                for run in paragraph.runs:
                    text_and_format.append(run)
    return text_and_format

def translate_and_update_slide(slide, target_lang):
    for shape in slide.shapes:
        if isinstance(shape, GroupShape):
            for s in shape.shapes:
                process_grouped_shape(s, target_lang)
        elif hasattr(shape, "text_frame"):
            for paragraph in shape.text_frame.paragraphs:
                for run in paragraph.runs:
                    original_text = run.text
                    original_font = run.font
                    translated_text = translate_text_with_deepl(original_text, target_lang)
                    run.text = translated_text
                    run.font.name = original_font.name
                    run.font.size = original_font.size

def process_grouped_shape(shape, target_language):
    if hasattr(shape, "text_frame"):
        for paragraph in shape.text_frame.paragraphs:
            for run in paragraph.runs:
                original_text = run.text
                original_font = run.font
                translated_text = translate_text_with_deepl(original_text, target_language)
                run.text = translated_text
                run.font.name = original_font.name
                run.font.size = original_font.size

def translate_pptx_file(input_pptx_path, target_language):
    # Load the PowerPoint presentation
    presentation = Presentation(input_pptx_path)

    # Iterate through slides, extract, translate, and update text while preserving formatting
    for slide in presentation.slides:
        translate_and_update_slide(slide, target_language)

    # Return the translated presentation
    return presentation

# Define the input and output file paths
#input_pptx_path = "c:\\miso\\testy\\DS_Template_EN_TRM.MDGF.032.00_Tagetik for Approver.pptx"  # Replace with the path to your input presentation
#output_pptx_path = "c:\\miso\\testy\\a.pptx"  # Specify the output path for the translated presentation

# Define the target language for translation
#target_language = "DE"  # Change this to your desired target language code

# Translate the PowerPoint presentation and save the translated version
#translate_pptx_file(input_pptx_path, target_language, output_pptx_path)