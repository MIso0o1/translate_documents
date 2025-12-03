import openpyxl
from translate_text import translate_text_with_deepl
import json
from datetime import datetime

def is_numeric_or_formula(value):
    if isinstance(value, (int, float)):
        return True
    elif isinstance(value, str) and value.startswith("="):
        return True
    return False

def translate_excel_cell(cell, target_lang):
    if cell.value and not is_numeric_or_formula(cell.value):
        # Convert datetime objects to strings before translation
        if isinstance(cell.value, datetime):
            cell.value = cell.value.strftime("%Y-%m-%d %H:%M:%S")
        
        # Translate the cell value
        translated_text = translate_text_with_deepl(cell.value, target_lang)

        # Update the cell with the translated text
        cell.value = translated_text

def translate_excel_file(excel_file_path, target_lang):
    # Open the Excel file
    workbook = openpyxl.load_workbook(excel_file_path)

    # Iterate through all sheets in the workbook
    for sheet_name in workbook.sheetnames:
        sheet = workbook[sheet_name]

        # Iterate through all cells in the sheet
        for row in sheet.iter_rows():
            for cell in row:
                translate_excel_cell(cell, target_lang)

    # Return the modified Excel workbook
    return workbook

